---
name: Analyst engine & g4 check
slug: analyst-engine-g4-check
type: system
sources:
  - path: scripts/analyst/opportunity-analyst-jcode.sh
    hash: 69985d473943f6d5adc94f51728ad97490391d0f517750ce54c9b785931bf5d6
  - path: scripts/ops/g4-check.py
    hash: 719fa86c0e307ef71bf0bce8f49e2baab2bb522aec732b784b39c8f2d788aba8
  - path: tests/test_analyst_engine.sh
    hash: 3f6fbcc1efd4568252ac5d138931953946575646f3cdd0edd9f2a3bbe325cf63
  - path: tests/test_g4_check.sh
    hash: 426129aa4d430db932523139037190cd1c5106394e917a10fc73e29b823bc4d2
sources_digest: 9202fe219b5b029ded74c8a18e875b26813d30c8174302e3ac0d859a6bb7e723
links:
  - to: state-snapshot-probe
    relation: produces
    description: >-
      The analyst report hash is delta-visible in the snapshot
      (OPREQ-INFRA-ANALYST-ROUTING-001 Option B)
generator:
  version: 1
covers:
  - symbol: load_key
    kind: function
    at: 'scripts/ops/g4-check.py:L71-L89'
  - symbol: norm
    kind: function
    at: 'scripts/ops/g4-check.py:L92-L100'
  - symbol: address_anchor
    kind: function
    at: 'scripts/ops/g4-check.py:L103-L132'
  - symbol: registry_id_anchor
    kind: function
    at: 'scripts/ops/g4-check.py:L135-L164'
  - symbol: field
    kind: function
    at: 'scripts/ops/g4-check.py:L167-L169'
  - symbol: domains_in
    kind: function
    at: 'scripts/ops/g4-check.py:L172-L180'
  - symbol: air_get
    kind: function
    at: 'scripts/ops/g4-check.py:L183-L187'
  - symbol: air_list
    kind: function
    at: 'scripts/ops/g4-check.py:L190-L195'
  - symbol: site_evidence
    kind: function
    at: 'scripts/ops/g4-check.py:L198-L217'
  - symbol: judge
    kind: function
    at: 'scripts/ops/g4-check.py:L220-L287'
  - symbol: main
    kind: function
    at: 'scripts/ops/g4-check.py:L290-L337'
---
<!-- context:generated:start -->
## Summary

The opportunity-analyst engine that runs jcode cycles to produce the auditor report, plus the g4-check decision logic for matching register addresses against website addresses (Turkish dotted/dotless İ-ı folding, coincidence guard, context-dependent number matching).

## Related

- produces [[state-snapshot-probe]] — The analyst report hash is delta-visible in the snapshot (OPREQ-INFRA-ANALYST-ROUTING-001 Option B)
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
