---
name: operator-action-router
slug: operator-action-router
type: file
sources:
  - path: scripts/ops/operator-action-router.py
    hash: 25fd8206f44d0baa7b87a910d0d1846fe5ef1b155289d1a769994aff6817587e
sources_digest: 0630049afb5a60689dd7ae19e5af7d3257975de56f3e2aac81ea6b433cddc8ee
links:
  - to: telegram-notify
    relation: uses
    description: Sends the digest via the shared Telegram script.
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

Telegram firehose digest consolidating operator's actionable items into one 'what needs YOU' message. Covers only locally-truthful signals: LOOP_HOLD latch, open OPREQ entries, PENDING directive past floor age. Hashes open set's stable identity into state file, speaks only when set changes or ROUTER_REPEAT_HOURS elapses. Excludes Airtable-backed queues and Sentry liveness (need network/outside container). Advisory-only, never writes to Airtable/Linear/directive.

## Related

- uses [[telegram-notify]] — Sends the digest via the shared Telegram script.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
