---
name: cycle-counter persistence
slug: cycle-counter-persistence
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 429ad6c9ab94694e7399685cf7b7f63d5d8c387141baef14d1adb065cdca6292
  - path: tests/test_cycle_counter.sh
    hash: ab58cfed1b942c55ff2422535c8904c0292904f40786afc3cb7a66774d635065
  - path: tests/test_tool_usage_audit.sh
    hash: 4bdf9378fc2af04ed89fc9559aa1fcc8520846c6847f13302f613ec896bfde6d
sources_digest: 7c68172efa47991baead6418246f7dc3f4ad87422da83399aeeeb097210bd80b
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: The counter init/persist logic lives inside auto-loop.sh.
  - to: tool-usage-audit
    relation: depends_on
    description: >-
      The audit re-audits rewritten cycle-0001.ndjson because the counter resets
      on container restart.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The cycle counter must be monotonic across redeploys and container restarts: it is seeded from a persisted CYCLE_COUNTER_FILE, self-heals to the highest cycle-NNNN log on disk when the file is missing, takes the max when both exist, and strips non-digits from corrupt values (falling back to 0). The seed block and persist line are extracted verbatim by tests so any drift breaks loudly.

## Related

- part of [[auto-loop-core-engine]] — The counter init/persist logic lives inside auto-loop.sh.
- depends on [[tool-usage-audit]] — The audit re-audits rewritten cycle-0001.ndjson because the counter resets on container restart.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
