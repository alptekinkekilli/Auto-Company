#!/usr/bin/env bash
# The prompt assembly must SURVIVE its own guardrail text.
#
#   bash tests/test_prompt_assembly.sh
#
# Why this exists: Runtime Guardrail 9 was written with a raw ASCII double quote in it
# ("ben browser os …"). The guardrails live inside a double-quoted shell assignment, so the
# quote closed FULL_PROMPT early and bash tried to run the remainder as commands:
#
#     [ERR] rc=127 at line 2648: FULL_PROMPT="$PROMPT
#
# The loop died on its first cycle after the deploy, restarted, and — correctly — booted
# held, so production sat idle until someone looked. `bash -n` does NOT catch this: the file
# stays syntactically valid, it just means something else entirely.
#
# So: extract each FULL_PROMPT assignment from the script, evaluate it in a sandbox with the
# variables it references, and require both that it succeeds and that the guardrails are
# actually present in the result. Any future guardrail carrying a stray quote, backtick or
# $( fails here instead of in production.
set -uo pipefail
SCRIPT="${1:-scripts/core/auto-loop.sh}"
fail=0
ok()   { echo "  PASS $1"; }
bad()  { echo "  FAIL $1: $2"; fail=1; }

# Every branch that builds the prompt, by its opening line number.
# `mapfile` does not exist in the bash 3.2 that ships with macOS, and this suite has to run
# on the operator's laptop as well as in the container.
STARTS=$(grep -n '^ *FULL_PROMPT="[$]PROMPT' "$SCRIPT" | cut -d: -f1)
if [ -z "$STARTS" ]; then
    echo "FAIL: no FULL_PROMPT assignment found in $SCRIPT"; exit 1
fi
echo "prompt-assembly branches found: $(printf '%s\n' "$STARTS" | wc -l | tr -d ' ')"

for start in $STARTS; do
    end=$(awk -v s="$start" 'NR>=s && /^This is Cycle #\$loop_count\. Act decisively\."$/ {print NR; exit}' "$SCRIPT")
    if [ -z "$end" ]; then bad "branch@$start" "no closing line found"; continue; fi
    block=$(sed -n "${start},${end}p" "$SCRIPT")

    out=$(PROMPT="[prompt]" CONSENSUS="[consensus]" _discovery_line="[discovery]" loop_count=7 \
          bash -c "$block"$'\nprintf %s "$FULL_PROMPT"' 2>&1)
    rc=$?
    if [ "$rc" -ne 0 ]; then
        bad "branch@$start assembles" "rc=$rc — $(printf '%s' "$out" | head -2)"
        continue
    fi
    ok "branch@$start assembles"

    case "$out" in
        *"Runtime Guardrails"*) ok "branch@$start carries the guardrail block" ;;
        *) bad "branch@$start guardrails" "header missing from the assembled prompt" ;;
    esac
    # The numbered rules the company is actually held to. A rule that silently vanishes from
    # one branch is the failure mode this file also guards against.
    for rule in "OUTPUT HYGIENE" "TURN ECONOMY" "NARROW READS" "SITE EVIDENCE IS RENDERED"; do
        case "$out" in
            *"$rule"*) ok "branch@$start has rule: $rule" ;;
            *) bad "branch@$start rule" "$rule missing" ;;
        esac
    done
    case "$out" in
        *"This is Cycle #7."*) ok "branch@$start expands the cycle counter" ;;
        *) bad "branch@$start counter" "cycle number did not expand" ;;
    esac
done

if [ "$fail" -eq 0 ]; then echo "ALL PASS"; else echo "FAILURES"; fi
exit "$fail"
