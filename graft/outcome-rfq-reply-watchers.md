---
name: outcome & RFQ reply watchers
slug: outcome-rfq-reply-watchers
type: system
sources:
  - path: tests/test_reply_watch.sh
    hash: a1291856a346b22fd46c2d1179ae6602778674b7f930d53c4216e449e286b67f
  - path: tests/test_rfq_reply_watch.sh
    hash: 67f49fb6296af24a61aa9a5b8bae530f3cb2db42d5ef68d6f6c2a5989d073cb0
sources_digest: a480ba62577e4c1d6fdaf989bb40d82719827d70225a8166b73c7f8e51470a60
links: []
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

scripts/ops/reply-watch.py and rfq-reply-watch.py classify email/RFQ replies, bounces, and silence for real firms. They report replies exactly once and never as silence, flag bounces as delivery failures (explicitly 'SESSİZLİK DEĞİLDİR'), keep fresh sends quiet, phrase silence as observation not verdict, persist state to suppress duplicate alerts, and honor --dry-run (no state write). rfq-reply-watch targets the RFQ table (tblzcGP7kNfkmPDGJ) and avoids the tender table and tender-seller language.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
