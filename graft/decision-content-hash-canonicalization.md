---
name: Decision content-hash canonicalization
slug: decision-content-hash-canonicalization
type: system
sources:
  - path: scripts/core/decision_text_hash.py
    hash: 790b22fa08940d8d4c5418ec441c98f9d119b33eb718b7cfde81c01c71d94922
  - path: scripts/ops/kik-decision-read.py
    hash: 4f2060cbaaa784433de9720f1e9a3bfb3ba6c06cab00fae0efa0a426e5c926de
sources_digest: 29bce193d5c60bd9e7bf52e9c353d21de59f11e0b8c1f585378295f1c8433681
links:
  - to: engine-final-text-extraction
    relation: uses
    description: >-
      kik-decision-read.py dynamically imports decision_text_hash.py to
      guarantee hash comparability with the bridge.
generator:
  version: 1
covers:
  - symbol: normalize
    kind: function
    at: 'scripts/core/decision_text_hash.py:L54-L60'
  - symbol: digest
    kind: function
    at: 'scripts/core/decision_text_hash.py:L63-L65'
  - symbol: fetch
    kind: function
    at: 'scripts/core/decision_text_hash.py:L68-L96'
  - symbol: main
    kind: function
    at: 'scripts/core/decision_text_hash.py:L99-L112'
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

The single source of truth for hashing KİK decision pages, existing because raw HTML from the ASP.NET endpoint varies by client. A load-bearing normalization pipeline (drop scripts/styles, replace tags with single spaces, unescape entities after tag removal, collapse whitespace) feeds a SHA-256 digest; any hash produced another way is not comparable and must not be written to the bridge.

## Related

- uses [[engine-final-text-extraction]] — kik-decision-read.py dynamically imports decision_text_hash.py to guarantee hash comparability with the bridge.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
