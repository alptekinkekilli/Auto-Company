---
name: auto-loop core
slug: auto-loop-core
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 376e5c5d4935009b140ead228b3ca323f3084a991e38f8961a9a9b045cf54ddb
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
  - path: tests/test_prompt_assembly.sh
    hash: 0cd8e397ee0db20d70eac066f7542b6dbabfec6bdd6d031cdc0e378da04876d6
  - path: tests/test_prompt_transport.sh
    hash: c5df34a0acc0d09b63a231df392960370ab146ceea135b5bcace427223300501
sources_digest: e5b215515c2b147ac24fa913c5736ab38c225b0ad0fa3d4341a8dbfa4a24ca57
links:
  - to: cockpit-dashboard
    relation: produces
    description: Writes auto-loop.log and spend ledgers that the dashboard parses.
  - to: mcp-config-key-management
    relation: uses
    description: Runs engine CLIs that consume the generated .mcp.json.
  - to: outreach-ops-scripts
    relation: uses
    description: auto-loop invokes the ops scripts to gate and audit sends.
  - to: set-e-and-list-lint
    relation: validates
    description: >-
      test_seteshape_lint.py scans auto-loop.sh for the fatal [ test ] && action
      pattern.
  - to: tier-ladder-tests
    relation: validates
    description: >-
      test_tier_ladder_daily.sh extracts and tests apply_tier_ladder in
      isolation.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

scripts/core/auto-loop.sh is the central orchestration loop that drives daily outreach cycles, including the APP-263 daily-budget tier ladder (apply_tier_ladder) that selects model tiers per engine from TOTAL_DAILY_BUDGET_USD and per-engine spend. It is the caller whose unguarded exit statuses matter: the set -e AND-list bug that caused APP-240.

## Related

- produces [[cockpit-dashboard]] — Writes auto-loop.log and spend ledgers that the dashboard parses.
- uses [[mcp-config-key-management]] — Runs engine CLIs that consume the generated .mcp.json.
- uses [[outreach-ops-scripts]] — auto-loop invokes the ops scripts to gate and audit sends.
- validates [[set-e-and-list-lint]] — test_seteshape_lint.py scans auto-loop.sh for the fatal [ test ] && action pattern.
- validates [[tier-ladder-tests]] — test_tier_ladder_daily.sh extracts and tests apply_tier_ladder in isolation.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
