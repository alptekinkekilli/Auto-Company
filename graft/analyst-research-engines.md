---
name: analyst & research engines
slug: analyst-research-engines
type: system
sources:
  - path: scripts/analyst/opportunity-analyst-jcode.sh
    hash: 69985d473943f6d5adc94f51728ad97490391d0f517750ce54c9b785931bf5d6
  - path: scripts/ops/web-research-cost.py
    hash: 24d7735b6dc6defa0f80e75aeee37a13a40d4df43e9b38539be02df6fe23cbf2
  - path: tests/test_analyst_engine.sh
    hash: 3f6fbcc1efd4568252ac5d138931953946575646f3cdd0edd9f2a3bbe325cf63
sources_digest: e0801813b32d490679b1fe088c16eb47ac015800556b500c6d3a3cb09f7bed9c
links:
  - to: auto-loop-core-loop
    relation: uses
    description: >-
      The analyst engine runs jcode cycles similar to the main loop's jcode
      path.
  - to: ops-scripts
    relation: part_of
    description: >-
      web-research-cost.py is an ops analysis script; the analyst engine is a
      separate script.
generator:
  version: 1
covers:
  - symbol: is_web
    kind: function
    at: 'scripts/ops/web-research-cost.py:L43-L44'
  - symbol: analyse
    kind: function
    at: 'scripts/ops/web-research-cost.py:L47-L76'
  - symbol: main
    kind: function
    at: 'scripts/ops/web-research-cost.py:L79-L161'
---
<!-- context:generated:start -->
## Summary

opportunity-analyst-jcode.sh runs the analyst jcode cycle with provider-specific env vars (JCODE_ANTHROPIC_REASONING_EFFORT vs JCODE_OPENAI_REASONING_EFFORT), fails closed naming the missing credential, dedupes done.session_id into the sessions log, and writes the report header naming jcode/claude and the model. web-research-cost.py measures true web-research cost by scoring every tool's output bytes × remaining turns (not just web tools, since Airtable dumps were the largest hidden context source).

## Related

- uses [[auto-loop-core-loop]] — The analyst engine runs jcode cycles similar to the main loop's jcode path.
- part of [[ops-scripts]] — web-research-cost.py is an ops analysis script; the analyst engine is a separate script.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
