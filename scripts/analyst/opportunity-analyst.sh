#!/usr/bin/env bash
# Opportunity Analyst — independent second-brain (APP-221).
# Engine: Codex (gpt-5.6-sol, effort very high) running the user's codex skill
# `autocompany-opportunity-director`. Runs INSIDE the company container as user `app`
# (has codex auth via CODEX_HOME on the persistent volume + the skill + Context7 key).
# The skill analyzes and returns a full decision report + a trailing ```json registry
# block; THIS script disposes: writes analysis-directive.md (draft, operator copies —
# NEVER auto-applied) and, if the json validates, the updated candidate-registry.md.
# Scope: reads scan/consensus/registry/framework; writes ONLY analysis-directive.md,
# candidate-registry.md, analyst-progress.md. Never applies a directive, writes product
# code, contacts anyone, or touches appricode-panel.
set -uo pipefail

APP="${APP_DIR:-/app}"
export CODEX_HOME="${CODEX_HOME:-/app/logs/.codex}"
SKILL_DIR="$CODEX_HOME/skills/autocompany-opportunity-director"
SKILL_SRC="$APP/scripts/analyst/codex-skill/autocompany-opportunity-director"
SCAN="$APP/docs/research/opportunity-scan.md"
REGISTRY="$APP/memories/candidate-registry.md"
CONSENSUS="$APP/memories/consensus.md"
OUT_DIRECTIVE="$APP/memories/analysis-directive.md"
PROGRESS="$APP/memories/analyst-progress.md"

CODEX_BIN="$(command -v codex || echo /usr/local/bin/codex)"
MODEL="${ANALYST_MODEL:-gpt-5.6-sol}"
# Operator caps Codex at max effort "high" — respect it; do not override the default.
EFFORT="${ANALYST_EFFORT:-high}"
TIMEOUT="${ANALYST_TIMEOUT:-1500}"
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

log() { printf '%s\n' "$1" >> "$PROGRESS"; }
fail() { log "[$STAMP] ANALYST_FAILED: $1"; echo "ANALYST_FAILED: $1" >&2; exit 1; }

