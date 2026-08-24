---
name: Web research cost model
slug: web-research-cost-model
type: system
sources:
  - path: scripts/ops/web-research-cost.py
    hash: 24d7735b6dc6defa0f80e75aeee37a13a40d4df43e9b38539be02df6fe23cbf2
sources_digest: 976169f8b29d99a352d9d4f4c66e56549da87c6f434116f4dfa18807078391d7
links:
  - to: airtable-read-write-guards
    relation: validates
    description: >-
      Motivates the read-scoping guards by quantifying Airtable dump context
      cost.
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

web-research-cost.py measures the true cost of web research in agent cycles: each tool result is re-read on every subsequent turn, so cost scales with output size times remaining turns. Scores all tools, not just web ones, because pre-filtering hid the largest context source (Airtable dumps). Uses a conservative BYTES_PER_TOKEN of 3.5.

## Related

- validates [[airtable-read-write-guards]] — Motivates the read-scoping guards by quantifying Airtable dump context cost.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
