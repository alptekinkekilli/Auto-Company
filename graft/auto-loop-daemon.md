---
name: Auto Loop Daemon
slug: auto-loop-daemon
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: f3e965e3aed59b32903f95d8be2954d7b966aa422c82a10fa581359fd906bb0b
sources_digest: 37ab20fc08031b66afd3689d1156671eff37d4ad8b4d6b223063c5bb09234e8f
links:
  - to: container-entrypoint
    relation: part_of
    description: Launched as a background process by docker-entrypoint.sh.
  - to: directive-writer
    relation: uses
    description: >-
      Writes/restores human-directive.md through the single deterministic
      writer.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

24/7 orchestration daemon running Claude or Codex CLI sessions in fresh cycles that use memories/consensus.md as the relay baton. Env-tunable: engine selection, cycle timing, a four-gate budget model fed by an idempotent spend ledger, a quota-aware router, and an opt-in tier ladder. Supports legacy cli and jcode harnesses with a tool denylist. check_usage_limit anchors on provider error signatures only; codex_auth_failed requires both non-zero exit and an auth-rejection phrase because transcripts embed files that may quote '401 unauthorized'; prompt_guardrails_intact verifies safety sections exist in PROMPT.md itself since consensus.md is model-rewritten and could self-satisfy an assembled-only check. ERR trap with errtrace, circuit breaker, watchdog timeout, fail-closed budget accounting, and .gitignore protection.

## Related

- part of [[container-entrypoint]] — Launched as a background process by docker-entrypoint.sh.
- uses [[directive-writer]] — Writes/restores human-directive.md through the single deterministic writer.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