# --- preconditions ---
for f in "$SCAN" "$REGISTRY" "$CONSENSUS"; do [ -f "$f" ] || fail "missing input: $f"; done
[ -x "$CODEX_BIN" ] || fail "codex CLI not found"
[ -s "$CODEX_HOME/auth.json" ] || fail "codex auth.json missing at $CODEX_HOME (needs CODEX_AUTH_B64 seed)"
# self-heal the skill into the persistent CODEX_HOME from the repo copy
if [ ! -f "$SKILL_DIR/SKILL.md" ] && [ -f "$SKILL_SRC/SKILL.md" ]; then
  mkdir -p "$CODEX_HOME/skills" && cp -r "$SKILL_SRC" "$CODEX_HOME/skills/"
  chmod +x "$SKILL_DIR"/scripts/*.sh 2>/dev/null || true
fi
[ -f "$SKILL_DIR/SKILL.md" ] || fail "codex skill autocompany-opportunity-director not installed"

WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
MSG="$WORK/msg.txt"

read -r -d '' PROMPT <<'EOF'
$autocompany-opportunity-director ile bu opportunity scan'in tamamını incele, adayları kendin seç ve Auto Company direktifini yaz.

Inputs are in this workspace (/app) — find them with rg:
- docs/research/opportunity-scan.md  (the complete scan — read all of it)
- memories/consensus.md              (Auto Company's own current selection + state)
- memories/candidate-registry.md     (Selected / Archived / Pending buckets — dedup key is axis = buyer × delivery × price)
- PROJECT_EVALUATION_FRAMEWORK.md

Do NOT write or modify any files yourself — output your full decision report as your final message, following the skill's output order.
EOF

# Same sandbox the company loop uses in-container (auto-loop.sh: danger-full-access);
# read-only fails under nested namespaces (bwrap). The skill is instructed not to write,
# and we snapshot/restore human-directive.md so the analyst can never auto-apply a directive.
SANDBOX="${CODEX_SANDBOX_MODE:-danger-full-access}"
run_codex() { # $1=effort
  ( cd "$APP" && timeout "$TIMEOUT" "$CODEX_BIN" exec --skip-git-repo-check \
      -c sandbox_mode="$SANDBOX" -m "$MODEL" -c model_reasoning_effort="$1" \
      -o "$MSG" "$PROMPT" ) >"$WORK/out" 2>&1
}

# draft-only guardrail: the analyst must never modify the live directive
DIRECTIVE_LIVE="$APP/memories/human-directive.md"
DIRECTIVE_BAK=""
if [ -f "$DIRECTIVE_LIVE" ]; then DIRECTIVE_BAK="$WORK/human-directive.bak"; cp "$DIRECTIVE_LIVE" "$DIRECTIVE_BAK"; fi
restore_directive() {
  [ -n "$DIRECTIVE_BAK" ] && ! cmp -s "$DIRECTIVE_BAK" "$DIRECTIVE_LIVE" 2>/dev/null && {
    cp "$DIRECTIVE_BAK" "$DIRECTIVE_LIVE"; log "[$STAMP] NOTE: restored human-directive.md (analyst must not write it)"; }
}

USED_EFFORT="$EFFORT"
run_codex "$EFFORT"; rc=$?
if [ "$rc" -ne 0 ] || [ ! -s "$MSG" ]; then
  log "[$STAMP] codex run failed (rc=$rc); one retry at effort='$EFFORT'"
  run_codex "$EFFORT"; rc=$?
fi
restore_directive
[ "$rc" -eq 0 ] && [ -s "$MSG" ] || fail "codex produced no output (rc=$rc); tail: $(tail -3 "$WORK/out" 2>/dev/null | tr '\n' ' ')"

# --- PASS 1 dispose: write the full decision report to analysis-directive.md ---
python3 - "$MSG" "$OUT_DIRECTIVE" "$PROGRESS" "$STAMP" "$MODEL" "$USED_EFFORT" <<'PY' || fail "report post-processing failed"
import sys
msg_p, out_p, prog, stamp, model, effort = sys.argv[1:7]
report = open(msg_p, encoding="utf-8").read().strip()
if len(report) < 200:
    open(prog,"a",encoding="utf-8").write(f"[{stamp}] ANALYST_FAILED: report too short ({len(report)} chars)\n"); sys.exit(1)
doc = (f"# Opportunity Analyst — {stamp}\n\n"
       f"*Engine: Codex `{model}` · effort `{effort}` · skill `autocompany-opportunity-director` · registry-write: PENDING*\n\n"
       f"---\n\n{report}\n")
open(out_p,"w",encoding="utf-8").write(doc)
open(prog,"a",encoding="utf-8").write(f"[{stamp}] REPORT OK | model={model} effort={effort} | report={len(report)}c\n")
print("REPORT_OK")
PY

# --- PASS 2: registry diff (dedicated codex call — report + old registry → json) ---
REG_EFFORT="${ANALYST_REGISTRY_EFFORT:-medium}"   # mechanical transform; stays within the operator's max=high cap
REG_MSG="$WORK/reg.txt"; REG_PROMPT="$WORK/reg_prompt.txt"
python3 - "$MSG" "$REGISTRY" > "$REG_PROMPT" <<'PY'
import sys
report=open(sys.argv[1],encoding="utf-8").read()
reg=open(sys.argv[2],encoding="utf-8").read()
print("You are updating Auto Company's candidate registry from an analyst decision report. Output ONLY a single ```json code block and nothing else.\n\n"
      "CURRENT REGISTRY:\n"+reg+"\n\nANALYST DECISION REPORT (verdicts + Auto-Company-vs-analyst selection):\n"+report+"\n\n"
      "Produce: {\"registry_md\":\"<COMPLETE updated candidate-registry.md. Keep the file structure and the three headers '## Selected Candidates', '## Archived Candidates', '## Pending Queue' with markdown tables and the SAME columns as the current registry. Apply the report verdicts: ACTIVE / CONDITIONAL GO / QUEUED -> Selected or Pending; NO-GO or de-selected -> Archived; HOLD / research-only -> Pending. Dedup by axis (buyer x delivery x price). Retain EVERY candidate already in the current Archived section - never drop one.>\"}\n"
      "Valid JSON, newlines escaped as \\n.")
PY

( cd "$APP" && timeout "$TIMEOUT" "$CODEX_BIN" exec --skip-git-repo-check \
    -c sandbox_mode="$SANDBOX" -m "$MODEL" -c model_reasoning_effort="$REG_EFFORT" \
    -o "$REG_MSG" "$(cat "$REG_PROMPT")" ) >"$WORK/reg_out" 2>&1 || true

reg_written=$(python3 - "$REG_MSG" "$REGISTRY" <<'PY'
import sys, json, re, os
msg_p, reg_p = sys.argv[1:3]
if not os.path.exists(msg_p) or os.path.getsize(msg_p)==0: print("skipped (pass-2 no output)"); sys.exit(0)
out=open(msg_p,encoding="utf-8").read()
m=re.search(r"```json\s*(\{.*?\})\s*```", out, re.S) or re.search(r"(\{.*\})", out, re.S)
if not m: print("skipped (no json)"); sys.exit(0)
try: reg_new=json.loads(m.group(1)).get("registry_md","")
except Exception: print("skipped (bad json)"); sys.exit(0)
if not reg_new or not all(h in reg_new for h in ("## Selected Candidates","## Archived Candidates","## Pending Queue")):
    print("skipped (missing sections)"); sys.exit(0)
def arch_rows(txt):
    seg=txt.split("## Archived Candidates",1); rows={}
    if len(seg)>1:
        for line in seg[1].split("## Pending Queue",1)[0].splitlines():
            s=line.strip()
            if s.startswith("|") and "---" not in s:
                name=s.strip("|").split("|")[0].strip()
                if name and name.lower()!="name": rows[name]=line.rstrip()
    return rows
# deterministic guarantee: re-insert any old Archived row the model dropped (never lose history)
old_rows=arch_rows(open(reg_p,encoding="utf-8").read())
missing=[old_rows[n] for n in old_rows if n not in reg_new]
merged=0
if missing:
    idx=reg_new.find("## Pending Queue")
    reg_new=reg_new[:idx].rstrip()+"\n"+"\n".join(missing)+"\n\n"+reg_new[idx:]
    merged=len(missing)
open(reg_p,"w",encoding="utf-8").write(reg_new.rstrip()+"\n")
print(f"yes (merged {merged} retained-archived)" if merged else "yes")
PY
)
log "[$STAMP] REGISTRY pass-2 (effort=$REG_EFFORT): $reg_written"
# reflect final registry status in the report header
python3 - "$OUT_DIRECTIVE" "$reg_written" <<'PY' 2>/dev/null || true
import sys
p,rw=sys.argv[1],sys.argv[2]
t=open(p,encoding="utf-8").read().replace("registry-write: PENDING",f"registry-write: {rw}",1)
open(p,"w",encoding="utf-8").write(t)
PY

echo "Opportunity Analyst run complete ($STAMP) — registry: $reg_written."
