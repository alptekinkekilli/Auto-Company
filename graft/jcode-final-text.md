---
name: jcode-final-text
slug: jcode-final-text
type: file
sources:
  - path: scripts/core/jcode-final-text.py
    hash: 8913ac57b8ca910581f28286fbdfb665674ee1a1273a477b39f39d1b02bf4215
sources_digest: 9dc3ddfffd81c401c2cc3324637e4092609c9fb0d51531d90a91eaeb486df9c8
links: []
generator:
  version: 1
covers:
  - symbol: final_text
    kind: function
    at: 'scripts/core/jcode-final-text.py:L30-L48'
  - symbol: main
    kind: function
    at: 'scripts/core/jcode-final-text.py:L51-L61'
---
<!-- context:generated:start -->
## Summary

Extracts complete assistant response from jcode ndjson stream. Concatenates all text_delta payloads and compares with done.text, returning the longer — done.text can silently truncate to the final block on tool-using runs. Exits 0 non-empty, 1 empty, 2 usage/read error.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
