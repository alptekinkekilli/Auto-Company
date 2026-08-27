---
name: Secret handling & ps-safety
slug: secret-handling-ps-safety
type: concept
sources:
  - path: scripts/core/jcode-mcp-config.py
    hash: 7e5496c29eae3646af4874f74f0d70e22230b762a74acdfb7e38e93197b41aca
  - path: scripts/ops/verify-mcp-keys.py
    hash: a35c1f35481876cedc5bb4cf0c7fd4eceaea1c85e57d3c28e87560b3f9f342db
  - path: tests/test_jcode_mcp_config.sh
    hash: 3a26837a4685e40b45e3e8593459a69680a7bc6cc7e839f4ceb986c570a27025
  - path: tests/test_mcp_key_fallback.sh
    hash: 21c4be05f1922a08fa185aaa94f73941a785d5f380b7770431bdee7bf78115d6
sources_digest: c73011dc45f8214aaa8bd30154b2039a634202986bd827468d3ceb2701bf6951
links:
  - to: mcp-configuration-probe
    relation: implements
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
  - symbol: loop_env
    kind: function
    at: 'scripts/ops/verify-mcp-keys.py:L39-L51'
  - symbol: main
    kind: function
    at: 'scripts/ops/verify-mcp-keys.py:L54-L75'
---
<!-- context:generated:start -->
## Summary

Secrets are never placed in process argv where ps could expose them; they live in env blocks or are read from env/runtime.env/Keychain. MCP config keeps ${VAR} placeholders in argv and real values in env; verify-mcp-keys reads /proc/<pid>/environ and never prints key values.

## Related

- implements [[mcp-configuration-probe]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
