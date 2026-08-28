---
name: airtable-write
slug: airtable-write
type: file
sources:
  - path: scripts/ops/airtable-write.py
    hash: 888d408c392193511145e11dfbe73841a6d7e3e743e396ab8c8fee8b9507ab7c
sources_digest: 32429546b94f064bb5d229ea57f778f80302c1cd70bbbb212bbb3537319c21b3
links: []
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

Sanctioned auditable single-record Airtable write path replacing ad-hoc curl that leaked API keys. Reads row first, applies only specified fields, PATCH, read-back verify, exit non-zero on mismatch. Dry-run default (--apply required), --allow-clear for non-empty fields, --replace for >300-char strings. Secrets never in argv.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
