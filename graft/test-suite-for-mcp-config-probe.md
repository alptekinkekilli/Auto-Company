---
name: Test suite for MCP config & probe
slug: test-suite-for-mcp-config-probe
type: system
sources:
  - path: tests/fixtures/mock_mcp_server.py
    hash: e5124ccf90e18331b1e81557000a0bf0cc13e1fd7f0412250c5f37fb08e23021
  - path: tests/test_jcode_mcp_config.sh
    hash: 3a26837a4685e40b45e3e8593459a69680a7bc6cc7e839f4ceb986c570a27025
  - path: tests/test_mcp_config_manifest_sync.sh
    hash: 372a198973bc97e73dd00c1acafe2fe458887504be2f5ef9849242d6549c1112
  - path: tests/test_mcp_key_fallback.sh
    hash: 21c4be05f1922a08fa185aaa94f73941a785d5f380b7770431bdee7bf78115d6
  - path: tests/test_mcp_probe.sh
    hash: 07482a8311b81667003a304c3741feed20e311f1e28263a5bb3bcc5599e962ce
sources_digest: 95f75b25463a13b61ac2e2137f4221b7c2a81c9a9422a2ec1cfe820e9ff6a39e
links:
  - to: mcp-config-key-handling
    relation: validates
    description: >-
      Pins the generator's env-not-argv invariant, manifest sync, and probe
      readcheck requirements.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Bash tests validating the MCP config generator, probe, and key fallback behavior: secrets stay in env not argv, config/manifest sync prevents boot crash-loops, the probe's readcheck requirements, and the Keychain fallback firing on macOS but never in the container. Uses a mock stdio MCP server fixture for deterministic probing.

## Related

- validates [[mcp-config-key-handling]] — Pins the generator's env-not-argv invariant, manifest sync, and probe readcheck requirements.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
