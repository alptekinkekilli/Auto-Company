---
name: Autonomous Loop
slug: autonomous-loop
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 376e5c5d4935009b140ead228b3ca323f3084a991e38f8961a9a9b045cf54ddb
sources_digest: 7454b13d037f0452d6e70bc9cfe60936ccc83ecee56b7661a84c43c98821179c
links:
  - to: codex-final-text
    relation: uses
    description: Extracts final text from codex exec --json event stream.
  - to: container-entrypoint
    relation: part_of
    description: Launched as background process by the entrypoint.
  - to: directive-writer
    relation: uses
    description: Writes/reads human-directive.md through the sole writer.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

24/7 orchestration loop running fresh Claude/Codex/jcode CLI sessions, using consensus.md as cross-cycle relay baton and assembling prompts from PROMPT.md + PROJECT_EVALUATION_FRAMEWORK.md. Anchored provider error signatures for usage/auth detection (never transcript prose); hard-coded tool denylist serving both safety and context budget (~540 tokens/turn saved per denied tool). Four-gate budget model (per-engine 5h, daily, weekly) fed by idempotent spend-total.log keyed on run_id; Codex metered by cycle count since it returns no USD cost. Tier ladder round-robins model/effort; circuit breaker with cooldown; ERR trap with set -E records silent set -e deaths.

## Related

- uses [[codex-final-text]] — Extracts final text from codex exec --json event stream.
- part of [[container-entrypoint]] — Launched as background process by the entrypoint.
- uses [[directive-writer]] — Writes/reads human-directive.md through the sole writer.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
