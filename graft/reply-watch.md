---
name: reply watch
slug: reply-watch
type: file
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

reply-watch.py classifies email replies, bounces, and silence for outreach firms. Replies reported once and never as silence; bounces flagged as delivery failures (explicitly not silence); fresh sends stay quiet; old unanswered rows become silence with age; a replied row is never also silent. Silence alert phrased as observation ('hüküm değil'); state persistence suppresses duplicate alerts; --dry-run writes no state file; a failure superseded by a later Sent is not reported as a delivery problem. Uses lexicographically comparable ISO timestamps and a 72-hour silence threshold.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
