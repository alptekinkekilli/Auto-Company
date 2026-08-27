---
name: Loop Driver
slug: loop-driver
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
  - path: scripts/core/codex-final-text.py
    hash: 3bc904db8c553fb60846f122faadf8447d3fe045c99b4d47c906c67567c264e4
sources_digest: 9c7f69c3ab695cdfeb60af9d2cf604e2afa439aa980e0d9141de96a1ce39e8cb
links:
  - to: directive-writer
    relation: uses
    description: >-
      auto-loop.sh and the analyst runners call scripts/core/directive_writer.py
      for safe directive writes/restores.
  - to: opportunity-analyst
    relation: uses
    description: >-
      The analyst runners (opportunity-analyst.sh, opportunity-analyst-jcode.sh)
      are driven by the same loop harness and share its budget/ledger helpers.
generator:
  version: 1
covers:
  - symbol: final_text
    kind: function
    at: 'scripts/core/codex-final-text.py:L30-L47'
  - symbol: main
    kind: function
    at: 'scripts/core/codex-final-text.py:L50-L60'
---
<!-- context:generated:start -->
## Summary

The 24/7 autonomous driver that runs continuous work cycles via Claude CLI, Codex CLI, or the unified jcode harness, with each cycle reading memories/consensus.md as the cross-cycle relay baton and PROMPT.md as standing law. Enforces a four-gate budget model (per-engine 5h, daily, weekly hard gates), a circuit breaker, usage-limit detection, and a jcode tool denylist that doubles as a context-budget lever. Guardrail verification checks PROMPT.md itself rather than the assembled prompt because consensus.md is model-rewritten and could mask a deleted section.

## Related

- uses [[directive-writer]] — auto-loop.sh and the analyst runners call scripts/core/directive_writer.py for safe directive writes/restores.
- uses [[opportunity-analyst]] — The analyst runners (opportunity-analyst.sh, opportunity-analyst-jcode.sh) are driven by the same loop harness and share its budget/ledger helpers.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
