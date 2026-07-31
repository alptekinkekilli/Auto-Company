#!/usr/bin/env bash
# Opportunity Analyst — jcode variant (gate-5 pilot; RUNBOOK-jcode-gecis.md).
# NOT wired into cron. The cron wrapper still calls opportunity-analyst.sh (codex);
# this file becomes the target only after the gate-5 acceptance run passes and the
# operator says so. Until then it exists to be run BY HAND for acceptance testing:
#   docker exec -u app <container> bash /app/scripts/analyst/opportunity-analyst-jcode.sh
#
# Behavioral contract is identical to opportunity-analyst.sh — same inputs, same
# three passes, same outputs (analysis-directive.md draft / registry live-span merge /
# deterministic promotion gate), same REPORT_OK protocol, same directive-restore
# guardrail. What changed and WHY:
#
#   engine        codex exec --json -o msg        ->  jcode run --ndjson (final text
#                 (message written to a file)         extracted from the `done` event)
#   skill         $skill from CODEX_HOME          ->  the model READS the repo skill
#                 (synced every run — a stale-        file itself. One source of truth,
#                 copy bug lived here once)           no sync step to go stale.
#   effort        -c model_reasoning_effort=X     ->  JCODE_OPENAI_REASONING_EFFORT=X
#   model check   (codex validated -m)            ->  EXPLICIT preflight against
#                                                     `jcode model list` — jcode
#                                                     SILENTLY substitutes its default
#                                                     model for an unknown -m (measured
#                                                     2026-07-31; the ladder must never
#                                                     inherit that trap)
#   sandbox       -c sandbox_mode=...             ->  none; container isolation + the
#                                                     skill's no-write instruction +
#                                                     the directive snapshot/restore
#   budget        thread_id -> analyst-codex-     ->  session_id (done event) ->
#                 sessions.log (ccusage exclude)      analyst-jcode-sessions.log, same
#                                                     fail-closed direction. jcode runs
#                                                     never appear in CODEX_HOME, so
#                                                     ccusage cannot MIS-attribute them;
#                                                     the ledger exists for the future
#                                                     jcode-native accounting.
#   cost line     (implicit in ccusage)           ->  engine-usage-cost.py on the
#                                                     ndjson, logged to progress. For
#                                                     gpt-5.6-sol this is an ESTIMATED
#                                                     figure until the price row is
#                                                     calibrated (gate 4/5) — logged,
#                                                     never gated on.
set -uo pipefail

APP="${APP_DIR:-/app}"
SKILL_MD="$APP/scripts/analyst/codex-skill/autocompany-opportunity-director/SKILL.md"
REGISTRY="$APP/memories/candidate-registry.md"
CONSENSUS="$APP/memories/consensus.md"
OUT_DIRECTIVE="$APP/memories/analysis-directive.md"
PROGRESS="$APP/memories/analyst-progress.md"

JCODE_BIN="$(command -v jcode || echo /usr/local/bin/jcode)"
PROVIDER="${ANALYST_PROVIDER:-openai}"
MODEL="${ANALYST_MODEL:-gpt-5.6-sol}"
# Operator caps effort at "high" — respect it; do not override the default.
EFFORT="${ANALYST_EFFORT:-high}"
TIMEOUT="${ANALYST_TIMEOUT:-1500}"
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
JQUIET=(--quiet --no-update --no-selfdev)
export JCODE_NO_TELEMETRY=1

log() { printf '%s\n' "$1" >> "$PROGRESS"; }
fail() { log "[$STAMP] ANALYST_FAILED: $1"; echo "ANALYST_FAILED: $1" >&2; exit 1; }

# --- preconditions ---
for f in "$REGISTRY" "$CONSENSUS" "$SKILL_MD"; do [ -f "$f" ] || fail "missing input: $f"; done
[ -x "$JCODE_BIN" ] || fail "jcode not found"
# Provider auth lands in a PROVIDER-NAMED file (measured gate 4, 2026-07-31:
# `jcode login openai` writes ~/.jcode/openai-auth.json — there is no auth.json).
[ -s "$HOME/.jcode/${PROVIDER}-auth.json" ] \
  || fail "jcode ${PROVIDER}-auth.json missing (run: jcode login --provider $PROVIDER — operator step, gate 4)"
