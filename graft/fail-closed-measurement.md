---
name: Fail-Closed Measurement
slug: fail-closed-measurement
type: concept
sources:
  - path: tests/test_ccusage_failclosed.sh
    hash: 366b96bee74416db05cc9752919b04304a49f5121d5802920a26641b196ef706
  - path: tests/test_jcode_mcp_config.sh
    hash: d6e5f312040010b657623eed1bd3a7b2b30bdd004870c9dc69e0d63b4d4a5d33
  - path: tests/test_mcp_probe.sh
    hash: 07482a8311b81667003a304c3741feed20e311f1e28263a5bb3bcc5599e962ce
  - path: tests/test_send_gate.sh
    hash: 4d0f03bd1b3e73a289e87cf0a56b25499b131e48fac01098b3f1d81755cb190d
sources_digest: a213e8e93bad22b3b05eebae58e00731948a5d2e61ac57a8881e06123bbeec37
links:
  - to: budget-spend-accounting
    relation: implements
    description: ccusage fail-closed latching and cache preservation.
  - to: ops-scripts
    relation: implements
    description: send-gate refuses on any unknown or error.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

A cross-cutting invariant: any measurement (ccusage spend, budget gates, MCP probes, send-gate policy) must fail closed on degraded/unknown input rather than silently proceeding. Degraded reads never lower a same-period prior observation and never overwrite the cache.

## Related

- implements [[budget-spend-accounting]] — ccusage fail-closed latching and cache preservation.
- implements [[ops-scripts]] — send-gate refuses on any unknown or error.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
