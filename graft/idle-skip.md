---
name: Idle Skip
slug: idle-skip
type: system
sources:
  - path: tests/test_idle_skip.sh
    hash: 13ce9f0b8801b94a1bc896bd2db53f2fc68c2984b45db8372050ca760e1edb53
sources_digest: 62054a522d1d44a646c3044dc19f96a3436690842bf64fa02eb59498b202e615
links:
  - to: auto-loop-core
    relation: part_of
    description: >-
      _idle_skip_due extracted from auto-loop.sh; wiring verified inside the
      loop.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Idle-skip mechanism: _idle_skip_due gate plus idle-skip-note.py consensus note. First cycle of a UTC day is never skipped; kill switch read at call time; skip branch never calls a model and always runs the OPREQ ledger step before sleeping.

## Related

- part of [[auto-loop-core]] — _idle_skip_due extracted from auto-loop.sh; wiring verified inside the loop.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
