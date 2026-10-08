---
name: MCP config sync
slug: mcp-config-sync
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 429ad6c9ab94694e7399685cf7b7f63d5d8c387141baef14d1adb065cdca6292
  - path: scripts/core/jcode-mcp-config.py
    hash: 7e5496c29eae3646af4874f74f0d70e22230b762a74acdfb7e38e93197b41aca
  - path: tests/test_mcp_config_manifest_sync.sh
    hash: 372a198973bc97e73dd00c1acafe2fe458887504be2f5ef9849242d6549c1112
  - path: tests/test_mcp_probe.sh
    hash: 07482a8311b81667003a304c3741feed20e311f1e28263a5bb3bcc5599e962ce
sources_digest: 7338127ea7fc3e0ff47d960d37cd6d94ea07b19f2511b4f3cc3ef95467a6bc31
links:
  - to: auto-loop-core-engine
    relation: depends_on
    description: >-
      auto-loop.sh's preflight list must agree with the manifest and generated
      config.
  - to: mcp-probe
    relation: validates
    description: The probe checks the live server set against the manifest and readchecks.
generator:
  version: 1
covers:
  - symbol: expand
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L96-L108'
  - symbol: sub
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L100-L105'
  - symbol: convert
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L111-L162'
  - symbol: main
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L165-L276'
---
<!-- context:generated:start -->
## Summary

The generated loop MCP config's server set must stay in sync with the manifest (scripts/core/jcode-mcp-manifest.json) and the hardcoded JCODE_MCP_CONFIG_REQUIRED preflight list in auto-loop.sh; divergence causes a boot crash-loop. The OPREQ-A invariant requires airtable and linear to be absent from the loop config, and every non-exempt manifest server must have a corresponding readcheck.

## Related

- depends on [[auto-loop-core-engine]] — auto-loop.sh's preflight list must agree with the manifest and generated config.
- validates [[mcp-probe]] — The probe checks the live server set against the manifest and readchecks.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
