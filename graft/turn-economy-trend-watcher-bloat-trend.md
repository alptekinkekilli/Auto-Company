---
name: Turn-economy trend watcher (bloat-trend)
slug: turn-economy-trend-watcher-bloat-trend
type: file
sources:
  - path: scripts/ops/bloat-trend.py
    hash: f74441749dee8335f3eb7b9fa4626fcde6b9903cf0006019a261e8c35115fe26
sources_digest: 3e232ea381ef4bec4947e6f0531d443f974034d08c1e18e714de47abbc332a73
links:
  - to: budget-calibration-cost-audit
    relation: uses
    description: >-
      Consumes the same auto-loop.log audit lines and turn-audit format as
      cost-audit.py.
generator:
  version: 1
covers:
  - symbol: ingest
    kind: function
    at: 'scripts/ops/bloat-trend.py:L54-L97'
  - symbol: is_bloated
    kind: function
    at: 'scripts/ops/bloat-trend.py:L109-L110'
  - symbol: summarise
    kind: function
    at: 'scripts/ops/bloat-trend.py:L113-L126'
  - symbol: pct
    kind: function
    at: 'scripts/ops/bloat-trend.py:L117-L118'
  - symbol: notify
    kind: function
    at: 'scripts/ops/bloat-trend.py:L129-L142'
  - symbol: fmt
    kind: function
    at: 'scripts/ops/bloat-trend.py:L145-L155'
  - symbol: d
    kind: function
    at: 'scripts/ops/bloat-trend.py:L146-L151'
  - symbol: main
    kind: function
    at: 'scripts/ops/bloat-trend.py:L158-L237'
  - symbol: hits_target
    kind: function
    at: 'scripts/ops/bloat-trend.py:L185-L187'
---
<!-- context:generated:start -->
## Summary

Trend watcher answering whether per-cycle turn-economy metrics improve over time, folding audit lines idempotently into durable NDJSON history keyed by session id and comparing a sliding window (default 15 cycles) against the preceding one. Stays quiet, alerting only on regression (p90 turns worsening ≥20% AND bloated share doubling past target), target met (bloated ≤10% AND p90 ≤55 for two consecutive windows to avoid false victory), or explicit --report. Stored verdicts are recomputed from raw numbers using current thresholds because thresholds changed 2026-08-02 — comparisons measure cycles, not the ruler.

## Related

- uses [[budget-calibration-cost-audit]] — Consumes the same auto-loop.log audit lines and turn-audit format as cost-audit.py.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
