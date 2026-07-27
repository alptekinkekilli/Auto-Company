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
# Root cause of the ORIGINAL E2BIG failure (2026-07-27, docs/research/
# opportunity-analyst-pass2-and-directive-promotion-diagnosis-2026-07-27.md):
# the full registry+report were interpolated into the prompt STRING and passed
# as a single execve() argv element, blowing past Linux's ~128KiB per-argument
# MAX_ARG_STRLEN. Fixed by giving codex file PATHS instead of inlined content.
#
# Root cause of a SECOND, more serious gap the operator caught in that fix
# (same date): ~180KB of this registry is an append-only historical journal
# (## PART A / Cycle N discovery-scan sections, after "## Exhausted patterns /
# lessons") that the pass-2 prompt never told the model to preserve — and the
# model is never trusted to reproduce ~280KB of content losslessly regardless.
# Fix: never ask a model to reproduce the whole file. Mechanically isolate the
# "## Selected" .. "## Archived" span (the only part that is genuinely live
# decision state) via exact string splitting BEFORE calling codex, and splice
# the model's proposed replacement for ONLY that span back in via
# scripts/analyst/merge_registry.py — everything else is byte-identical by
# construction, never by instruction-following. See that script for the
# candidate-ID-preservation and duplicate-axis invariant checks it enforces
# before writing anything.
REG_EFFORT="${ANALYST_REGISTRY_EFFORT:-medium}"   # mechanical transform; stays within the operator's max=high cap
REG_MSG="$WORK/reg.txt"; REG_PROMPT="$WORK/reg_prompt.txt"
LIVE_SPAN_FILE="$WORK/registry-live-span.md"

python3 - "$REGISTRY" > "$LIVE_SPAN_FILE" 2>"$WORK/extract_err" <<'PY'
import sys
t = open(sys.argv[1], encoding="utf-8").read()
START = "\n\n## Selected\n"; END = "\n\n## Exhausted patterns / lessons\n"
if START not in t or END not in t:
    print(f"marker not found (START={START in t}, END={END in t})", file=sys.stderr)
    sys.exit(1)
before, rest = t.split(START, 1)
live_and_after = START + rest
live, _after = live_and_after.split(END, 1)
sys.stdout.write(live)
PY
extract_rc=$?
if [ "$extract_rc" -ne 0 ]; then
    reg_written="skipped (could not isolate live span: $(cat "$WORK/extract_err" 2>/dev/null | tr '\n' ' '))"
fi

if [ -z "${reg_written:-}" ]; then
    python3 - "$OUT_DIRECTIVE" "$LIVE_SPAN_FILE" > "$REG_PROMPT" <<'PY'
import sys
report_path, live_span_path = sys.argv[1:3]
print("You are updating the LIVE portion of Auto Company's candidate registry from an "
      "analyst decision report. Output ONLY a single ```json code block and nothing else.\n\n"
      f"Read the COMPLETE current live registry span at: {live_span_path}\n"
      "(this file starts with the line '## Selected' and contains, in order: '## Selected', "
      "'## Pending shortlist', '## Deferred / HOLD index', and '## Archived' — it is NOT the "
      "whole registry file, only its live-decision-state span. Do not invent other sections.)\n"
      f"Read the COMPLETE analyst decision report (verdicts + Auto-Company-vs-analyst selection) at: {report_path}\n\n"
      "Produce: {\"registry_live_span\":\"<the COMPLETE updated live span, starting with '## Selected' "
      "and ending at the last line of the Archived section (do not include '## Exhausted patterns / "
      "lessons' or anything after it). Keep the exact same four headers and table/bullet formats "
      "as the input span. Apply the report's verdicts: ACTIVE/CONDITIONAL GO/QUEUED -> Selected or "
      "Pending shortlist; HOLD/research-only -> Deferred / HOLD index; NO-GO or de-selected -> "
      "Archived. Dedup by axis (buyer x delivery x price). Every candidate ID present in the input "
      "span MUST still appear somewhere in the output span - moving between subsections is fine, "
      "silently dropping one is not.>\"}\n"
      "Valid JSON, newlines escaped as \\n.")
PY

    ( cd "$APP" && timeout "$TIMEOUT" "$CODEX_BIN" exec --skip-git-repo-check \
        -c sandbox_mode="$SANDBOX" -m "$MODEL" -c model_reasoning_effort="$REG_EFFORT" \
        -o "$REG_MSG" "$(cat "$REG_PROMPT")" ) >"$WORK/reg_out" 2>&1
    REG_RC=$?
    # preserve diagnostics past the WORK dir's EXIT trap so a silent pass-2 failure is
    # diagnosable next time (bare "skipped (pass-2 no output)" gave no root cause)
    REG_DEBUG="$APP/logs/analyst-reg-debug.log"
    mkdir -p "$(dirname "$REG_DEBUG")" 2>/dev/null || true
    {
      echo "[$STAMP] pass-2 rc=$REG_RC prompt_bytes=$(wc -c < "$REG_PROMPT" 2>/dev/null) msg_bytes=$(wc -c < "$REG_MSG" 2>/dev/null || echo 0)"
      tail -c 4000 "$WORK/reg_out" 2>/dev/null
      echo "---"
    } >> "$REG_DEBUG" 2>/dev/null || true

    MERGE_SCRIPT="$APP/scripts/analyst/merge_registry.py"
    if [ -f "$MERGE_SCRIPT" ]; then
        reg_written="$(python3 "$MERGE_SCRIPT" "$REGISTRY" "$REG_MSG" "$REGISTRY" 2>&1)"
    else
        reg_written="skipped (merge_registry.py not found)"
    fi
fi
log "[$STAMP] REGISTRY pass-2 (effort=$REG_EFFORT): $reg_written"
# reflect final registry status in the report header
python3 - "$OUT_DIRECTIVE" "$reg_written" <<'PY' 2>/dev/null || true
import sys
p,rw=sys.argv[1],sys.argv[2]
t=open(p,encoding="utf-8").read().replace("registry-write: PENDING",f"registry-write: {rw}",1)
open(p,"w",encoding="utf-8").write(t)
PY


# --- PASS 3: deterministic directive-promotion gate (narrow v1, 2026-07-27) ---
# Separate from PASS 1/2 above: decides whether the report's proposed
# human-directive.md text may be auto-applied, per the operator's explicit
# narrow scoping (docs/research/opportunity-analyst-pass2-and-directive-
# promotion-diagnosis-2026-07-27.md § 5-7). Pure deterministic text matching,
# NOT another model call — see scripts/analyst/promote_directive.py for the
# exact rules. Best-effort: never let a promotion-gate failure break the run.
PROMOTE_SCRIPT="$APP/scripts/analyst/promote_directive.py"
promotion_result="skipped (promote_directive.py not found)"
if [ -f "$PROMOTE_SCRIPT" ]; then
    promotion_result="$(python3 "$PROMOTE_SCRIPT" "$OUT_DIRECTIVE" 2>&1 || echo "BLOCKED: promote_directive.py errored")"
fi
log "[$STAMP] PROMOTION (narrow v1): $promotion_result"

echo "Opportunity Analyst run complete ($STAMP) — registry: $reg_written — promotion: $promotion_result."
