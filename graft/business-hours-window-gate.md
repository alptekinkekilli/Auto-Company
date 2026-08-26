---
name: Business-hours window gate
slug: business-hours-window-gate
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: bc00d41b28222e0836508c4e1674f4e8146364f9a8d8e3a35fcf4c4a3e67f1f6
  - path: tests/test_active_window.sh
    hash: fcd17dad9794b155cb623d85a88dd74bf10c12961df71a37f446f030958135fd
sources_digest: 19a7cc1eb5ebcbd190f5e6c74e386ef62dd989bfbf7b33d31915111a9a6e506f
links:
  - to: auto-loop-core-engine
    relation: implements
    description: The _window_active function
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The _window_active() gate that keeps the loop in off-hours polling, with fail-open behavior where any malformed or missing window config forces the gate to stay active so a typo never parks the company. Must run before select_cycle_engine and before the loop_count increment so off-hours ticks don't burn cycle numbers or trigger external calls.

## Related

- implements [[auto-loop-core-engine]] — The _window_active function
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
