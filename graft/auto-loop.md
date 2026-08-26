---
name: Auto Loop
slug: auto-loop
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: f3e965e3aed59b32903f95d8be2954d7b966aa422c82a10fa581359fd906bb0b
sources_digest: 37ab20fc08031b66afd3689d1156671eff37d4ad8b4d6b223063c5bb09234e8f
links:
  - to: container-entrypoint
    relation: part_of
    description: Launched by docker-entrypoint.sh.
  - to: directive-writer
    relation: uses
    description: Restores human-directive.md via directive_writer.py.
  - to: opportunity-analyst-jcode
    relation: uses
    description: >-
      Analyst Codex sessions are excluded from budget only when their thread IDs
      parse cleanly.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The 24/7 orchestration daemon running Claude/Codex CLI sessions in fresh cycles using memories/consensus.md as the relay baton. Env-var-tunable: engine selection, cycle timing, a four-gate budget model fed by an idempotent spend ledger, a quota-aware router, and an opt-in tier ladder. Supports legacy cli and jcode harnesses with a tool denylist. Key invariants: check_usage_limit anchors on provider error signatures only; codex_auth_failed requires both non-zero exit and an auth-rejection phrase; prompt_guardrails_intact verifies safety sections in PROMPT.md itself because consensus.md is model-rewritten and could self-satisfy an assembled-only check. Has an ERR trap with errtrace, a circuit breaker, a watchdog timeout, and fail-closed budget accounting.

## Related

- part of [[container-entrypoint]] — Launched by docker-entrypoint.sh.
- uses [[directive-writer]] — Restores human-directive.md via directive_writer.py.
- uses [[opportunity-analyst-jcode]] — Analyst Codex sessions are excluded from budget only when their thread IDs parse cleanly.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
