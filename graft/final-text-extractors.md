---
name: Final-text extractors
slug: final-text-extractors
type: system
sources:
  - path: scripts/core/codex-final-text.py
    hash: 3bc904db8c553fb60846f122faadf8447d3fe045c99b4d47c906c67567c264e4
  - path: scripts/core/jcode-final-text.py
    hash: 8913ac57b8ca910581f28286fbdfb665674ee1a1273a477b39f39d1b02bf4215
sources_digest: 8c86c687652a082aa409b4a8ba8ffb34c64122612918dfab6b3f4384e3425870
links: []
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

Two parallel extractors pulling the assistant's final answer from event streams because done.text is unreliable (truncates on tool-using runs). codex-final-text.py concatenates all agent_message item.completed events; jcode-final-text.py concatenates all text_delta payloads and returns whichever is longer of deltas vs done.text — a deliberate safety trade-off preferring concatenated deltas (may include pre-tool narration noise but never lose content). Both fail-soft on malformed lines and read with errors='replace'.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
