---
name: reply watch
slug: reply-watch
type: system
sources:
  - path: tests/test_reply_watch.sh
    hash: a1291856a346b22fd46c2d1179ae6602778674b7f930d53c4216e449e286b67f
sources_digest: 44d6035bf3543193845dd9112531189a1cc9a3122dcae16157ec5135207e5405
links: []
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

reply-watch.py classifies email replies, bounces, and silence for five real firms: replies reported once and never as silence, bounces flagged as delivery failures (explicitly 'SESSİZLİK DEĞİLDİR'), fresh sends stay quiet, old unanswered rows become 'silence' with age (72-hour threshold), a replied row is never also silent, silence phrased as an observation ('hüküm değil'), state persistence suppresses duplicate alerts, --dry-run writes no state, and a failure superseded by a later Sent (Rayelsis case) is not reported as a delivery problem. Uses lexicographically comparable ISO timestamps.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
