---
name: refusal format
slug: refusal-format
type: concept
sources:
  - path: tests/test_refusal_format.sh
    hash: 11bf5e9869e2e573b4a897e4df84053e4f58d759d3073a9e058705482cc31ef5
sources_digest: fa1e567e86d3f6e094c9099b3b56d7e1bf0f9670855fc004d14a77f37673fd5b
links:
  - to: operator-request-notify
    relation: implements
    description: >-
      operator_request_notify.py consumes the refusal format and records REFUSED
      status
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The operator-decision panel writes refusals as a short bounded REFUSE head line followed by verbatim multi-line text. A line-anchored regex previously flattened multi-line reasoning into a single long line, breaking the parser. Numbered points must survive as separate lines; audit log records a single REFUSED entry with readable line length; second run is idempotent.

## Related

- implements [[operator-request-notify]] — operator_request_notify.py consumes the refusal format and records REFUSED status
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
