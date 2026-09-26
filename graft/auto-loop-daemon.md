---
name: Auto Loop Daemon
slug: auto-loop-daemon
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: b3850b8050b576a46bfa19953ae0492889b603967275721a09344b9589552d56
sources_digest: 09399485c2e8e9c57d25cea9e3e3d4e9c22b720c86c8238a7c7a4b25e1fc5140
links:
  - to: cockpit-server
    relation: produces
    description: >-
      Writes the state files (spend-total.log, router-state,
      operator-usage.json) the server reads for status.
  - to: directive-writer
    relation: uses
    description: Consumes human-directive.md written through the deterministic writer.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

24/7 orchestration daemon running fresh Claude/Codex/jcode CLI sessions in cycles, using memories/consensus.md as the cross-cycle relay baton. Four-gate budget model (CLAUDE_5H, CODEX_5H, TOTAL_DAILY, TOTAL_WEEKLY) over notional USD. For jcode uses a tool DENYLIST (not allowlist) to save context tokens and block destructive MCP tools, verified against live tool sets at boot. check_usage_limit anchors to provider error signatures; codex_auth_failed requires both non-zero exit and an auth phrase. ERR trap with set -E, circuit breaker (MAX_CONSECUTIVE_ERRORS/COOLDOWN_SECONDS), and ROUTER_TIER_LADDER round-robin.

## Related

- produces [[cockpit-server]] — Writes the state files (spend-total.log, router-state, operator-usage.json) the server reads for status.
- uses [[directive-writer]] — Consumes human-directive.md written through the deterministic writer.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
