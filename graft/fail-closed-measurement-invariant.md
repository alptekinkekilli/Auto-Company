---
name: Fail-closed measurement invariant
slug: fail-closed-measurement-invariant
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 332728052d5c8e3d8dbb64ca1d391062fc22c656cdb0a87d5e258b4f688d6103
  - path: scripts/ops/rfq-send.py
    hash: 09815061d704b6bd2034469e3bfe3dfac7417f25761ea9ae845be4c5367fd225
  - path: scripts/ops/send-gate.py
    hash: 6acd746a20aff7267d711d61350ac14d8fa0c17a1af95341625aa2bfd9a63f92
  - path: scripts/ops/verify-mcp-keys.py
    hash: a35c1f35481876cedc5bb4cf0c7fd4eceaea1c85e57d3c28e87560b3f9f342db
  - path: scripts/ops/wowcar-revenue-vocabulary-acceptance.py
    hash: bc164912338c15636cc9183c9327a6f77fdab6aebc86e2747f197f01f824fab2
sources_digest: c7eee6970140e127d2f005a8c7f1287ab02372ca4cc8fc2f47628564f90c0120
links: []
generator:
  version: 1
covers:
  - symbol: _load_key
    kind: function
    at: 'scripts/ops/rfq-send.py:L61-L82'
  - symbol: _app_dir
    kind: function
    at: 'scripts/ops/rfq-send.py:L85-L87'
  - symbol: _air
    kind: function
    at: 'scripts/ops/rfq-send.py:L91-L103'
  - symbol: _record
    kind: function
    at: 'scripts/ops/rfq-send.py:L106-L107'
  - symbol: _all_rows
    kind: function
    at: 'scripts/ops/rfq-send.py:L110-L121'
  - symbol: _sponsor_ok
    kind: function
    at: 'scripts/ops/rfq-send.py:L125-L126'
  - symbol: _opted_out
    kind: function
    at: 'scripts/ops/rfq-send.py:L129-L130'
  - symbol: _already_sent
    kind: function
    at: 'scripts/ops/rfq-send.py:L133-L134'
  - symbol: _email_of
    kind: function
    at: 'scripts/ops/rfq-send.py:L137-L139'
  - symbol: _caps_now
    kind: function
    at: 'scripts/ops/rfq-send.py:L142-L152'
  - symbol: render
    kind: function
    at: 'scripts/ops/rfq-send.py:L155-L163'
  - symbol: anonymity_scan
    kind: function
    at: 'scripts/ops/rfq-send.py:L166-L171'
  - symbol: decide
    kind: function
    at: 'scripts/ops/rfq-send.py:L174-L197'
  - symbol: send_fe
    kind: function
    at: 'scripts/ops/rfq-send.py:L201-L226'
  - symbol: _mark_sent
    kind: function
    at: 'scripts/ops/rfq-send.py:L229-L232'
  - symbol: main
    kind: function
    at: 'scripts/ops/rfq-send.py:L236-L278'
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
  - symbol: loop_env
    kind: function
    at: 'scripts/ops/verify-mcp-keys.py:L39-L51'
  - symbol: main
    kind: function
    at: 'scripts/ops/verify-mcp-keys.py:L54-L75'
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

...
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
