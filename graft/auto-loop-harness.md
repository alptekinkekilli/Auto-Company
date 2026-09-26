---
name: Auto-loop harness
slug: auto-loop-harness
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: b3850b8050b576a46bfa19953ae0492889b603967275721a09344b9589552d56
  - path: scripts/ops/ledger-guard.py
    hash: 9892f74da9b9b06f9977b053a05717c67eeafc4030ee7dbd2e2bc087fb8c3400
  - path: scripts/ops/state-snapshot.py
    hash: 3112f4632b64a6b531b215ea81ba82b2ceb6436942511f816de94ced3171bfe8
  - path: scripts/ops/tool-usage-audit.py
    hash: 73a75d68bab3e0b42e31ad3d268b44a8c7ac168b91c6a8d1b2f1b3cd4cdba975
  - path: scripts/ops/turn-audit.py
    hash: 006e9aac95a503a1e158d1c6f03a7bdf98f44322805509d886c627e74d4d41d0
  - path: scripts/ops/turn-bloat-brake.py
    hash: c4d72b732830311e89db486abb41c8a13a5760ffa043354c953b99a155ff96fb
  - path: scripts/ops/verify-mcp-keys.py
    hash: a35c1f35481876cedc5bb4cf0c7fd4eceaea1c85e57d3c28e87560b3f9f342db
  - path: scripts/ops/web-research-cost.py
    hash: 24d7735b6dc6defa0f80e75aeee37a13a40d4df43e9b38539be02df6fe23cbf2
  - path: scripts/ops/work-window-watchdog.py
    hash: 228677456f5e5634b3c6a9964c8b92e13a4c2e4992154feed8a3334779fd0a5f
  - path: scripts/ops/work-window.py
    hash: 7b39b958c05be0d7242887ae4957cf7e6034f20990d587dbab31471a3365c92a
sources_digest: db5c3f0a4775f16bf181f8b82e88d7c536769c602fe9262caeb6527f732156f8
links:
  - to: budget-gates
    relation: part_of
    description: >-
      evaluate_budget_gates, select_cycle_engine, and record_total_spend live in
      auto-loop.sh and are validated by test_budget_gates.sh.
  - to: telegram-notify-shell-out
    relation: uses
    description: >-
      Escalation scripts (turn-bloat-brake, work-window-watchdog) print Telegram
      alarms via this script.
  - to: work-window-brake
    relation: part_of
    description: >-
      work-window.py and work-window-watchdog.py are the brake and its alarm
      companion wired into the loop.
generator:
  version: 1
covers:
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
  - symbol: _check
    kind: function
    at: 'scripts/ops/ledger-guard.py:L121-L146'
  - symbol: main
    kind: function
    at: 'scripts/ops/ledger-guard.py:L149-L212'
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
  - symbol: calls_from_ndjson
    kind: function
    at: 'scripts/ops/tool-usage-audit.py:L43-L65'
  - symbol: categorize
    kind: function
    at: 'scripts/ops/tool-usage-audit.py:L68-L121'
  - symbol: main
    kind: function
    at: 'scripts/ops/tool-usage-audit.py:L124-L251'
  - symbol: dump
    kind: function
    at: 'scripts/ops/tool-usage-audit.py:L177-L190'
  - symbol: ts_of
    kind: function
    at: 'scripts/ops/turn-audit.py:L74-L78'
  - symbol: scan
    kind: function
    at: 'scripts/ops/turn-audit.py:L81-L112'
  - symbol: floor_usd
    kind: function
    at: 'scripts/ops/turn-audit.py:L115-L118'
  - symbol: summary_line
    kind: function
    at: 'scripts/ops/turn-audit.py:L121-L139'
  - symbol: main
    kind: function
    at: 'scripts/ops/turn-audit.py:L142-L155'
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
  - symbol: loop_env
    kind: function
    at: 'scripts/ops/verify-mcp-keys.py:L39-L51'
  - symbol: main
    kind: function
    at: 'scripts/ops/verify-mcp-keys.py:L54-L75'
  - symbol: is_web
    kind: function
    at: 'scripts/ops/web-research-cost.py:L43-L44'
  - symbol: analyse
    kind: function
    at: 'scripts/ops/web-research-cost.py:L47-L76'
  - symbol: main
    kind: function
    at: 'scripts/ops/web-research-cost.py:L79-L161'
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

The central orchestration loop scripts/core/auto-loop.sh and its operational guards. It owns the cycle counter (monotonic across redeploys, self-healing from cycle-NNNN logs), the business-hours _window_active gate, the budget gates (15 behaviors from APP-263), the work-window brake, the ledger guard, and the turn-bloat brake. Fail-closed throughout: any degraded read latches a hold rather than lowering a prior observation.

## Related

- part of [[budget-gates]] — evaluate_budget_gates, select_cycle_engine, and record_total_spend live in auto-loop.sh and are validated by test_budget_gates.sh.
- uses [[telegram-notify-shell-out]] — Escalation scripts (turn-bloat-brake, work-window-watchdog) print Telegram alarms via this script.
- part of [[work-window-brake]] — work-window.py and work-window-watchdog.py are the brake and its alarm companion wired into the loop.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