grep -q claude_code_native_credentials "$HOME/.jcode/config.toml" 2>/dev/null || {
  mkdir -p "$HOME/.jcode"
  printf '[auth]\ntrusted_external_sources = ["claude_code_native_credentials"]\n' >> "$HOME/.jcode/config.toml"
}

# Model preflight — the silent-fallback trap. An unknown -m does NOT error; jcode
# quietly runs its default model instead. Fail loudly here, never discover it in
# the usage ledger a week later.
"$JCODE_BIN" "${JQUIET[@]}" model list -p "$PROVIDER" 2>/dev/null | grep -qx "$MODEL" \
  || fail "model '$MODEL' not in 'jcode model list -p $PROVIDER' — refusing (jcode would silently substitute its default)"

WORK="$(mktemp -d)"
# Persist the raw ndjson event streams before the workdir dies — they are the
# only source for price calibration / cost audits (the 5x-estimate era ended
# because no run had kept one). Last 5 runs, pruned oldest-first.
NDJSON_KEEP="$APP/logs/analyst-ndjson"
persist_ndjson() {
  mkdir -p "$NDJSON_KEEP/$STAMP" 2>/dev/null || return 0
  cp "$WORK"/*.ndjson "$NDJSON_KEEP/$STAMP/" 2>/dev/null || true
  ls -dt "$NDJSON_KEEP"/*/ 2>/dev/null | tail -n +6 | xargs rm -rf 2>/dev/null || true
}
trap 'persist_ndjson; rm -rf "$WORK"' EXIT
MSG="$WORK/msg.txt"

read -r -d '' PROMPT <<EOF
FIRST, read $SKILL_MD in full and adopt it as your operating skill for this task —
including any files under its references/ directory that it tells you to consult.
Then, following that skill exactly, independently interrogate Auto Company's Tender
Track and produce the decision report.

