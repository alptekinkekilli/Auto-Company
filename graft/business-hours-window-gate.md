---
name: Business-Hours Window Gate
slug: business-hours-window-gate
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 429ad6c9ab94694e7399685cf7b7f63d5d8c387141baef14d1adb065cdca6292
  - path: tests/test_active_window.sh
    hash: fcd17dad9794b155cb623d85a88dd74bf10c12961df71a37f446f030958135fd
sources_digest: 6b142502aa5946e46dddd9800380b879ea17de62933ca0bb5d10e73daaedeaaa
links:
  - to: auto-loop-harness-brakes-and-guards
    relation: part_of
    description: The window gate is a function inside auto-loop.sh
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The _window_active() gate extracted from auto-loop.sh that restricts autonomous outreach to configured business hours, with fail-open behavior so a malformed or missing window config never parks the company. It must run before select_cycle_engine and before the loop_count increment so off-hours ticks don't burn cycle numbers or trigger external calls, and off-hours polling defaults to 900 seconds with the transition logged once. Leading-zero hours (08/09) are an octal trap handled explicitly.

## Related

- part of [[auto-loop-harness-brakes-and-guards]] — The window gate is a function inside auto-loop.sh
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
