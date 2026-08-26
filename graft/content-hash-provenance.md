---
name: Content-Hash Provenance
slug: content-hash-provenance
type: concept
sources:
  - path: scripts/core/decision_text_hash.py
    hash: 790b22fa08940d8d4c5418ec441c98f9d119b33eb718b7cfde81c01c71d94922
sources_digest: 837c6e521378bcf965cbfcc5891b481682400ecc60b202a8af12f5fc90600758
links:
  - to: bridge-leak-scanner
    relation: uses
    description: >-
      The scanner's public evidence fields like content_hash are the values this
      hash produces.
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

The canonical content-hash implementation for KİK decision pages, existing because raw HTML from the ASP.NET endpoint varies by client (User-Agent, __VIEWSTATE), making raw-byte hashes unreliable. The normalization pipeline is load-bearing at every step: decode UTF-8 with replacement, drop script/style, replace every remaining tag with a single space (so a<br>b stays a b), unescape HTML entities after tag removal, map NBSP to space, collapse whitespace. A hash produced any other way is not comparable and must not be written to the bridge — a lesson from a 2026-07-29 incident where an underdetermined spec caused a legitimate evidence quarantine.

## Related

- uses [[bridge-leak-scanner]] — The scanner's public evidence fields like content_hash are the values this hash produces.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