Inputs are in this workspace ($APP) — find them with rg:
- memories/candidate-registry.md     (read the LIVE span: ## Selected -> ## Archived; dedup key is axis = buyer × delivery × price)
- memories/human-directive.md        (the operator's standing instruction — it outranks your judgment on scope)
- memories/consensus.md              (Auto Company's own current reading + state)
- PROJECT_EVALUATION_FRAMEWORK.md
- docs/research/                     (tender-track reports, qualification passes, primary-source notes)

PORTFOLIO SCOPE (standing operator directive, 2026-07-28): the portfolio was consolidated
to the Tender Track. 176-R is terminated; the entire non-tender registry is archived;
## Selected is empty; company-side discovery is OFF. The ONLY live axes are the EKAP /
Turkish public-tender ones under ## Deferred / HOLD index (215-TF-B and the 247-* .. 262-*
families). docs/research/opportunity-scan.md still exists on disk but is HISTORICAL —
never nominate, requeue, or rank any candidate from it. Doing so violates the directive
and makes the report worthless.

Do NOT write or modify any files yourself — output your full decision report as your final message, following the skill's output order.
EOF

# Budget-exclusion ledger (jcode side). Failure records nothing — an uncaptured
# analyst session counts toward company totals, the mandated fail-closed direction.
ANALYST_SESSIONS_FILE="$APP/logs/analyst-jcode-sessions.log"
record_analyst_session() { # $1=ndjson events file
  python3 - "$1" "$ANALYST_SESSIONS_FILE" <<'PY' 2>/dev/null || true
import json, sys, time
events_p, ledger_p = sys.argv[1], sys.argv[2]
sid = None
with open(events_p, encoding="utf-8", errors="replace") as fh:
    for line in fh:
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except Exception:
            continue
        if ev.get("type") == "done" and ev.get("session_id"):
            sid = str(ev["session_id"])
if not sid:
    sys.exit(0)
try:
    existing = open(ledger_p, encoding="utf-8").read()
except FileNotFoundError:
    existing = ""
if sid in existing:
    sys.exit(0)
with open(ledger_p, "a", encoding="utf-8") as fh:
    fh.write(f"{int(time.time())} {sid}\n")
PY
}

# Extract the final assistant text from an ndjson stream into a file.
# The `done` event's .text is the whole final message; `-o`-style output files
# do not exist in jcode. Exit 1 (leaving the output empty) if no done event.
# Delegates to the ONE extractor (scripts/core/jcode-final-text.py). This used to read
# `done.text` directly, which is the last text BLOCK rather than the answer — measured
# 2026-07-31. It never bit the analyst (its 42k-char reports came through done.text
# whole, and the <200-char guard would not have caught a half-lost 42k report either),
# but the failure is silent by construction, so both callers now share one reading.
extract_final_text() { # $1=ndjson file  $2=out file
  python3 "$APP/scripts/core/jcode-final-text.py" "$1" > "$2" 2>/dev/null
  [ -s "$2" ]
}

log_run_cost() { # $1=ndjson file $2=label — visibility only, never gating
  local cost
  cost="$(python3 "$APP/scripts/core/engine-usage-cost.py" --ndjson-file "$1" 2>/dev/null)" \
    && log "[$STAMP] COST $2: $cost" \
    || log "[$STAMP] COST $2: unavailable (adapter error — run counts toward company totals)"
}

run_jcode() { # $1=effort $2=prompt $3=events-out $4=text-out
  ( cd "$APP" && JCODE_OPENAI_REASONING_EFFORT="$1" timeout "$TIMEOUT" \
      "$JCODE_BIN" -p "$PROVIDER" -m "$MODEL" -C "$APP" run "$2" \
      "${JQUIET[@]}" --ndjson ) >"$3" 2>"$3.err"
  local rc=$?
  record_analyst_session "$3"
  extract_final_text "$3" "$4" || return 1
  return $rc
}

# --- draft-only guardrail: the analyst must never modify the live directive ---
DIRECTIVE_LIVE="$APP/memories/human-directive.md"
DIRECTIVE_BAK=""
if [ -f "$DIRECTIVE_LIVE" ]; then DIRECTIVE_BAK="$WORK/human-directive.bak"; cp "$DIRECTIVE_LIVE" "$DIRECTIVE_BAK"; fi
DIRECTIVE_SHA=""
[ -n "$DIRECTIVE_BAK" ] && DIRECTIVE_SHA=$(sha256sum "$DIRECTIVE_LIVE" 2>/dev/null | cut -d' ' -f1)

restore_directive() {
  [ -n "$DIRECTIVE_BAK" ] || return 0
  AC_APP_DIR="$APP" AC_ACTOR="opportunity-analyst-jcode" \
  python3 "$APP/scripts/core/directive_writer.py" restore \
      --from-file "$DIRECTIVE_BAK" --expect-sha256 "${DIRECTIVE_SHA:-none}" \
      >>"$PROGRESS" 2>&1 \
    || log "[$STAMP] NOTE: directive restore refused (the slot was written during the analyst run) — live file left alone, candidate kept in memories/human-directive-recovery/"
}

USED_EFFORT="$EFFORT"
run_jcode "$EFFORT" "$PROMPT" "$WORK/ev1.ndjson" "$MSG"; rc=$?
if [ "$rc" -ne 0 ] || [ ! -s "$MSG" ]; then
  log "[$STAMP] jcode run failed (rc=$rc); one retry at effort='$EFFORT'"
  run_jcode "$EFFORT" "$PROMPT" "$WORK/ev1b.ndjson" "$MSG"; rc=$?
fi
restore_directive
[ "$rc" -eq 0 ] && [ -s "$MSG" ] || fail "jcode produced no output (rc=$rc); tail: $(tail -3 "$WORK/ev1.ndjson.err" 2>/dev/null | tr '\n' ' ')"
log_run_cost "$WORK/ev1.ndjson" "pass-1"

# --- PASS 1 dispose: write the full decision report to analysis-directive.md ---
python3 - "$MSG" "$OUT_DIRECTIVE" "$PROGRESS" "$STAMP" "$MODEL" "$USED_EFFORT" <<'PY' || fail "report post-processing failed"
import sys
msg_p, out_p, prog, stamp, model, effort = sys.argv[1:7]
report = open(msg_p, encoding="utf-8").read().strip()
if len(report) < 200:
    open(prog,"a",encoding="utf-8").write(f"[{stamp}] ANALYST_FAILED: report too short ({len(report)} chars)\n"); sys.exit(1)
doc = (f"# Opportunity Analyst — {stamp}\n\n"
       f"*Engine: jcode `{model}` · effort `{effort}` · skill `autocompany-opportunity-director` (read from repo) · registry-write: PENDING*\n\n"
       f"---\n\n{report}\n")
open(out_p,"w",encoding="utf-8").write(doc)
open(prog,"a",encoding="utf-8").write(f"[{stamp}] REPORT OK | engine=jcode model={model} effort={effort} | report={len(report)}c\n")
print("REPORT_OK")
PY

# --- PASS 2: registry live-span diff (same single-boundary design as codex variant;
# see opportunity-analyst.sh for the E2BIG and journal-loss history that shaped it) ---
REG_EFFORT="${ANALYST_REGISTRY_EFFORT:-medium}"
REG_MSG="$WORK/reg.txt"; REG_PROMPT_FILE="$WORK/reg_prompt.txt"
LIVE_SPAN_FILE="$WORK/registry-live-span.md"

python3 "$APP/scripts/analyst/merge_registry.py" --extract-live-span "$REGISTRY" \
  > "$LIVE_SPAN_FILE" 2>"$WORK/extract_err"
extract_rc=$?
if [ "$extract_rc" -ne 0 ]; then
    reg_written="skipped (could not isolate live span: $(cat "$WORK/extract_err" 2>/dev/null | tr '\n' ' '))"
fi

if [ -z "${reg_written:-}" ]; then
    python3 - "$OUT_DIRECTIVE" "$LIVE_SPAN_FILE" > "$REG_PROMPT_FILE" <<'PY'
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

    run_jcode "$REG_EFFORT" "$(cat "$REG_PROMPT_FILE")" "$WORK/ev2.ndjson" "$REG_MSG"
    REG_RC=$?
    log_run_cost "$WORK/ev2.ndjson" "pass-2"
    REG_DEBUG="$APP/logs/analyst-reg-debug.log"
    mkdir -p "$(dirname "$REG_DEBUG")" 2>/dev/null || true
    {
      echo "[$STAMP] (jcode) pass-2 rc=$REG_RC prompt_bytes=$(wc -c < "$REG_PROMPT_FILE" 2>/dev/null) msg_bytes=$(wc -c < "$REG_MSG" 2>/dev/null || echo 0)"
      tail -c 4000 "$WORK/ev2.ndjson.err" 2>/dev/null
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
python3 - "$OUT_DIRECTIVE" "$reg_written" <<'PY' 2>/dev/null || true
import sys
p,rw=sys.argv[1],sys.argv[2]
t=open(p,encoding="utf-8").read().replace("registry-write: PENDING",f"registry-write: {rw}",1)
open(p,"w",encoding="utf-8").write(t)
PY

# --- PASS 3: deterministic directive-promotion gate (unchanged — no model call) ---
PROMOTE_SCRIPT="$APP/scripts/analyst/promote_directive.py"
promotion_result="skipped (promote_directive.py not found)"
if [ -f "$PROMOTE_SCRIPT" ]; then
    promotion_result="$(python3 "$PROMOTE_SCRIPT" "$OUT_DIRECTIVE" 2>&1 || echo "BLOCKED: promote_directive.py errored")"
fi
log "[$STAMP] PROMOTION (narrow v1): $promotion_result"

echo "Opportunity Analyst (jcode) run complete ($STAMP) — registry: $reg_written — promotion: $promotion_result."
