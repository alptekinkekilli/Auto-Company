---
name: Sentry Reporter
slug: sentry-reporter
type: file
sources:
  - path: dashboard/sentry_client.py
    hash: 96977bb6701f18064edb69c783e53bdb73c930c8ddadcd1caf47583b42700df4
sources_digest: d14955d1810e44ac017b77743809ea9e510da96b9f40c625eb3bfe88e5d2372d
links:
  - to: cockpit-dashboard-server
    relation: part_of
    description: External library used by server.py for error reporting.
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

Minimal stdlib-only Sentry error reporter that POSTs to Sentry's legacy Store API via urllib.request, avoiding the official sentry-sdk because the container has no pip deps. Best-effort: any failure is caught and logged to stderr, never raised, so monitoring cannot crash the dashboard. DSN parsed and cached at import time; 3-second timeout; X-Sentry-Auth header built manually with sentry_version=7.

## Related

- part of [[cockpit-dashboard-server]] — External library used by server.py for error reporting.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
