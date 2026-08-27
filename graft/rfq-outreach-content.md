---
name: RFQ outreach content
slug: rfq-outreach-content
type: system
sources:
  - path: scripts/ops/rfq_template.py
    hash: b5c3940ff17fde2ec3ca4fc810008581235c87728e4c313c0a1351c1ef390eb7
sources_digest: ee209adfab4b5062be544ad95226a0ed2ad75166de1be4d8fce6415aa97832f7
links:
  - to: auto-company-loop-core
    relation: produces
    description: Provides the email body used by the protected rfq-send.py delivery path.
generator:
  version: 1
covers:
  - symbol: subject
    kind: function
    at: 'scripts/ops/rfq_template.py:L43-L44'
  - symbol: body
    kind: function
    at: 'scripts/ops/rfq_template.py:L47-L64'
---
<!-- context:generated:start -->
## Summary

Generates the email content for RFQ outreach, deliberately separating content from sending so text can be iterated without touching production safeguards. Exports a SCOPE dictionary of anonymous procurement needs across five categories and a SIGNATURE, avoiding any client name or strategic details to preserve anonymity.

## Related

- produces [[auto-company-loop-core]] — Provides the email body used by the protected rfq-send.py delivery path.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
