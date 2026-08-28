---
name: Fail-Open Monitoring
slug: fail-open-monitoring
type: concept
sources:
  - path: dashboard/sentry_client.py
    hash: 96977bb6701f18064edb69c783e53bdb73c930c8ddadcd1caf47583b42700df4
  - path: projects/_archive/snapog/src/alerts/check.ts
    hash: fa0fdacdc3a2b495e86f2e70be76d1cadba5f829c78f39010a53d479eb5192c4
  - path: projects/_archive/snapog/src/alerts/webhook.ts
    hash: 518ec45652bc5010bbd34856e527e2dc9c2dfa525aea151ff467f3a802c9da81
  - path: scripts/analyst/merge_registry.py
    hash: 55719338148054fff06780400062453a037e4bf10fe5817f04536b5c85ade7d1
  - path: scripts/analyst/promote_directive.py
    hash: 9c45147f1730fc30545b94a30428d54e0bd40f04506aa3db00614880ec93d677
  - path: scripts/compact-preflight.py
    hash: e05718ceddc1954b8cefcea9ad00d143d0adb92d0d5547b55fe3916e5fbdb0b3
  - path: scripts/compact-report.py
    hash: acbd35a8779fa472cd8164183bcc13c79e716e9e05a51473b0cd2e1b5e2375d1
  - path: scripts/core/bridge_leak_scan.py
    hash: e5b7b7ecf614217b79e93037d780bdd0314f4953d8e6308939a49fe5b5b92bcf
sources_digest: 1a3681c3ff7b8ff33348a872d1c646baee516d18ca07e8053077ac47ad29a32f
links: []
generator:
  version: 1
covers:
  - symbol: _parse_dsn
    kind: function
    at: 'dashboard/sentry_client.py:L33-L43'
  - symbol: capture_exception
    kind: function
    at: 'dashboard/sentry_client.py:L49-L102'
  - symbol: AlertSeverity
    kind: type
    at: 'projects/_archive/snapog/src/alerts/check.ts:L10-L10'
  - symbol: Alert
    kind: interface
    at: 'projects/_archive/snapog/src/alerts/check.ts:L12-L18'
  - symbol: checkD1WritesPerDay
    kind: function
    at: 'projects/_archive/snapog/src/alerts/check.ts:L27-L44'
  - symbol: checkCacheHitRate
    kind: function
    at: 'projects/_archive/snapog/src/alerts/check.ts:L46-L71'
  - symbol: checkNewSignups
    kind: function
    at: 'projects/_archive/snapog/src/alerts/check.ts:L73-L89'
  - symbol: checkActiveUsers
    kind: function
    at: 'projects/_archive/snapog/src/alerts/check.ts:L91-L105'
  - symbol: checkR2Storage
    kind: function
    at: 'projects/_archive/snapog/src/alerts/check.ts:L107-L126'
  - symbol: runAllChecks
    kind: function
    at: 'projects/_archive/snapog/src/alerts/check.ts:L131-L150'
  - symbol: AlertPayload
    kind: interface
    at: 'projects/_archive/snapog/src/alerts/webhook.ts:L8-L13'
  - symbol: postAlerts
    kind: function
    at: 'projects/_archive/snapog/src/alerts/webhook.ts:L15-L42'
  - symbol: identifier_fields
    kind: function
    at: 'scripts/analyst/merge_registry.py:L66-L76'
  - symbol: audit
    kind: function
    at: 'scripts/analyst/merge_registry.py:L79-L82'
  - symbol: blocked
    kind: function
    at: 'scripts/analyst/merge_registry.py:L85-L88'
  - symbol: extract_ids
    kind: function
    at: 'scripts/analyst/merge_registry.py:L91-L105'
  - symbol: extract_axes
    kind: function
    at: 'scripts/analyst/merge_registry.py:L108-L120'
  - symbol: table_rows
    kind: function
    at: 'scripts/analyst/merge_registry.py:L123-L131'
  - symbol: row_identity
    kind: function
    at: 'scripts/analyst/merge_registry.py:L134-L151'
  - symbol: sections
    kind: function
    at: 'scripts/analyst/merge_registry.py:L154-L163'
  - symbol: active_candidates
    kind: function
    at: 'scripts/analyst/merge_registry.py:L166-L186'
  - symbol: normalize_axis
    kind: function
    at: 'scripts/analyst/merge_registry.py:L189-L190'
  - symbol: resolve_span
    kind: function
    at: 'scripts/analyst/merge_registry.py:L193-L232'
  - symbol: _rewind_over_separators
    kind: function
    at: 'scripts/analyst/merge_registry.py:L235-L246'
  - symbol: split_registry
    kind: function
    at: 'scripts/analyst/merge_registry.py:L249-L272'
  - symbol: main
    kind: function
    at: 'scripts/analyst/merge_registry.py:L275-L428'
  - symbol: sha256
    kind: function
    at: 'scripts/analyst/promote_directive.py:L91-L92'
  - symbol: audit
    kind: function
    at: 'scripts/analyst/promote_directive.py:L95-L98'
  - symbol: blocked
    kind: function
    at: 'scripts/analyst/promote_directive.py:L101-L104'
  - symbol: notify
    kind: function
    at: 'scripts/analyst/promote_directive.py:L107-L113'
  - symbol: main
    kind: function
    at: 'scripts/analyst/promote_directive.py:L116-L225'
  - symbol: sh
    kind: function
    at: 'scripts/compact-preflight.py:L24-L28'
  - symbol: repo_report
    kind: function
    at: 'scripts/compact-preflight.py:L31-L48'
  - symbol: main
    kind: function
    at: 'scripts/compact-preflight.py:L51-L80'
  - symbol: sh
    kind: function
    at: 'scripts/compact-report.py:L30-L35'
  - symbol: sh_input
    kind: function
    at: 'scripts/compact-report.py:L38-L43'
  - symbol: repo_root
    kind: function
    at: 'scripts/compact-report.py:L46-L48'
  - symbol: line_repo
    kind: function
    at: 'scripts/compact-report.py:L51-L59'
  - symbol: block_prod
    kind: function
    at: 'scripts/compact-report.py:L62-L71'
  - symbol: block_loop
    kind: function
    at: 'scripts/compact-report.py:L74-L145'
  - symbol: grab
    kind: function
    at: 'scripts/compact-report.py:L101-L103'
  - symbol: block_discretionary
    kind: function
    at: 'scripts/compact-report.py:L148-L199'
  - symbol: g
    kind: function
    at: 'scripts/compact-report.py:L186-L188'
  - symbol: main
    kind: function
    at: 'scripts/compact-report.py:L202-L212'
  - symbol: scan
    kind: function
    at: 'scripts/core/bridge_leak_scan.py:L63-L69'
  - symbol: selftest
    kind: function
    at: 'scripts/core/bridge_leak_scan.py:L98-L111'
  - symbol: main
    kind: function
    at: 'scripts/core/bridge_leak_scan.py:L114-L127'
---
<!-- context:generated:start -->
## Summary

A pervasive design principle: monitoring and reporting must never crash the system. Sentry reporting catches all failures, alert checks treat thrown errors as no-alert, webhook delivery falls back to log-only, compact hooks always exit 0, and the ccusage block hides when unavailable. The inverse is the fail-closed gates (promotion, merge, leak scanner) that refuse to proceed on uncertainty.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
