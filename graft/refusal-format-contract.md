---
name: refusal format contract
slug: refusal-format-contract
type: concept
sources:
  - path: tests/test_refusal_format.sh
    hash: 11bf5e9869e2e573b4a897e4df84053e4f58d759d3073a9e058705482cc31ef5
sources_digest: fa1e567e86d3f6e094c9099b3b56d7e1bf0f9670855fc004d14a77f37673fd5b
links:
  - to: dashboard-server
    relation: produces
    description: The format is produced by dashboard/server.py's operator-decision panel
  - to: operator-request-notification
    relation: validates
    description: >-
      operator_request_notify.py consumes the refusal format and records REFUSED
      status
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The operator-decision panel's refusal format must keep multi-line operator reasoning intact: a short head line followed by verbatim text, never flattened into a single long REFUSE line (a line-anchored regex previously broke the parser). The decision file retains at least 12 lines, the REFUSE head is a single bounded line, numbered points survive as separate lines, and operator_request_notify.py records a single REFUSED audit entry idempotently.

## Related

- produces [[dashboard-server]] — The format is produced by dashboard/server.py's operator-decision panel
- validates [[operator-request-notification]] — operator_request_notify.py consumes the refusal format and records REFUSED status
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
