---
name: opportunity analyst orchestration
slug: opportunity-analyst-orchestration
type: system
sources:
  - path: scripts/ops/opportunity-analyst-cron.sh
    hash: 57b25b2a7db84a5155d3a56c2cbca69f949cbc56883de0d0d52c2dbf87c63b4e
  - path: scripts/ops/state-snapshot.py
    hash: 3112f4632b64a6b531b215ea81ba82b2ceb6436942511f816de94ced3171bfe8
sources_digest: 34a93427a43ac8e365fe5883356f5ecd4213bf787b1e74bcbedbf09b601594d6
links:
  - to: cost-budget-reporting
    relation: uses
    description: The analyst runs after cost-audit so it interprets measured numbers.
  - to: loop-lifecycle-monitoring
    relation: uses
    description: Reports liveness to Sentry Crons like sentry-heartbeat.sh.
generator:
  version: 1
covers:
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
---
<!-- context:generated:start -->
## Summary

Daily cron orchestration of the Opportunity Analyst, selecting jcode or codex engine, enforcing a codex-idle guard, reporting liveness to Sentry, and handling image-tag fallback and rollback. Also the state-snapshot probe that collapses per-cycle state checks into one turn.

## Related

- uses [[cost-budget-reporting]] — The analyst runs after cost-audit so it interprets measured numbers.
- uses [[loop-lifecycle-monitoring]] — Reports liveness to Sentry Crons like sentry-heartbeat.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
