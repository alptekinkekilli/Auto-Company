---
name: Reply/silence classification
slug: reply-silence-classification
type: concept
sources:
  - path: scripts/ops/reply-watch.py
    hash: 110e009b20f709db9dda31e2e17af9fb061696a869901bd389dddedca9294070
  - path: tests/test_reply_watch.sh
    hash: a1291856a346b22fd46c2d1179ae6602778674b7f930d53c4216e449e286b67f
sources_digest: ce5714749921b9400cfaa17af0fe9932f3146e57178b31a75e3812be36b83d8e
links:
  - to: outreach-ops-scripts
    relation: part_of
    description: reply-watch.py is one of the ops scripts.
  - to: outreach-ops-test-suites
    relation: validates
    description: test_reply_watch.sh pins these classification invariants.
generator:
  version: 1
covers:
  - symbol: api_key
    kind: function
    at: 'scripts/ops/reply-watch.py:L46-L56'
  - symbol: fetch
    kind: function
    at: 'scripts/ops/reply-watch.py:L59-L74'
  - symbol: notify
    kind: function
    at: 'scripts/ops/reply-watch.py:L77-L91'
  - symbol: first_ts
    kind: function
    at: 'scripts/ops/reply-watch.py:L94-L99'
  - symbol: hours_since
    kind: function
    at: 'scripts/ops/reply-watch.py:L102-L112'
  - symbol: main
    kind: function
    at: 'scripts/ops/reply-watch.py:L115-L142'
  - symbol: classify
    kind: function
    at: 'scripts/ops/reply-watch.py:L145-L223'
---
<!-- context:generated:start -->
## Summary

reply-watch.py's invariants: a reply is reported once and never as silence, a replied row is never also silent, bounces are flagged as delivery failures (explicitly 'SESSİZLİK DEĞİLDİR'), fresh sends stay quiet, old unanswered rows become 'silence' with age, and the silence alert is phrased as an observation ('hüküm değil'). State persistence suppresses duplicate alerts on a second run, --dry-run writes no state file, and a failure superseded by a later Sent (the Rayelsis case) is not reported as a delivery problem. Uses lexicographically comparable ISO timestamps and a 72-hour silence threshold.

## Related

- part of [[outreach-ops-scripts]] — reply-watch.py is one of the ops scripts.
- validates [[outreach-ops-test-suites]] — test_reply_watch.sh pins these classification invariants.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
