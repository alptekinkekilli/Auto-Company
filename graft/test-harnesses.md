---
name: Test harnesses
slug: test-harnesses
type: system
sources:
  - path: tests/test_active_window.sh
    hash: fcd17dad9794b155cb623d85a88dd74bf10c12961df71a37f446f030958135fd
  - path: tests/test_airtable_read.sh
    hash: f1c8fbb1b495e922c52d041bac7edbae8f100ab57606ebd987179783265325df
  - path: tests/test_airtable_write.sh
    hash: a51c25001935da566cca4a450cfc0906827eb332779f2b454b12d547b7a0e6e0
  - path: tests/test_analyst_engine.sh
    hash: 3f6fbcc1efd4568252ac5d138931953946575646f3cdd0edd9f2a3bbe325cf63
  - path: tests/test_auto_loop_ledger_guard.sh
    hash: 707a207723f0b5c371c39d0fbc5a14170b4c74bb9c893f550186797aebcf440f
  - path: tests/test_auto_loop_work_window.sh
    hash: 7bb4ebdcaef7c71820540195fab59c8c657ff11f525429105bb0376a30405369
  - path: tests/test_browse_extract.sh
    hash: 37b269657d3077acf85e81540cd0355f9e97b432f0e6e1d973c2dfc170a887a6
  - path: tests/test_budget_gates.sh
    hash: 8d96846319108d7f4c41477e346d7ae803743be23e0bc4ca6de30e9f117e99c9
  - path: tests/test_ccusage_failclosed.sh
    hash: 366b96bee74416db05cc9752919b04304a49f5121d5802920a26641b196ef706
  - path: tests/test_codex_spend_sources.sh
    hash: 38e285a908cfdba71566f50ec2429fed8dc40ccdaaf68886e24e27399bba5bef
  - path: tests/test_compact_anchor_sync.py
    hash: 1f6ccedb49c760b6902820e32ca23f00f80927518fff9288ab1273aca4711378
  - path: tests/test_compact_ritual_hardening.sh
    hash: 2d94865ee02e9d01b5770928d95abef8e3f9157576dc40326fb74e8a164408f9
  - path: tests/test_compact_yol.py
    hash: 707405adc7816737d22c7079fe2e3484cb6959a80f4b4323acb76f44d4074e49
  - path: tests/test_context7_check.sh
    hash: d4fc93cf6b456038f23e1e756019a7fa1b47a344b0385bc5cd3d3a5536834733
  - path: tests/test_cost_audit_tool_surface.py
    hash: 801b92c715ca95cef9c34ab863f87fa443c8abcc65ba03237a934f5aed78121a
  - path: tests/test_cost_model_hint.sh
    hash: c17d1daedaa46cd803aa562c933e2a0d75aa6f2a5f7e059fd47fa8961847f743
  - path: tests/test_cycle_counter.sh
    hash: ab58cfed1b942c55ff2422535c8904c0292904f40786afc3cb7a66774d635065
  - path: tests/test_cycle_metadata.sh
    hash: ed0597fda8cb7dd8c8f45b5dea353e18374e12a7f4b247afab630f455e708c2e
sources_digest: 918999711de69d05f3a02f12138ab89d62d763f135e738290ccfa170e0c28704
links:
  - to: airtable-read-wrapper
    relation: validates
    description: >-
      test_airtable_read.sh pins the query-shaping and scoping rules offline via
      --print-query.
  - to: airtable-write-guard
    relation: validates
    description: test_airtable_write.sh pins the guard's refusal rules offline.
  - to: auto-loop-harness
    relation: validates
    description: >-
      Extract and exercise auto-loop.sh functions to pin budget gates, cycle
      counter, work-window, and spend behavior.
  - to: compact-ritual
    relation: validates
    description: >-
      test_compact_* suites pin anchor strings, path resolution, and ritual
      hardening.
generator:
  version: 1
covers:
  - symbol: _load
    kind: function
    at: 'tests/test_compact_anchor_sync.py:L41-L45'
  - symbol: check
    kind: function
    at: 'tests/test_compact_anchor_sync.py:L48-L53'
  - symbol: test_hepsi_gecti
    kind: function
    at: 'tests/test_compact_anchor_sync.py:L88-L89'
  - symbol: check
    kind: function
    at: 'tests/test_compact_yol.py:L31-L36'
  - symbol: _load
    kind: function
    at: 'tests/test_compact_yol.py:L39-L43'
  - symbol: git
    kind: function
    at: 'tests/test_compact_yol.py:L46-L49'
  - symbol: yeni_repo
    kind: function
    at: 'tests/test_compact_yol.py:L52-L59'
  - symbol: temiz_env
    kind: function
    at: 'tests/test_compact_yol.py:L62-L63'
  - symbol: zaman_asimi
    kind: function
    at: 'tests/test_compact_yol.py:L120-L122'
  - symbol: git_yok
    kind: function
    at: 'tests/test_compact_yol.py:L124-L125'
  - symbol: test_hepsi_gecti
    kind: function
    at: 'tests/test_compact_yol.py:L163-L164'
  - symbol: ok
    kind: function
    at: 'tests/test_cost_audit_tool_surface.py:L24-L25'
  - symbol: 'no'
    kind: function
    at: 'tests/test_cost_audit_tool_surface.py:L28-L31'
---
<!-- context:generated:start -->
## Summary

The offline regression suites that validate the harness and ops scripts by extracting real functions via awk/sed and stubbing external binaries (date, ccusage, jcode, timeout, MCP gateway). They run under the same set -euo pipefail options as production so crash-loop bugs surface loudly, and use mktemp sandboxes so no real state is touched.

## Related

- validates [[airtable-read-wrapper]] — test_airtable_read.sh pins the query-shaping and scoping rules offline via --print-query.
- validates [[airtable-write-guard]] — test_airtable_write.sh pins the guard's refusal rules offline.
- validates [[auto-loop-harness]] — Extract and exercise auto-loop.sh functions to pin budget gates, cycle counter, work-window, and spend behavior.
- validates [[compact-ritual]] — test_compact_* suites pin anchor strings, path resolution, and ritual hardening.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
