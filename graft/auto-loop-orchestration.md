---
name: Auto-loop orchestration
slug: auto-loop-orchestration
type: concept
sources:
  - path: scripts/linux/noop-action.sh
    hash: 0f0aaa7c6c79e6c7844c7528a253084811b9a9b7277f557a1a60a8011347f4d9
  - path: scripts/linux/status-linux.sh
    hash: 1dc4a455fe8ffdd5e1696608d50d02311afd701906d80ee26d5708374d3947d8
  - path: scripts/macos/install-daemon.sh
    hash: 21f1e9576d7552530f20812f04232c75a2dadb4a7f5e3819045a35dec10037e9
  - path: scripts/macos/status-mac.sh
    hash: ba8bc08141ca80245bea6ccb35984221942d6a855ce856e5a492a38c4c151418
sources_digest: f255c43465d62dbf3f2557bb92ba24462856a6cb2e41ab0f71ef970cddecdb31
links:
  - to: final-text-extractors
    relation: uses
    description: auto-loop.sh calls these to extract final answers from engine streams.
  - to: loop-lifecycle-and-monitoring
    relation: part_of
    description: These scripts manage and observe the auto-loop process.
  - to: mcp-config-generation-and-probe
    relation: uses
    description: Boot probe gates loop startup on MCP health.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The central background loop (scripts/core/auto-loop.sh) that runs cycles, writes state to .auto-loop-state, PID to .auto-loop.pid, and logs to logs/auto-loop.log. It is the consumer of final-text extractors, MCP probe gates, and the producer of cycle-ndjson logs and turn-audit data consumed by many watchers. Platform-specific daemon install (macOS launchd with KeepAlive tied to pause flag) and container status reporting (Linux) adapt the same loop to both runtimes.

## Related

- uses [[final-text-extractors]] — auto-loop.sh calls these to extract final answers from engine streams.
- part of [[loop-lifecycle-and-monitoring]] — These scripts manage and observe the auto-loop process.
- uses [[mcp-config-generation-and-probe]] — Boot probe gates loop startup on MCP health.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
