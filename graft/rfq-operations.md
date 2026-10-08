---
name: RFQ operations
slug: rfq-operations
type: system
sources:
  - path: tests/test_rfq_reply_watch.sh
    hash: 67f49fb6296af24a61aa9a5b8bae530f3cb2db42d5ef68d6f6c2a5989d073cb0
  - path: tests/test_rfq_send.sh
    hash: da4d25d4be3529f89c4c62e9b7099278b95d98a4336a9762bfe6c01e31030a97
sources_digest: 04fc00bfe8af995d842d443d0b68027148782fd34708a6fef19a8b63227b558f
links:
  - to: send-gate
    relation: uses
    description: >-
      rfq-send.py is registered in prod-mechanism-guard.py alongside
      send-gate.py
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

rfq-send.py is the buyer-side RFQ sender with §15 sponsor-approval and _sponsor_ok, no G4 gate usage, an ANON_DENY anonymity denylist, and correct Airtable table IDs (RFQ table tblzcGP7kNfkmPDGJ, not the frozen tender table tbl1fZbNmolrEXAMy). rfq-reply-watch.py watches RFQ rows for replies and silence: replied rows reported exactly once and never marked silent, silence reported as an observation (not a verdict) with age, advisory (no writes), avoiding tender-seller language (İKN, Stage 2), with state persistence and --dry-run leaving no state file.

## Related

- uses [[send-gate]] — rfq-send.py is registered in prod-mechanism-guard.py alongside send-gate.py
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
