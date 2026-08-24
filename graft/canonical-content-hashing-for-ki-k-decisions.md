---
name: Canonical content hashing for KİK decisions
slug: canonical-content-hashing-for-ki-k-decisions
type: system
sources:
  - path: scripts/core/decision_text_hash.py
    hash: 790b22fa08940d8d4c5418ec441c98f9d119b33eb718b7cfde81c01c71d94922
sources_digest: 837c6e521378bcf965cbfcc5891b481682400ecc60b202a8af12f5fc90600758
links: []
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

The single source of truth for content hashes of KİK decision pages, existing because raw HTML from the ASP.NET endpoint varies by client (User-Agent, __VIEWSTATE). Applies a load-bearing normalization pipeline (drop script/style, replace tags with a single space, unescape entities after tag removal, collapse whitespace) then SHA-256 truncated to 16 hex chars plus char count. A hash produced any other way is not comparable and must not be written to the bridge.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
