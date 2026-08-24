---
name: Airtable access layer
slug: airtable-access-layer
type: system
sources:
  - path: scripts/ops/airtable-read.py
    hash: 148f66145510c90e03256b7b37853122bcd892d51cba67f095ce700a0895e3e2
  - path: scripts/ops/airtable-write.py
    hash: 888d408c392193511145e11dfbe73841a6d7e3e743e396ab8c8fee8b9507ab7c
  - path: scripts/ops/registry-queue-watch.py
    hash: 0ef6723d089c54ee8272050eb2776ce81af9de986e8f6dc15b065b7bbd913497
  - path: scripts/ops/reply-watch.py
    hash: 110e009b20f709db9dda31e2e17af9fb061696a869901bd389dddedca9294070
sources_digest: f0577feca01d1963e0dab3eaeab7489841b53cbe146e17d59057508418db773e
links:
  - to: operator-escalation-notification
    relation: uses
    description: >-
      reply-watch and registry-queue-watch read Airtable and notify via
      telegram-notify.sh.
  - to: outreach-eligibility-gate
    relation: uses
    description: send-gate reads Airtable rows through the same air() wrapper.
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
  - symbol: api_key
    kind: function
    at: 'scripts/ops/registry-queue-watch.py:L48-L58'
  - symbol: fetch
    kind: function
    at: 'scripts/ops/registry-queue-watch.py:L61-L77'
  - symbol: main
    kind: function
    at: 'scripts/ops/registry-queue-watch.py:L80-L215'
  - symbol: api_key
    kind: function
    at: 'scripts/ops/reply-watch.py:L46-L56'
  - symbol: fetch
    kind: function
    at: 'scripts/ops/reply-watch.py:L59-L74'
  - symbol: notify
    kind: function
    at: 'scripts/ops/reply-watch.py:L77-L91'
  - symbol: first_ts
    kind: function
    at: 'scripts/ops/reply-watch.py:L94-L99'
  - symbol: hours_since
    kind: function
    at: 'scripts/ops/reply-watch.py:L102-L112'
  - symbol: main
    kind: function
    at: 'scripts/ops/reply-watch.py:L115-L142'
  - symbol: classify
    kind: function
    at: 'scripts/ops/reply-watch.py:L145-L223'
---
<!-- context:generated:start -->
## Summary

Scoped, auditable access to Airtable: airtable-read refuses unscoped reads (whole-table pulls cost $2.41/cycle in context re-reads), airtable-write is a single-record PATCH with read-back verification and dry-run default, and the watchers (reply-watch, registry-queue-watch) read tables read-only. Secrets come from env, logs/runtime.env, or macOS Keychain — never argv.

## Related

- uses [[operator-escalation-notification]] — reply-watch and registry-queue-watch read Airtable and notify via telegram-notify.sh.
- uses [[outreach-eligibility-gate]] — send-gate reads Airtable rows through the same air() wrapper.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
