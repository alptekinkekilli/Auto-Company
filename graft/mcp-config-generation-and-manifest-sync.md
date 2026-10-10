---
name: MCP config generation and manifest sync
slug: mcp-config-generation-and-manifest-sync
type: system
sources:
  - path: tests/test_jcode_mcp_config.sh
    hash: 3a26837a4685e40b45e3e8593459a69680a7bc6cc7e839f4ceb986c570a27025
  - path: tests/test_mcp_config_manifest_sync.sh
    hash: 372a198973bc97e73dd00c1acafe2fe458887504be2f5ef9849242d6549c1112
  - path: tests/test_mcp_key_fallback.sh
    hash: 21c4be05f1922a08fa185aaa94f73941a785d5f380b7770431bdee7bf78115d6
sources_digest: 2d062c219f47066bd2e5c7d761a16c9c156291c1a70efad000d073a6b35bd07a
links:
  - to: auto-loop-core-engine
    relation: configures
    description: >-
      Generated loop config's server set must match the preflight list in
      auto-loop.sh
  - to: mcp-probe
    relation: uses
    description: The probe validates the generated config against the manifest
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

jcode-mcp-config.py generates MCP server config from .mcp.json, keeping secrets in the server spec's env block (never in argv where ps could expose them). A manifest (jcode-mcp-manifest.json) must stay in sync with the generated config and the JCODE_MCP_CONFIG_REQUIRED preflight list in auto-loop.sh; divergence causes a boot crash-loop. OPREQ-A invariant: airtable and linear are absent from the loop config. Keychain fallback works on macOS but must never fire inside the container where the security binary does not exist.

## Related

- configures [[auto-loop-core-engine]] — Generated loop config's server set must match the preflight list in auto-loop.sh
- uses [[mcp-probe]] — The probe validates the generated config against the manifest
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
