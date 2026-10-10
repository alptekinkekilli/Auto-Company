---
name: Engine Output Extraction
slug: engine-output-extraction
type: system
sources:
  - path: scripts/core/codex-final-text.py
    hash: 3bc904db8c553fb60846f122faadf8447d3fe045c99b4d47c906c67567c264e4
  - path: scripts/core/engine-usage-cost.py
    hash: 6a70e9d1375893c7269ea1e77d431f205006156b191366d90e588ad0485db344
  - path: scripts/core/jcode-final-text.py
    hash: 8913ac57b8ca910581f28286fbdfb665674ee1a1273a477b39f39d1b02bf4215
sources_digest: 9b15087206e6540f49099ead7360918eec85ea4e284419a14465be0ff80e8aac
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
  - symbol: _n
    kind: function
    at: 'scripts/core/engine-usage-cost.py:L75-L78'
  - symbol: cost_for
    kind: function
    at: 'scripts/core/engine-usage-cost.py:L81-L123'
  - symbol: main
    kind: function
    at: 'scripts/core/engine-usage-cost.py:L126-L204'
  - symbol: final_text
    kind: function
    at: 'scripts/core/jcode-final-text.py:L30-L48'
  - symbol: main
    kind: function
    at: 'scripts/core/jcode-final-text.py:L51-L61'
---
<!-- context:generated:start -->
## Summary

Utilities that extract the assistant's final text from CLI event streams, because the engines' own 'done' fields are unreliable. jcode-final-text.py concatenates all text_delta payloads and returns the longer of deltas vs done.text (a measured failure: a 31-event delta sequence produced a full answer while done.text held only its last paragraph). codex-final-text.py concatenates all item.completed agent_message events, ignoring reasoning/tool calls, with fail-soft behavior. engine-usage-cost.py converts token usage to notional USD via a hardcoded price table (summing all tokens events since done.usage undercounts multi-tool cycles), with conservative 5x fallback pricing for unknown models.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
