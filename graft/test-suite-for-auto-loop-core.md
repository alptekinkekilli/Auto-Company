---
name: Test suite for auto-loop core
slug: test-suite-for-auto-loop-core
type: system
sources:
  - path: tests/test_active_window.sh
    hash: fcd17dad9794b155cb623d85a88dd74bf10c12961df71a37f446f030958135fd
  - path: tests/test_budget_gates.sh
    hash: 8d96846319108d7f4c41477e346d7ae803743be23e0bc4ca6de30e9f117e99c9
  - path: tests/test_ccusage_failclosed.sh
    hash: 366b96bee74416db05cc9752919b04304a49f5121d5802920a26641b196ef706
  - path: tests/test_codex_spend_sources.sh
    hash: 38e285a908cfdba71566f50ec2429fed8dc40ccdaaf68886e24e27399bba5bef
  - path: tests/test_cycle_counter.sh
    hash: ab58cfed1b942c55ff2422535c8904c0292904f40786afc3cb7a66774d635065
  - path: tests/test_cycle_metadata.sh
    hash: ed0597fda8cb7dd8c8f45b5dea353e18374e12a7f4b247afab630f455e708c2e
  - path: tests/test_discretionary_budget.sh
    hash: 32b2f12385f1bf8cc0984fc89d1181074406a1726028d2705d2224759cf6de7e
  - path: tests/test_escalation.sh
    hash: 51d700c7d869599d1a6d48913b0097143e7b0c93a520123dd7cf3bb5c8c874fc
  - path: tests/test_idle_skip.sh
    hash: 13ce9f0b8801b94a1bc896bd2db53f2fc68c2984b45db8372050ca760e1edb53
  - path: tests/test_mixed_harness.sh
    hash: bd8a1f81df957e0bfdfacf44982a2274a58809d5f9bd8618c64c3efeecb868cc
sources_digest: a33e2fef1404d6dfab231469bea07640ada0bd9ad42b1c3d420caa35d7d88455
links:
  - to: auto-loop-core
    relation: validates
    description: >-
      Drives the shipping auto-loop.sh functions, not copies; any change to
      extraction patterns breaks the tests loudly.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The large family of bash test scripts that extract functions verbatim from auto-loop.sh via awk and drive them under the same set -euo pipefail conditions as production, stubbing date/ccusage/jcode/timeout to run offline and deterministically. Covers budget gates, ccusage fail-closed behavior, codex spend sources, cycle counter monotonicity, escalation one-shot consumption, idle skip, engine attribution, and window gating.

## Related

- validates [[auto-loop-core]] — Drives the shipping auto-loop.sh functions, not copies; any change to extraction patterns breaks the tests loudly.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
