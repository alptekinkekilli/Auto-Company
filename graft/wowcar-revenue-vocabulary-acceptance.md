---
name: wowcar revenue vocabulary acceptance
slug: wowcar-revenue-vocabulary-acceptance
type: file
sources:
  - path: tests/test_wowcar_revenue_vocabulary_acceptance.sh
    hash: 2d2ccfe9406d4effbc4872168e5d1f2a48f41842d8ac28397be5a2809dd28083
sources_digest: a14e4fe2b5a8ce01c35ef2cd4572b470cf93c226c80dce76da1245e3991423f6
links: []
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

scripts/ops/wowcar-revenue-vocabulary-acceptance.py checks that the candidate vocabulary (fixed to projects/wowcar/generator-source/kod) either remains unchanged or contains exactly 14 anchor terms, with a thin bash harness enforcing strict set -euo pipefail and an absolute report path. The mode must be exactly 'unchanged' or '14-anchor'.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
