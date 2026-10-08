---
name: cycle metadata extraction
slug: cycle-metadata-extraction
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 429ad6c9ab94694e7399685cf7b7f63d5d8c387141baef14d1adb065cdca6292
  - path: scripts/core/codex-final-text.py
    hash: 3bc904db8c553fb60846f122faadf8447d3fe045c99b4d47c906c67567c264e4
  - path: tests/test_cycle_metadata.sh
    hash: ed0597fda8cb7dd8c8f45b5dea353e18374e12a7f4b247afab630f455e708c2e
  - path: tests/test_mixed_harness.sh
    hash: bd8a1f81df957e0bfdfacf44982a2274a58809d5f9bd8618c64c3efeecb868cc
sources_digest: 5b5bcf39e830bbf26ff9dbe8871f6c93a1ea01ae0700854cffaeb2542561454d
links:
  - to: auto-loop-core-engine
    relation: part_of
    description: extract_cycle_metadata() lives in auto-loop.sh.
  - to: mixed-harness-attribution
    relation: implements
    description: >-
      Per-cycle metadata feeds the mixed-harness attribution of cost and
      harness.
generator:
  version: 1
covers:
  - symbol: final_text
    kind: function
    at: 'scripts/core/codex-final-text.py:L30-L47'
  - symbol: main
    kind: function
    at: 'scripts/core/codex-final-text.py:L50-L60'
---
<!-- context:generated:start -->
## Summary

extract_cycle_metadata() parses per-cycle CYCLE_TYPE/CYCLE_SUBTYPE/RESULT_TEXT from engine output without killing the loop (APP-240 regression: it previously killed the container when Codex was routed through alternation/fallback). The companion codex-final-text.py converts the Codex CLI JSONL event stream into clean summary text, treating non-JSON input as a fallback trigger (exit 1) and never leaking reasoning/thread metadata.

## Related

- part of [[auto-loop-core-engine]] — extract_cycle_metadata() lives in auto-loop.sh.
- implements [[mixed-harness-attribution]] — Per-cycle metadata feeds the mixed-harness attribution of cost and harness.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
