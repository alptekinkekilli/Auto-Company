---
name: Operator escalation & routing
slug: operator-escalation-routing
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
  - path: scripts/ops/operator-action-router.py
    hash: 25fd8206f44d0baa7b87a910d0d1846fe5ef1b155289d1a769994aff6817587e
sources_digest: cef7b73431ce29966d515c5cda567005e2015c6066bf20774c2697c21e8b8c3e
links:
  - to: auto-loop-core-auto-loop-sh
    relation: part_of
    description: apply_cycle_escalation and _consume_escalation live in auto-loop.sh.
generator:
  version: 1
covers:
  - symbol: _now
    kind: function
    at: 'scripts/ops/operator-action-router.py:L78-L79'
  - symbol: read_hold
    kind: function
    at: 'scripts/ops/operator-action-router.py:L82-L102'
  - symbol: read_opreqs
    kind: function
    at: 'scripts/ops/operator-action-router.py:L105-L118'
  - symbol: read_directive
    kind: function
    at: 'scripts/ops/operator-action-router.py:L121-L134'
  - symbol: collect_items
    kind: function
    at: 'scripts/ops/operator-action-router.py:L137-L174'
  - symbol: render
    kind: function
    at: 'scripts/ops/operator-action-router.py:L177-L183'
  - symbol: set_hash
    kind: function
    at: 'scripts/ops/operator-action-router.py:L186-L189'
  - symbol: should_notify
    kind: function
    at: 'scripts/ops/operator-action-router.py:L192-L207'
  - symbol: load_state
    kind: function
    at: 'scripts/ops/operator-action-router.py:L210-L214'
  - symbol: write_state
    kind: function
    at: 'scripts/ops/operator-action-router.py:L217-L225'
  - symbol: clear_state
    kind: function
    at: 'scripts/ops/operator-action-router.py:L228-L232'
  - symbol: notify
    kind: function
    at: 'scripts/ops/operator-action-router.py:L235-L251'
  - symbol: main
    kind: function
    at: 'scripts/ops/operator-action-router.py:L254-L296'
---
<!-- context:generated:start -->
## Summary

One-shot operator escalation (APP-238): consumed exactly once, refusal leaves it ARMED. operator-action-router.py prioritizes hold > opreq > directive with staleness floors and dedup. operator_request_notify.py maintains the OPREQ ledger.

## Related

- part of [[auto-loop-core-auto-loop-sh]] — apply_cycle_escalation and _consume_escalation live in auto-loop.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
