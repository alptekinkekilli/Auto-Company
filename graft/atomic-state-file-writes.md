---
name: Atomic State File Writes
slug: atomic-state-file-writes
type: concept
sources:
  - path: scripts/ops/consensus-prune.py
    hash: 1a741019d9b78a90dc9121e012850f5bcebd88fbd8527a8b17a4357068ca4684
  - path: scripts/ops/state-snapshot.py
    hash: 3112f4632b64a6b531b215ea81ba82b2ceb6436942511f816de94ced3171bfe8
  - path: scripts/ops/turn-bloat-brake.py
    hash: c4d72b732830311e89db486abb41c8a13a5760ffa043354c953b99a155ff96fb
  - path: scripts/ops/work-window-watchdog.py
    hash: 228677456f5e5634b3c6a9964c8b92e13a4c2e4992154feed8a3334779fd0a5f
  - path: scripts/ops/work-window.py
    hash: 7b39b958c05be0d7242887ae4957cf7e6034f20990d587dbab31471a3365c92a
sources_digest: b1d8554a567abb2492d6b74ddc1c3cafea6c0ce78cd446a1e1a3472fdb0fd034
links:
  - to: auto-loop-harness-brakes-and-guards
    relation: implements
    description: All guard state files use atomic tmp+rename writes
generator:
  version: 1
covers:
  - symbol: _load_runtime_env
    kind: function
    at: 'scripts/ops/consensus-prune.py:L101-L112'
  - symbol: _env_int
    kind: function
    at: 'scripts/ops/consensus-prune.py:L115-L120'
  - symbol: _env_flag
    kind: function
    at: 'scripts/ops/consensus-prune.py:L123-L124'
  - symbol: _app
    kind: function
    at: 'scripts/ops/consensus-prune.py:L127-L128'
  - symbol: _sha16
    kind: function
    at: 'scripts/ops/consensus-prune.py:L131-L132'
  - symbol: _load_state
    kind: function
    at: 'scripts/ops/consensus-prune.py:L135-L139'
  - symbol: _save_state
    kind: function
    at: 'scripts/ops/consensus-prune.py:L142-L149'
  - symbol: Skip
    kind: class
    at: 'scripts/ops/consensus-prune.py:L152-L153'
  - symbol: Section
    kind: class
    at: 'scripts/ops/consensus-prune.py:L157-L172'
  - symbol: __init__
    kind: method
    at: 'scripts/ops/consensus-prune.py:L160-L168'
  - symbol: kind
    kind: method
    at: 'scripts/ops/consensus-prune.py:L171-L172'
  - symbol: Removal
    kind: class
    at: 'scripts/ops/consensus-prune.py:L175-L184'
  - symbol: __init__
    kind: method
    at: 'scripts/ops/consensus-prune.py:L179-L184'
  - symbol: _split_sections
    kind: function
    at: 'scripts/ops/consensus-prune.py:L187-L195'
  - symbol: _mark_primary
    kind: function
    at: 'scripts/ops/consensus-prune.py:L198-L219'
  - symbol: flush
    kind: function
    at: 'scripts/ops/consensus-prune.py:L204-L207'
  - symbol: _tail_pass
    kind: function
    at: 'scripts/ops/consensus-prune.py:L223-L227'
  - symbol: _entries_wwd
    kind: function
    at: 'scripts/ops/consensus-prune.py:L230-L262'
  - symbol: _entries_para
    kind: function
    at: 'scripts/ops/consensus-prune.py:L265-L282'
  - symbol: _select
    kind: function
    at: 'scripts/ops/consensus-prune.py:L285-L308'
  - symbol: _line_offsets
    kind: function
    at: 'scripts/ops/consensus-prune.py:L312-L316'
  - symbol: _strip_and_blocks
    kind: function
    at: 'scripts/ops/consensus-prune.py:L319-L334'
  - symbol: _rebuild
    kind: function
    at: 'scripts/ops/consensus-prune.py:L337-L346'
  - symbol: main
    kind: function
    at: 'scripts/ops/consensus-prune.py:L350-L647'
  - symbol: finish_skip
    kind: function
    at: 'scripts/ops/consensus-prune.py:L379-L395'
  - symbol: after_bytes
    kind: function
    at: 'scripts/ops/consensus-prune.py:L461-L462'
  - symbol: record_history
    kind: function
    at: 'scripts/ops/consensus-prune.py:L478-L495'
  - symbol: emit_warns
    kind: function
    at: 'scripts/ops/consensus-prune.py:L497-L499'
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
  - symbol: _app
    kind: function
    at: 'scripts/ops/turn-bloat-brake.py:L25-L26'
  - symbol: _streak_len
    kind: function
    at: 'scripts/ops/turn-bloat-brake.py:L29-L34'
  - symbol: _load
    kind: function
    at: 'scripts/ops/turn-bloat-brake.py:L37-L41'
  - symbol: _save
    kind: function
    at: 'scripts/ops/turn-bloat-brake.py:L44-L51'
  - symbol: main
    kind: function
    at: 'scripts/ops/turn-bloat-brake.py:L63-L104'
  - symbol: _app_dir
    kind: function
    at: 'scripts/ops/work-window-watchdog.py:L45-L48'
  - symbol: _threshold
    kind: function
    at: 'scripts/ops/work-window-watchdog.py:L51-L57'
  - symbol: _read_state
    kind: function
    at: 'scripts/ops/work-window-watchdog.py:L60-L64'
  - symbol: _write_state
    kind: function
    at: 'scripts/ops/work-window-watchdog.py:L67-L74'
  - symbol: main
    kind: function
    at: 'scripts/ops/work-window-watchdog.py:L77-L125'
  - symbol: _app_dir
    kind: function
    at: 'scripts/ops/work-window.py:L44-L48'
  - symbol: _env_int
    kind: function
    at: 'scripts/ops/work-window.py:L51-L58'
  - symbol: _parse_delta
    kind: function
    at: 'scripts/ops/work-window.py:L61-L70'
  - symbol: _read_state
    kind: function
    at: 'scripts/ops/work-window.py:L73-L80'
  - symbol: _write_state
    kind: function
    at: 'scripts/ops/work-window.py:L83-L87'
  - symbol: _line
    kind: function
    at: 'scripts/ops/work-window.py:L90-L100'
  - symbol: main
    kind: function
    at: 'scripts/ops/work-window.py:L103-L160'
---
<!-- context:generated:start -->
## Summary

A recurring convention: all state files (work-window.json, turn-bloat-state.json, state-snapshot-last.json, consensus-prune.json, work-window-watchdog.json) are written atomically via temp file + os.replace so a crash mid-write never corrupts the guard state. This is critical because these files gate fail-closed behavior — a corrupt state file must fail open (exit 10) rather than silently pass.

## Related

- implements [[auto-loop-harness-brakes-and-guards]] — All guard state files use atomic tmp+rename writes
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
