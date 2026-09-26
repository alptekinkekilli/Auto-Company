---
name: Airtable write guard
slug: airtable-write-guard
type: system
sources:
  - path: scripts/ops/airtable-write.py
    hash: 888d408c392193511145e11dfbe73841a6d7e3e743e396ab8c8fee8b9507ab7c
sources_digest: 32429546b94f064bb5d229ea57f778f80302c1cd70bbbb212bbb3537319c21b3
links:
  - to: rfq-send-pipeline
    relation: uses
    description: >-
      rfq-send.py's _mark_sent patches Airtable status through this guarded
      write path.
generator:
  version: 1
covers:
  - symbol: load_env
    kind: function
    at: 'scripts/ops/airtable-write.py:L46-L62'
  - symbol: load_keychain
    kind: function
    at: 'scripts/ops/airtable-write.py:L65-L80'
  - symbol: call
    kind: function
    at: 'scripts/ops/airtable-write.py:L83-L92'
  - symbol: guard
    kind: function
    at: 'scripts/ops/airtable-write.py:L98-L133'
  - symbol: show
    kind: function
    at: 'scripts/ops/airtable-write.py:L136-L142'
  - symbol: main
    kind: function
    at: 'scripts/ops/airtable-write.py:L145-L202'
---
<!-- context:generated:start -->
## Summary

The guard that validates single-record Airtable writes before they hit the API: unknown fields are refused unless --force, clearing a non-empty field requires --allow-clear, and substantial value replacement requires --replace while appends preserving old text are allowed. Extracted from main() specifically so refusals are testable offline.

## Related

- uses [[rfq-send-pipeline]] — rfq-send.py's _mark_sent patches Airtable status through this guarded write path.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
