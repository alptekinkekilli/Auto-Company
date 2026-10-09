---
name: MCP config generator
slug: mcp-config-generator
type: system
sources:
  - path: tests/test_jcode_mcp_config.sh
    hash: 3a26837a4685e40b45e3e8593459a69680a7bc6cc7e839f4ceb986c570a27025
  - path: tests/test_mcp_key_fallback.sh
    hash: 21c4be05f1922a08fa185aaa94f73941a785d5f380b7770431bdee7bf78115d6
sources_digest: bb7a46e749bf5cf188237332a19c925be341fc7e8c0a5fb8d47959b9490018b8
links:
  - to: mcp-config-sync-invariant
    relation: implements
    description: Generator output must match the manifest and preflight pins
  - to: mcp-probe
    relation: produces
    description: The probe validates the config the generator produces
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

scripts/core/jcode-mcp-config.py generates the .mcp.json server config, keeping secrets in the server spec's env block rather than argv (so ps cannot expose them), with ${VAR} placeholders in argv. It fails closed if a required server's variable is unset, and --print masks both argv and env values. The Keychain fallback works on macOS but must never fire inside the container where the security binary is absent.

## Related

- implements [[mcp-config-sync-invariant]] — Generator output must match the manifest and preflight pins
- produces [[mcp-probe]] — The probe validates the config the generator produces
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
