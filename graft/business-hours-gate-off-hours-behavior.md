---
name: Business-hours gate & off-hours behavior
slug: business-hours-gate-off-hours-behavior
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 30cc1c943819800a5516778d7d841255d14720019a6bce081cc5b2d730631e64
  - path: tests/test_active_window.sh
    hash: fcd17dad9794b155cb623d85a88dd74bf10c12961df71a37f446f030958135fd
sources_digest: ee02caca6b8424aa18275fd341992cad6ce2de13b98c50fccd8792bdcae38cde
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: >-
      _window_active() runs before select_cycle_engine and the loop_count
      increment.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The _window_active() gate restricts cycles to a business-hours window (default 07-15 UTC), with fail-open behavior so a malformed/missing config never parks the company, and an octal trap for leading-zero hours (08/09). Off-hours ticks must not burn cycle numbers or trigger external calls, and the transition is logged once via _offhours_logged.

## Related

- part of [[auto-loop-core-engine]] — _window_active() runs before select_cycle_engine and the loop_count increment.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
