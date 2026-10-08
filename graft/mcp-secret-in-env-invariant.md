---
name: MCP secret-in-env invariant
slug: mcp-secret-in-env-invariant
type: concept
sources:
  - path: tests/test_jcode_mcp_config.sh
    hash: 3a26837a4685e40b45e3e8593459a69680a7bc6cc7e839f4ceb986c570a27025
  - path: tests/test_mcp_key_fallback.sh
    hash: 21c4be05f1922a08fa185aaa94f73941a785d5f380b7770431bdee7bf78115d6
sources_digest: bb7a46e749bf5cf188237332a19c925be341fc7e8c0a5fb8d47959b9490018b8
links:
  - to: mcp-configuration-and-manifest-sync
    relation: part_of
    description: Enforced by jcode-mcp-config.py and .mcp.json
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Secret values must never appear in process argv where ps could expose them; they live in the server spec's env block with the literal ${VAR} placeholder in argv. --print masks both argv header values and env values. The Keychain fallback (via the security binary) fires on macOS when a placeholder or unset variable is seen, but never inside the container where security does not exist. Context7 uses a stdio server reading CONTEXT7_API_KEY from the environment for the same reason.

## Related

- part of [[mcp-configuration-and-manifest-sync]] — Enforced by jcode-mcp-config.py and .mcp.json
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
