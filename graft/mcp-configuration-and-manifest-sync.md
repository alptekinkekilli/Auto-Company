---
name: MCP configuration and manifest sync
slug: mcp-configuration-and-manifest-sync
type: system
sources:
  - path: tests/test_jcode_mcp_config.sh
    hash: 3a26837a4685e40b45e3e8593459a69680a7bc6cc7e839f4ceb986c570a27025
  - path: tests/test_mcp_config_manifest_sync.sh
    hash: 372a198973bc97e73dd00c1acafe2fe458887504be2f5ef9849242d6549c1112
  - path: tests/test_mcp_key_fallback.sh
    hash: 21c4be05f1922a08fa185aaa94f73941a785d5f380b7770431bdee7bf78115d6
  - path: tests/test_mcp_probe.sh
    hash: 07482a8311b81667003a304c3741feed20e311f1e28263a5bb3bcc5599e962ce
sources_digest: 81e578683fe3be807e72c1f06d92408015601631b429cc15a49d88cdcdab06ca
links:
  - to: auto-loop-core-engine
    relation: configures
    description: >-
      JCODE_MCP_CONFIG_REQUIRED preflight list in auto-loop.sh must agree with
      the manifest
  - to: mcp-secret-in-env-invariant
    relation: implements
    description: 'jcode-mcp-config.py keeps secrets in env, not argv'
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The MCP server configuration (scripts/core/jcode-mcp-config.py, .mcp.json, jcode-mcp-manifest.json) must stay in sync to prevent boot crash-loops when the generated loop config's server set diverges from the manifest. Secrets are kept in the server spec's env block, never in process argv where ps could expose them; the Keychain fallback works on macOS but never fires inside the container where the security binary does not exist. The deterministic probe (jcode-mcp-probe.py) validates servers, destructive tools, denylist coverage, and readchecks against a mock stdio server.

## Related

- configures [[auto-loop-core-engine]] — JCODE_MCP_CONFIG_REQUIRED preflight list in auto-loop.sh must agree with the manifest
- implements [[mcp-secret-in-env-invariant]] — jcode-mcp-config.py keeps secrets in env, not argv
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
