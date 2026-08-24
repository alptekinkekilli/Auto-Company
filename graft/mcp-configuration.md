---
name: MCP Configuration
slug: mcp-configuration
type: system
sources:
  - path: tests/test_jcode_mcp_config.sh
    hash: d6e5f312040010b657623eed1bd3a7b2b30bdd004870c9dc69e0d63b4d4a5d33
  - path: tests/test_mcp_key_fallback.sh
    hash: 21c4be05f1922a08fa185aaa94f73941a785d5f380b7770431bdee7bf78115d6
sources_digest: 65e211f4830d9aa9e9ff86947017aaa949b226bf5dd1b691eb118d051bf52d05
links:
  - to: airtable-ops
    relation: configures
    description: airtable/linear/context7/browseros servers are defined here.
  - to: mcp-probe
    relation: produces
    description: The generated config is what the probe validates against the manifest.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The .mcp.json MCP server configuration and its generator (jcode-mcp-config.py) that wraps HTTP servers in the mcp-remote stdio bridge. Secrets never appear in argv (ps-readable) — literal ${VAR} placeholders ride in --header while real values live in the env block. Keychain fallback works on macOS but never fires inside the container.

## Related

- configures [[airtable-ops]] — airtable/linear/context7/browseros servers are defined here.
- produces [[mcp-probe]] — The generated config is what the probe validates against the manifest.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
