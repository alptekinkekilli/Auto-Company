---
name: kik-decision-read
slug: kik-decision-read
type: file
sources:
  - path: scripts/ops/kik-decision-read.py
    hash: 4f2060cbaaa784433de9720f1e9a3bfb3ba6c06cab00fae0efa0a426e5c926de
sources_digest: d0430e1b2184f3b5ab5ef2ec2df0217a8110eb3508d564651dace20265543677
links:
  - to: decision-text-hash
    relation: uses
    description: >-
      Dynamically imports decision_text_hash to compute the canonical hash for
      bridge comparability.
generator:
  version: 1
covers:
  - symbol: _hasher
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L45-L51'
  - symbol: fetch
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L54-L67'
  - symbol: text_of
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L70-L73'
  - symbol: first
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L76-L78'
  - symbol: field
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L81-L89'
  - symbol: read
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L92-L131'
  - symbol: main
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L134-L159'
---
<!-- context:generated:start -->
## Summary

Fetches Turkish public procurement (KİK) decision page in one call, returns compact digest: decision number/date, meeting/agenda, contracting authority, tender ref, complainant (distinguished from excluded firm), operative 'karar verildi' sentence, canonical content hash. curl with browser UA (urllib fails TLS on macOS), 3 retries. Exclusion sentences extracted only after dropping quoted legislation so quoted article never mistaken for real exclusion.

## Related

- uses [[decision-text-hash]] — Dynamically imports decision_text_hash to compute the canonical hash for bridge comparability.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
