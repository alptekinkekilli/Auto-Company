---
name: Airtable Read/Write Wrappers
slug: airtable-read-write-wrappers
type: system
sources:
  - path: scripts/ops/airtable-read.py
    hash: 148f66145510c90e03256b7b37853122bcd892d51cba67f095ce700a0895e3e2
  - path: scripts/ops/airtable-write.py
    hash: 888d408c392193511145e11dfbe73841a6d7e3e743e396ab8c8fee8b9507ab7c
sources_digest: 43a42c7621b93d8e35ed7813326f7b761e954384d076a4d1b176afa770c1b952
links:
  - to: g4-identity-attribution
    relation: uses
    description: g4-check.py pulls registry bridge records via air_get/air_list.
  - to: operator-escalation-gate
    relation: uses
    description: >-
      registry-queue-watch.py and reply-watch.py read Airtable queues through
      the REST API.
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

Scoped, auditable wrappers around the Airtable REST API. airtable-read.py refuses unscoped reads (which cost $2.41 in context re-reads) and paginates with automatic POST /listRecords past a 15k-char URL threshold; airtable-write.py is dry-run by default, reads-then-PATCH-then-verifies, and requires explicit flags to clear or replace substantial content. Secrets come from runtime.env or macOS Keychain, never argv.

## Related

- uses [[g4-identity-attribution]] — g4-check.py pulls registry bridge records via air_get/air_list.
- uses [[operator-escalation-gate]] — registry-queue-watch.py and reply-watch.py read Airtable queues through the REST API.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
