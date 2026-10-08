---
name: Consensus pruning + ledger guard
slug: consensus-pruning-ledger-guard
type: system
sources:
  - path: scripts/ops/consensus-prune.py
    hash: 721ea1c0b942cae4679c4472f4ec5547e4655cd9e94c12c9ddc8fccd2f922821
  - path: scripts/ops/ledger-guard.py
    hash: 5b3098424eada1d1f669995baf5e1dd76ea4fb724c0c524ddc9986ce361128d7
sources_digest: 7627c05bf56e7d9e6243c5f96b23027618db7f792b5ec87990f0764c9bbe3ac5
links:
  - to: idle-skip-note
    relation: uses
    description: Both write to consensus.md; idle-skip appends a per-day line.
generator:
  version: 1
covers:
  - symbol: _load_runtime_env
    kind: function
    at: 'scripts/ops/consensus-prune.py:L69-L80'
  - symbol: _env_int
    kind: function
    at: 'scripts/ops/consensus-prune.py:L83-L88'
  - symbol: _env_flag
    kind: function
    at: 'scripts/ops/consensus-prune.py:L91-L92'
  - symbol: _app
    kind: function
    at: 'scripts/ops/consensus-prune.py:L95-L96'
  - symbol: _sha16
    kind: function
    at: 'scripts/ops/consensus-prune.py:L99-L100'
  - symbol: _load_state
    kind: function
    at: 'scripts/ops/consensus-prune.py:L103-L107'
  - symbol: _save_state
    kind: function
    at: 'scripts/ops/consensus-prune.py:L110-L117'
  - symbol: _section_sizes
    kind: function
    at: 'scripts/ops/consensus-prune.py:L120-L125'
  - symbol: Skip
    kind: class
    at: 'scripts/ops/consensus-prune.py:L128-L129'
  - symbol: _split_section
    kind: function
    at: 'scripts/ops/consensus-prune.py:L132-L146'
  - symbol: _parse_entries
    kind: function
    at: 'scripts/ops/consensus-prune.py:L149-L186'
  - symbol: _check_monotonic
    kind: function
    at: 'scripts/ops/consensus-prune.py:L189-L196'
  - symbol: _archive_path
    kind: function
    at: 'scripts/ops/consensus-prune.py:L199-L200'
  - symbol: main
    kind: function
    at: 'scripts/ops/consensus-prune.py:L203-L373'
  - symbol: finish_skip
    kind: function
    at: 'scripts/ops/consensus-prune.py:L227-L245'
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

Two cooperating integrity mechanisms for consensus.md and the Gate-0 ledger. consensus-prune.py archives old cycle entries byte-exact with sha256-stamped headers when the file exceeds a threshold, deliberately avoiding ledger-guard's INCIDENT_RE words so it doesn't trigger the content-loss alarm, and logs state for the guard to exempt the transition. ledger-guard.py keeps rolling backups and detects content drops by comparing metrics against the previous cycle, with _rebase_after_prune reconciling baselines after legitimate pruning so real deletions still alarm. Both always exit 0.

## Related

- uses [[idle-skip-note]] — Both write to consensus.md; idle-skip appends a per-day line.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
