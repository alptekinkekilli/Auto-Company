---
name: Fail-closed invariant
slug: fail-closed-invariant
type: concept
sources:
  - path: scripts/analyst/opportunity-analyst-jcode.sh
    hash: 8250db61c0a1031c088076e240616d2771868957339ff80f5e730388b06e5395
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
  - path: scripts/core/jcode-mcp-probe.py
    hash: 60fdd2addf2f53741d03e21002a00b6ee9d8895af1fae9746a51308e67672b67
  - path: scripts/ops/send-gate.py
    hash: 6acd746a20aff7267d711d61350ac14d8fa0c17a1af95341625aa2bfd9a63f92
  - path: scripts/ops/wowcar-revenue-vocabulary-acceptance.py
    hash: bc164912338c15636cc9183c9327a6f77fdab6aebc86e2747f197f01f824fab2
sources_digest: 75cc3fffdf424e59a6fb4f2d0c41a0e379bf781572b73c285722a528b5db5b2b
links: []
generator:
  version: 1
covers:
  - symbol: ServerError
    kind: class
    at: 'scripts/core/jcode-mcp-probe.py:L43-L44'
  - symbol: StdioClient
    kind: class
    at: 'scripts/core/jcode-mcp-probe.py:L47-L155'
  - symbol: __init__
    kind: method
    at: 'scripts/core/jcode-mcp-probe.py:L50-L65'
  - symbol: _remaining
    kind: method
    at: 'scripts/core/jcode-mcp-probe.py:L67-L71'
  - symbol: _send
    kind: method
    at: 'scripts/core/jcode-mcp-probe.py:L73-L79'
  - symbol: _read_msg
    kind: method
    at: 'scripts/core/jcode-mcp-probe.py:L81-L102'
  - symbol: request
    kind: method
    at: 'scripts/core/jcode-mcp-probe.py:L104-L116'
  - symbol: notify
    kind: method
    at: 'scripts/core/jcode-mcp-probe.py:L118-L119'
  - symbol: initialize
    kind: method
    at: 'scripts/core/jcode-mcp-probe.py:L121-L127'
  - symbol: list_tools
    kind: method
    at: 'scripts/core/jcode-mcp-probe.py:L129-L137'
  - symbol: call_tool
    kind: method
    at: 'scripts/core/jcode-mcp-probe.py:L139-L140'
  - symbol: close
    kind: method
    at: 'scripts/core/jcode-mcp-probe.py:L142-L155'
  - symbol: probe_server
    kind: function
    at: 'scripts/core/jcode-mcp-probe.py:L158-L168'
  - symbol: judge_readcheck
    kind: function
    at: 'scripts/core/jcode-mcp-probe.py:L171-L186'
  - symbol: main
    kind: function
    at: 'scripts/core/jcode-mcp-probe.py:L189-L362'
  - symbol: phase_of
    kind: function
    at: 'scripts/ops/send-gate.py:L66-L91'
  - symbol: body_claims
    kind: function
    at: 'scripts/ops/send-gate.py:L94-L101'
  - symbol: load_key
    kind: function
    at: 'scripts/ops/send-gate.py:L104-L122'
  - symbol: air
    kind: function
    at: 'scripts/ops/send-gate.py:L125-L135'
  - symbol: sent_rows
    kind: function
    at: 'scripts/ops/send-gate.py:L138-L148'
  - symbol: logged_sends
    kind: function
    at: 'scripts/ops/send-gate.py:L154-L177'
  - symbol: counts
    kind: function
    at: 'scripts/ops/send-gate.py:L180-L198'
  - symbol: opted_out
    kind: function
    at: 'scripts/ops/send-gate.py:L201-L215'
  - symbol: body_leak_scan
    kind: function
    at: 'scripts/ops/send-gate.py:L236-L244'
  - symbol: g4_live
    kind: function
    at: 'scripts/ops/send-gate.py:L247-L309'
  - symbol: decide
    kind: function
    at: 'scripts/ops/send-gate.py:L312-L544'
  - symbol: main
    kind: function
    at: 'scripts/ops/send-gate.py:L547-L583'
  - symbol: AcceptanceFailure
    kind: class
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L383-L384'
  - symbol: ConfigurationFailure
    kind: class
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L387-L388'
  - symbol: sha256_bytes
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L391-L392'
  - symbol: canonical_digest
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L395-L397'
  - symbol: require
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L400-L402'
  - symbol: config_require
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L405-L407'
  - symbol: find_repo
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L410-L413'
  - symbol: verify_runtime
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L416-L425'
  - symbol: baseline_records
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L428-L444'
  - symbol: verify_baseline
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L447-L450'
  - symbol: tree_manifest
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L453-L472'
  - symbol: inventory
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L475-L488'
  - symbol: apply_candidate_edits
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L491-L499'
  - symbol: check_source_boundary
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L502-L531'
  - symbol: run
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L534-L540'
  - symbol: require_success
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L543-L544'
  - symbol: numeric_probe
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L547-L551'
  - symbol: numeric_leaf_count
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L554-L560'
  - symbol: scrub_command
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L563-L564'
  - symbol: build_chain
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L567-L585'
  - symbol: scalar
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L588-L603'
  - symbol: workbook_structure
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L606-L634'
  - symbol: cached_cells
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L637-L655'
  - symbol: normalize_f4_pair
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L658-L669'
  - symbol: locate
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L659-L664'
  - symbol: compare_workbooks
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L672-L683'
  - symbol: normalize_stdout
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L686-L708'
  - symbol: compare_stdout
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L711-L730'
  - symbol: parse_args
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L733-L738'
  - symbol: control_identity
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L741-L758'
  - symbol: main
    kind: function
    at: 'scripts/ops/wowcar-revenue-vocabulary-acceptance.py:L761-L911'
---
<!-- context:generated:start -->
## Summary

Cross-cutting rule: any check that cannot complete is a REFUSE/NA, never an ALLOW/0. Appears in send-gate (REFUSE), budget gates (ccusage failure latches hold returning NA), MCP probe (server death fails), analyst runner (missing credential fails closed), and acceptance harness (AcceptanceFailure).
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
