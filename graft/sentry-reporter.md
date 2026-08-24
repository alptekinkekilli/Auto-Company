---
name: Sentry reporter
slug: sentry-reporter
type: file
sources:
  - path: dashboard/sentry_client.py
    hash: 96977bb6701f18064edb69c783e53bdb73c930c8ddadcd1caf47583b42700df4
sources_digest: d14955d1810e44ac017b77743809ea9e510da96b9f40c625eb3bfe88e5d2372d
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
---
<!-- context:generated:start -->
## Summary

Stdlib-only Sentry error reporter (no sentry-sdk, no pip deps). Best-effort: any failure to reach Sentry is caught and logged, never raised, so monitoring cannot crash the dashboard. DSN parsed at import time; 3s timeout; legacy Store API.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
