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
      The content hash is written to the bridge and validated by the leak
      scanner's public-evidence handling.
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

The principle that a canonical, load-bearing hash must be produced by exactly one deterministic implementation, because raw bytes vary by client and any other hash is not comparable. decision_text_hash.py normalizes KİK decision HTML (decode, drop script/style, replace tags with a single space so a<br>b stays a b, unescape entities after tag removal, collapse whitespace) before hashing, because the ASP.NET endpoint varies by User-Agent and __VIEWSTATE. A 2026-07-29 incident where an underdetermined spec caused a legitimate evidence quarantine motivated making this file the single source of truth.

## Related

- uses [[bridge-leak-scanner]] — The content hash is written to the bridge and validated by the leak scanner's public-evidence handling.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
