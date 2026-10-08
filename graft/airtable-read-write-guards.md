---
name: Airtable read/write guards
slug: airtable-read-write-guards
type: system
sources:
  - path: tests/test_airtable_read.sh
    hash: f1c8fbb1b495e922c52d041bac7edbae8f100ab57606ebd987179783265325df
  - path: tests/test_airtable_write.sh
    hash: a51c25001935da566cca4a450cfc0906827eb332779f2b454b12d547b7a0e6e0
sources_digest: f36a07c38e3cd5b13c9c5c2ebd4240613fd28de5db52e96debd23170ea040e77
links:
  - to: outreach-eligibility-send-gate
    relation: uses
    description: >-
      send-gate.py and the RFQ sender read/write Airtable through these
      wrappers.
  - to: turn-economics-auditing
    relation: validates
    description: >-
      web-research-cost.py identified Airtable dumps as the largest context
      source, which the read-scoping wrapper addresses.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Context-cost and safety wrappers around Airtable access: airtable-read.py gates reads (refuses unscoped reads, caps --all-fields and --max-records at 200, pageSize at 100, builds OR(RECORD_ID()=...) formulas combined with --formula via AND), and airtable-write.py's guard validates single-record writes offline (unknown fields refused unless --force, clearing non-empty fields needs --allow-clear, substantial replacements need --replace while appends preserving old text are allowed). The read wrapper exists specifically to control context costs; the write guard was extracted from main() to be testable offline.

## Related

- uses [[outreach-eligibility-send-gate]] — send-gate.py and the RFQ sender read/write Airtable through these wrappers.
- validates [[turn-economics-auditing]] — web-research-cost.py identified Airtable dumps as the largest context source, which the read-scoping wrapper addresses.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
