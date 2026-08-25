# scripts/core/jcode-mcp-config.py · [[atomic-state-writes]] [[mcp-boot-config]] [[mcp-config-key-handling]] [[secret-handling]]

Generates jcode's stdio-only MCP config from the repo's .mcp.json, bridging http/sse servers through mcp-remote and refusing to write partial or stale configs so the loop never silently loses tools.

- expand · function · L82-L94 — Substitutes ${VAR} references from the environment, returning None if any referenced variable is unset so the caller can skip the server loudly.
- sub · function · L86-L91 — Replacement callback that resolves one ${VAR} match and records it as missing when the environment has no value.
- convert · function · L97-L148 — Rewrites one server spec into a jcode-compatible stdio form, passing stdio servers through and wrapping http/sse servers in an mcp-remote bridge while keeping secrets out of argv.
- main · function · L151-L258 — Orchestrates reading the source config, applying overrides, converting servers, and atomically writing the config plus a freshness stamp, refusing to write empty or partial results.
