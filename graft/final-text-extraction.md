---
name: Final-text extraction
slug: final-text-extraction
type: system
sources:
  - path: scripts/core/codex-final-text.py
    hash: 3bc904db8c553fb60846f122faadf8447d3fe045c99b4d47c906c67567c264e4
  - path: scripts/core/jcode-final-text.py
    hash: 8913ac57b8ca910581f28286fbdfb665674ee1a1273a477b39f39d1b02bf4215
sources_digest: 8c86c687652a082aa409b4a8ba8ffb34c64122612918dfab6b3f4384e3425870
links:
  - to: auto-loop-orchestration
    relation: uses
    description: >-
      Consumed by auto-loop.sh to obtain the assistant's answer from raw event
      streams.
generator:
  version: 1
covers:
  - symbol: final_text
    kind: function
    at: 'scripts/core/codex-final-text.py:L30-L47'
  - symbol: main
    kind: function
    at: 'scripts/core/codex-final-text.py:L50-L60'
  - symbol: final_text
    kind: function
    at: 'scripts/core/jcode-final-text.py:L30-L48'
  - symbol: main
    kind: function
    at: 'scripts/core/jcode-final-text.py:L51-L61'
---
<!-- context:generated:start -->
## Summary

Two parallel CLI utilities (codex and jcode variants) that extract the assistant's complete final text from NDJSON event streams, because done.text is unreliable on tool-using runs (can carry only the final block). Both concatenate all agent-message/delta payloads and prefer the longer of the two readings, following the principle that noise is never loss; they fail soft on malformed lines and tolerate schema changes.

## Related

- uses [[auto-loop-orchestration]] — Consumed by auto-loop.sh to obtain the assistant's answer from raw event streams.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
