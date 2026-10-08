---
name: KİK decision content-hash (decision_text_hash)
slug: ki-k-decision-content-hash-decision-text-hash
type: file
sources:
  - path: scripts/core/decision_text_hash.py
    hash: 790b22fa08940d8d4c5418ec441c98f9d119b33eb718b7cfde81c01c71d94922
sources_digest: 837c6e521378bcf965cbfcc5891b481682400ecc60b202a8af12f5fc90600758
links:
  - to: content-hash-provenance
    relation: implements
    description: >-
      This is the canonical implementation of the content-hash provenance
      concept.
  - to: ki-k-decision-reader
    relation: implements
    description: >-
      kik-decision-read.py dynamically imports this via importlib to guarantee
      hash comparability with the bridge's recorded value.
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
---
<!-- context:generated:start -->
## Summary

Canonical content-hash implementation for KİK decision pages, existing because raw HTML from KararGoster.aspx varies by client (User-Agent, __VIEWSTATE). The normalization pipeline order is load-bearing at every step (drop script/style, replace tags with single space, unescape entities after tag removal, collapse whitespace); digest is first 16 hex of SHA-256 of normalized text plus char count. Deliberately the single source of truth — a hash produced any other way is not comparable and must not be written to the bridge, a lesson from a 2026-07-29 underdetermined-spec incident.

## Related

- implements [[content-hash-provenance]] — This is the canonical implementation of the content-hash provenance concept.
- implements [[ki-k-decision-reader]] — kik-decision-read.py dynamically imports this via importlib to guarantee hash comparability with the bridge's recorded value.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
