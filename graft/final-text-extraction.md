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
  - to: auto-company-loop-core
    relation: produces
    description: >-
      Provides the plain final text the loop acts on, with exit 1 signaling
      fallback to raw content.
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

Two parallel CLI utilities that extract the assistant's final answer from an event stream (codex exec --json or jcode --ndjson), because the stream's own 'done' event can silently truncate the answer on tool-using runs. Both concatenate all message deltas and prefer the longer of concatenated deltas vs the done event's text, on the principle that noise is never loss.

## Related

- produces [[auto-company-loop-core]] — Provides the plain final text the loop acts on, with exit 1 signaling fallback to raw content.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
