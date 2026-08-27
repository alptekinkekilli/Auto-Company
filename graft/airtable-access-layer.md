---
name: Airtable access layer
slug: airtable-access-layer
type: system
sources:
  - path: scripts/ops/airtable-read.py
    hash: 148f66145510c90e03256b7b37853122bcd892d51cba67f095ce700a0895e3e2
  - path: scripts/ops/airtable-write.py
    hash: 888d408c392193511145e11dfbe73841a6d7e3e743e396ab8c8fee8b9507ab7c
sources_digest: 43a42c7621b93d8e35ed7813326f7b761e954384d076a4d1b176afa770c1b952
links:
  - to: g4-identity-check
    relation: uses
    description: Pulls registry bridge records for identity-attribution verdicts.
  - to: registry-queue-watch
    relation: uses
    description: 'Reads the Registry Bridge, EKAP Bridge, and Ihale Outreach tables.'
  - to: reply-watch
    relation: uses
    description: Reads outreach records from the Ihale Outreach table.
generator:
  version: 1
covers:
  - symbol: Refusal
    kind: class
    at: 'scripts/ops/airtable-read.py:L68-L69'
  - symbol: load_env
    kind: function
    at: 'scripts/ops/airtable-read.py:L72-L92'
  - symbol: load_keychain
    kind: function
    at: 'scripts/ops/airtable-read.py:L95-L111'
  - symbol: build_params
    kind: function
    at: 'scripts/ops/airtable-read.py:L114-L173'
  - symbol: encode
    kind: function
    at: 'scripts/ops/airtable-read.py:L176-L183'
  - symbol: to_body
    kind: function
    at: 'scripts/ops/airtable-read.py:L186-L198'
  - symbol: request
    kind: function
    at: 'scripts/ops/airtable-read.py:L201-L217'
  - symbol: fetch
    kind: function
    at: 'scripts/ops/airtable-read.py:L220-L239'
  - symbol: clip
    kind: function
    at: 'scripts/ops/airtable-read.py:L242-L248'
  - symbol: main
    kind: function
    at: 'scripts/ops/airtable-read.py:L251-L343'
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

Scoped, auditable access to Airtable: airtable-read.py prevents cycles from pulling whole tables (which cost $2.41 in context re-reads) by refusing unscoped reads and always naming the fixing flag, while airtable-write.py provides a sanctioned single-record PATCH path with read-back verification, dry-run default, and guards against accidental data loss (--allow-clear, --replace for >300-char strings). Secrets come from logs/runtime.env or macOS Keychain, never argv.

## Related

- uses [[g4-identity-check]] — Pulls registry bridge records for identity-attribution verdicts.
- uses [[registry-queue-watch]] — Reads the Registry Bridge, EKAP Bridge, and Ihale Outreach tables.
- uses [[reply-watch]] — Reads outreach records from the Ihale Outreach table.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
