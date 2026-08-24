---
name: Test-by-extraction strategy
slug: test-by-extraction-strategy
type: concept
sources:
  - path: tests/test_budget_gates.sh
    hash: 8d96846319108d7f4c41477e346d7ae803743be23e0bc4ca6de30e9f117e99c9
  - path: tests/test_ccusage_failclosed.sh
    hash: 366b96bee74416db05cc9752919b04304a49f5121d5802920a26641b196ef706
  - path: tests/test_cycle_metadata.sh
    hash: 66a21f12ac379be58cda6db2e98c410b11104c0fc2c2d8c6efdffd422dcd3988
  - path: tests/test_escalation.sh
    hash: 51d700c7d869599d1a6d48913b0097143e7b0c93a520123dd7cf3bb5c8c874fc
  - path: tests/test_idle_skip.sh
    hash: 13ce9f0b8801b94a1bc896bd2db53f2fc68c2984b45db8372050ca760e1edb53
  - path: tests/test_mixed_harness.sh
    hash: bd8a1f81df957e0bfdfacf44982a2274a58809d5f9bd8618c64c3efeecb868cc
  - path: tests/test_prompt_assembly.sh
    hash: 0cd8e397ee0db20d70eac066f7542b6dbabfec6bdd6d031cdc0e378da04876d6
  - path: tests/test_prompt_transport.sh
    hash: c5df34a0acc0d09b63a231df392960370ab146ceea135b5bcace427223300501
  - path: tests/test_tier_ladder_daily.sh
    hash: d0bfb4ace48e1fa9665e17059be3f618b46fda0dcf432544a6bb16c07a3ed8db
sources_digest: 259da2b15bf78007f317d503e36cd91193a2bca26f3fb1acd35983be11c58886
links:
  - to: auto-loop-core-engine
    relation: validates
    description: Most extraction-based suites target auto-loop.sh functions.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The dominant testing convention: tests extract real function bodies from shipping scripts via awk/grep/sed and drive them in isolated sandboxes with stubbed binaries and pinned time, rather than reimplementing logic. This catches regressions in the actual shipped code (e.g., a stray quote caught twice before shipping) and keeps suites offline and deterministic.

## Related

- validates [[auto-loop-core-engine]] — Most extraction-based suites target auto-loop.sh functions.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
