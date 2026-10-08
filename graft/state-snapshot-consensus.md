---
name: State Snapshot & Consensus
slug: state-snapshot-consensus
type: system
sources:
  - path: scripts/ops/consensus-prune.py
    hash: 47d5d806a8f48f41817b9bce5cc8e759d9ed04b244627e858664aeef6c9cf42b
  - path: scripts/ops/state-snapshot.py
    hash: 3112f4632b64a6b531b215ea81ba82b2ceb6436942511f816de94ced3171bfe8
  - path: tests/test_auto_loop_consensus_prune.sh
    hash: 9f5bbd179e642477f15485da93a5390b583697954e54da99cd4e2af00dce5eb8
  - path: tests/test_consensus_prune.py
    hash: 8d093395e45aaa2340d7b9ee706ebcb97f02510efb903ed5432f7079982cb339
sources_digest: 6dbe3e07c1171210b6fa9460259b287ec9b36cb9c9079bf2086abf556587950d
links:
  - to: auto-loop-harness
    relation: part_of
    description: >-
      consensus-prune.py is invoked by auto-loop.sh after ledger-guard.py, gated
      on cycle_failed_reason being empty.
  - to: cycle-escalation-brakes
    relation: produces
    description: >-
      The DELTA line from state-snapshot.py is the input that work-window.py
      parses to decide whether to open/keep a work window.
generator:
  version: 1
covers:
  - symbol: _env_int
    kind: function
    at: 'scripts/ops/consensus-prune.py:L61-L66'
  - symbol: _app
    kind: function
    at: 'scripts/ops/consensus-prune.py:L69-L70'
  - symbol: _sha16
    kind: function
    at: 'scripts/ops/consensus-prune.py:L73-L74'
  - symbol: _load_state
    kind: function
    at: 'scripts/ops/consensus-prune.py:L77-L81'
  - symbol: _save_state
    kind: function
    at: 'scripts/ops/consensus-prune.py:L84-L91'
  - symbol: _section_sizes
    kind: function
    at: 'scripts/ops/consensus-prune.py:L94-L99'
  - symbol: Skip
    kind: class
    at: 'scripts/ops/consensus-prune.py:L102-L103'
  - symbol: _split_section
    kind: function
    at: 'scripts/ops/consensus-prune.py:L106-L120'
  - symbol: _parse_entries
    kind: function
    at: 'scripts/ops/consensus-prune.py:L123-L153'
  - symbol: _check_monotonic
    kind: function
    at: 'scripts/ops/consensus-prune.py:L156-L163'
  - symbol: _archive_path
    kind: function
    at: 'scripts/ops/consensus-prune.py:L166-L167'
  - symbol: main
    kind: function
    at: 'scripts/ops/consensus-prune.py:L170-L327'
  - symbol: finish_skip
    kind: function
    at: 'scripts/ops/consensus-prune.py:L190-L208'
  - symbol: file_sha16
    kind: function
    at: 'scripts/ops/state-snapshot.py:L54-L61'
  - symbol: directive_state
    kind: function
    at: 'scripts/ops/state-snapshot.py:L64-L72'
  - symbol: opreq_open
    kind: function
    at: 'scripts/ops/state-snapshot.py:L75-L87'
  - symbol: wowcar_sources
    kind: function
    at: 'scripts/ops/state-snapshot.py:L90-L104'
  - symbol: main
    kind: function
    at: 'scripts/ops/state-snapshot.py:L107-L166'
  - symbol: check
    kind: function
    at: 'tests/test_consensus_prune.py:L17-L20'
  - symbol: newapp
    kind: function
    at: 'tests/test_consensus_prune.py:L23-L26'
  - symbol: consensus
    kind: function
    at: 'tests/test_consensus_prune.py:L29-L30'
  - symbol: entry
    kind: function
    at: 'tests/test_consensus_prune.py:L33-L38'
  - symbol: doc
    kind: function
    at: 'tests/test_consensus_prune.py:L41-L51'
  - symbol: run
    kind: function
    at: 'tests/test_consensus_prune.py:L54-L61'
  - symbol: guard
    kind: function
    at: 'tests/test_consensus_prune.py:L64-L67'
---
<!-- context:generated:start -->
## Summary

A one-call probe that collapses the per-cycle fan-out of state checks into a single turn, plus the consensus-prune hook that trims old cycle entries from consensus.md. state-snapshot.py prints a compact grep-friendly report of five watched surfaces (directive status/SHA, open OPREQ blocks, auditor report hash, combined Wowcar hash, operator-decisions hash) and computes a DELTA line against the previous snapshot so an unchanged world can be dismissed without re-probing; it always exits 0 so a probe failure never kills the cycle, and 'none' does not mean 'nothing to do' — standing orders still apply. consensus-prune.py archives old cycle entries when consensus.md exceeds a size threshold, keeping the 12 newest byte-exact, deduping archive blocks by SHA, and skipping on non-monotonic cycle numbers or missing section headers.

## Related

- part of [[auto-loop-harness]] — consensus-prune.py is invoked by auto-loop.sh after ledger-guard.py, gated on cycle_failed_reason being empty.
- produces [[cycle-escalation-brakes]] — The DELTA line from state-snapshot.py is the input that work-window.py parses to decide whether to open/keep a work window.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
