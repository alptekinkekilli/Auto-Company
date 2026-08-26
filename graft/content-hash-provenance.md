---
name: Content-Hash Provenance
slug: content-hash-provenance
type: concept
sources:
  - path: projects/_archive/snapog/src/og/render.ts
    hash: c74a09fcf98afae74090c3b72b8b4c7f84252e7f0aca090d1418352cd48d8094
  - path: scripts/core/decision_text_hash.py
    hash: 790b22fa08940d8d4c5418ec441c98f9d119b33eb718b7cfde81c01c71d94922
sources_digest: 1e628f4874fb1669c237c51ce666b97d3554f7d0dff92b36395cd37d8b0c4df8
links:
  - to: bridge-leak-scanner
    relation: uses
    description: Canonical hash feeds the value-sensitive leak scanner's evidence fields.
generator:
  version: 1
covers:
  - symbol: generateOGImage
    kind: function
    at: 'projects/_archive/snapog/src/og/render.ts:L11-L23'
  - symbol: buildCacheKey
    kind: function
    at: 'projects/_archive/snapog/src/og/render.ts:L26-L37'
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

Cross-cutting invariant that evidence hashes must be produced by a single canonical implementation to be comparable. decision_text_hash.py normalizes KİK decision HTML (decode, drop script/style, replace tags with single space, unescape entities after tag removal, collapse whitespace) because raw ASP.NET HTML varies by client. A hash produced any other way is not comparable and must not be written to the bridge — lesson from a 2026-07-29 underdetermined-spec incident. Also reflected in buildCacheKey's sorted-key SHA-256 for OG images.

## Related

- uses [[bridge-leak-scanner]] — Canonical hash feeds the value-sensitive leak scanner's evidence fields.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
