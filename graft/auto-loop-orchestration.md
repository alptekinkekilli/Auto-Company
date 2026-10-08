---
name: auto-loop orchestration
slug: auto-loop-orchestration
type: concept
sources:
  - path: scripts/core/monitor.sh
    hash: 9a104b2efb99c2712cbff51c614b1dc964f3a8be29ba7bc990c3d63d7c58bd03
  - path: scripts/core/sentry-heartbeat.sh
    hash: 874eccbdbde7e82f3b3f97f023c1503321380b2c7a28754386d1fb7b366ac12f
  - path: scripts/core/stop-loop.sh
    hash: 4ea7f4b5ce31ce14039bf5cedd3c6a9718e2357906fe289906d06debe11f3fe3
  - path: scripts/graft-auto-refresh.py
    hash: 678e4a269c718dc9043afa096157f5d835cb3099883d31954de70ff10a4bfe33
  - path: scripts/ops/consensus-prune.py
    hash: 8f4770cc811cb6df649d8003446b2ce59125e8ee2482fc513a9f59a2303a8400
  - path: scripts/ops/idle-skip-note.py
    hash: 1d4f853b19cdc9ee94c0fd1136ea67393d04deb36a7563e2720ef15a0631ec98
  - path: scripts/ops/ledger-guard.py
    hash: 5b3098424eada1d1f669995baf5e1dd76ea4fb724c0c524ddc9986ce361128d7
sources_digest: 7125cb676d701316fa90d7df0bf7239af853fb1ce923ffea2f7496c4df8a7228
links: []
generator:
  version: 1
covers:
  - symbol: _repo_root
    kind: function
    at: 'scripts/graft-auto-refresh.py:L42-L54'
  - symbol: _git
    kind: function
    at: 'scripts/graft-auto-refresh.py:L57-L68'
  - symbol: _lock_alive
    kind: function
    at: 'scripts/graft-auto-refresh.py:L71-L81'
  - symbol: _emit
    kind: function
    at: 'scripts/graft-auto-refresh.py:L84-L94'
  - symbol: main
    kind: function
    at: 'scripts/graft-auto-refresh.py:L97-L187'
  - symbol: status
    kind: function
    at: 'scripts/graft-auto-refresh.py:L122-L132'
  - symbol: fmt
    kind: function
    at: 'scripts/graft-auto-refresh.py:L134-L137'
  - symbol: _load_runtime_env
    kind: function
    at: 'scripts/ops/consensus-prune.py:L64-L75'
  - symbol: _env_int
    kind: function
    at: 'scripts/ops/consensus-prune.py:L78-L83'
  - symbol: _env_flag
    kind: function
    at: 'scripts/ops/consensus-prune.py:L86-L87'
  - symbol: _app
    kind: function
    at: 'scripts/ops/consensus-prune.py:L90-L91'
  - symbol: _sha16
    kind: function
    at: 'scripts/ops/consensus-prune.py:L94-L95'
  - symbol: _load_state
    kind: function
    at: 'scripts/ops/consensus-prune.py:L98-L102'
  - symbol: _save_state
    kind: function
    at: 'scripts/ops/consensus-prune.py:L105-L112'
  - symbol: _section_sizes
    kind: function
    at: 'scripts/ops/consensus-prune.py:L115-L120'
  - symbol: Skip
    kind: class
    at: 'scripts/ops/consensus-prune.py:L123-L124'
  - symbol: _split_section
    kind: function
    at: 'scripts/ops/consensus-prune.py:L127-L141'
  - symbol: _parse_entries
    kind: function
    at: 'scripts/ops/consensus-prune.py:L144-L174'
  - symbol: _check_monotonic
    kind: function
    at: 'scripts/ops/consensus-prune.py:L177-L184'
  - symbol: _archive_path
    kind: function
    at: 'scripts/ops/consensus-prune.py:L187-L188'
  - symbol: main
    kind: function
    at: 'scripts/ops/consensus-prune.py:L191-L361'
  - symbol: finish_skip
    kind: function
    at: 'scripts/ops/consensus-prune.py:L215-L233'
  - symbol: build_line
    kind: function
    at: 'scripts/ops/idle-skip-note.py:L26-L34'
  - symbol: main
    kind: function
    at: 'scripts/ops/idle-skip-note.py:L37-L89'
  - symbol: _env_int
    kind: function
    at: 'scripts/ops/ledger-guard.py:L43-L48'
  - symbol: _env_float
    kind: function
    at: 'scripts/ops/ledger-guard.py:L51-L55'
  - symbol: _app
    kind: function
    at: 'scripts/ops/ledger-guard.py:L58-L59'
  - symbol: _find_ledger
    kind: function
    at: 'scripts/ops/ledger-guard.py:L62-L69'
  - symbol: _metrics
    kind: function
    at: 'scripts/ops/ledger-guard.py:L72-L84'
  - symbol: _backup
    kind: function
    at: 'scripts/ops/ledger-guard.py:L87-L101'
  - symbol: _load_state
    kind: function
    at: 'scripts/ops/ledger-guard.py:L104-L108'
  - symbol: _save_state
    kind: function
    at: 'scripts/ops/ledger-guard.py:L111-L118'
  - symbol: _rebase_after_prune
    kind: function
    at: 'scripts/ops/ledger-guard.py:L125-L142'
  - symbol: _check
    kind: function
    at: 'scripts/ops/ledger-guard.py:L145-L170'
  - symbol: main
    kind: function
    at: 'scripts/ops/ledger-guard.py:L173-L240'
---
<!-- context:generated:start -->
## Summary

The central background loop that ties together the cycle lifecycle, budget gates, consensus memory, and operator escalation. It is the consumer of most scripts here: final-text extractors give it plain answers, engine-usage-cost feeds its budget ledger, ledger-guard/consensus-prune protect its memory files, monitor/stop-loop manage its lifecycle, and sentry-heartbeat proves its liveness. Its [PROMPT-SIZE] brake and IDLE-SKIP path are the failure modes that consensus-prune and idle-skip-note respectively address.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
