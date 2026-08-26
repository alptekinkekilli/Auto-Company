---
name: Offline testability via awk extraction & stubbing
slug: offline-testability-via-awk-extraction-stubbing
type: concept
sources:
  - path: tests/test_active_window.sh
    hash: fcd17dad9794b155cb623d85a88dd74bf10c12961df71a37f446f030958135fd
  - path: tests/test_budget_gates.sh
    hash: 8d96846319108d7f4c41477e346d7ae803743be23e0bc4ca6de30e9f117e99c9
  - path: tests/test_ccusage_failclosed.sh
    hash: 366b96bee74416db05cc9752919b04304a49f5121d5802920a26641b196ef706
  - path: tests/test_escalation.sh
    hash: 51d700c7d869599d1a6d48913b0097143e7b0c93a520123dd7cf3bb5c8c874fc
  - path: tests/test_mcp_key_fallback.sh
    hash: 21c4be05f1922a08fa185aaa94f73941a785d5f380b7770431bdee7bf78115d6
  - path: tests/test_prompt_assembly.sh
    hash: 0cd8e397ee0db20d70eac066f7542b6dbabfec6bdd6d031cdc0e378da04876d6
  - path: tests/test_prompt_transport.sh
    hash: c5df34a0acc0d09b63a231df392960370ab146ceea135b5bcace427223300501
  - path: tests/test_send_gate.sh
    hash: 4d0f03bd1b3e73a289e87cf0a56b25499b131e48fac01098b3f1d81755cb190d
sources_digest: a54dcef8add7ccdf8a2ece7d3372884c1e474992fa94a6c04ef5b6df537ca9a0
links:
  - to: auto-loop-core-engine
    relation: validates
    description: These tests validate auto-loop.sh functions by extracting them via awk.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

A pervasive testing strategy: extract real function bodies from auto-loop.sh via awk (so tests drive shipping code, not copies), stub external binaries (ccusage, jcode, timeout, security, date) and network calls (Airtable, MCP gateway), and pin time via BUDGET_NOW_OVERRIDE. This catches regressions like a stray quote that bash -n could not detect.

## Related

- validates [[auto-loop-core-engine]] — These tests validate auto-loop.sh functions by extracting them via awk.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
