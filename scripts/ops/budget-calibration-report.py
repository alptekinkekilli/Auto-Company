#!/usr/bin/env python3
"""APP-263 calibration report — run after 14 complete UTC days of four-gate data.

Produces, over the observation window:
  - per-engine 5h p50/p90/p95/max (sliding 5h windows sampled hourly — the real
    plan anchors are not retained historically, so this is a declared
    approximation of window peaks, not a replay of exact plan windows)
  - combined daily p50/p90/p95/max (UTC calendar days)
  - rolling weekly maximum (sliding 7x24h sampled daily)
  - block counts grouped by gate type (CLAUDE_5H / CODEX_5H / DAILY_TOTAL /
    WEEKLY_TOTAL, from [GATE] log lines)
  - time spent paused (gate-pause log lines x BUDGET_PAUSE_SECONDS)
  - observed operator interactive impact (from [LIMIT] plan-ceiling stamps and
    the operator-usage snapshot, to the extent history exists — gaps are
    reported as gaps, never silently zero)

All figures are API-equivalent/NOTIONAL usage, not billed cash. This script
never changes a threshold: per the decision, thresholds change only on a new
operator decision.

Usage (in the container):  python3 scripts/ops/budget-calibration-report.py [days]
Data: logs/spend-total.log (claude rows), ccusage codex sessions (analyst rows
excluded via logs/analyst-codex-sessions.log), logs/auto-loop.log.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import statistics
import subprocess
import sys

APP = os.environ.get("AC_APP_DIR", "/app")
LOG_DIR = os.path.join(APP, "logs")
DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 14
NOW = int(dt.datetime.now(dt.timezone.utc).timestamp())
SINCE = NOW - DAYS * 86400


def pct(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    k = max(0, min(len(values) - 1, round(p / 100 * (len(values) - 1))))
    return values[k]


def load_claude() -> list[tuple[int, float]]:
    out = []
    try:
        with open(os.path.join(LOG_DIR, "spend-total.log"), encoding="utf-8") as fh:
            for line in fh:
                parts = line.split()
                if len(parts) >= 4 and parts[1] == "claude":
                    try:
                        e, c = int(parts[0]), float(parts[3])
                    except ValueError:
                        continue
                    if e >= SINCE:
                        out.append((e, c))
    except FileNotFoundError:
        pass
    return out


def load_codex() -> list[tuple[int, float]]:
    excl = set()
    try:
        with open(os.path.join(LOG_DIR, "analyst-codex-sessions.log"), encoding="utf-8") as fh:
            for line in fh:
                parts = line.split()
                if len(parts) >= 2 and re.fullmatch(r"[0-9a-fA-F-]{36}", parts[1]):
                    excl.add(parts[1].lower())
    except FileNotFoundError:
        pass
    env = dict(os.environ, CODEX_HOME=os.environ.get("CODEX_HOME", os.path.join(LOG_DIR, ".codex")))
    try:
        raw = subprocess.run(["ccusage", "codex", "session", "--json"],
                             capture_output=True, timeout=120, env=env).stdout
        d = json.loads(raw)
    except Exception as exc:  # noqa: BLE001
        print(f"[warn] ccusage unavailable ({type(exc).__name__}) — codex figures MISSING, not zero")
        return []
    out = []
    for s in d.get("sessions", []):
        la = s.get("lastActivity")
        if not la:
            continue
        try:
            e = int(dt.datetime.fromisoformat(la.replace("Z", "+00:00")).timestamp())
        except ValueError:
            continue
        if e < SINCE:
            continue
        sf = (s.get("sessionFile") or "").lower()
        if sf and any(t in sf for t in excl):
            continue
        out.append((e, float(s.get("costUSD") or 0)))
    return out


def sliding(entries: list[tuple[int, float]], span: int, step: int) -> list[float]:
    if not entries:
        return []
    samples = []
    t = SINCE + span
    while t <= NOW:
        samples.append(sum(c for e, c in entries if t - span <= e < t))
        t += step
    return samples


def daily_buckets(entries: list[tuple[int, float]]) -> list[float]:
    buckets: dict[int, float] = {}
    for e, c in entries:
        buckets[e - (e % 86400)] = buckets.get(e - (e % 86400), 0.0) + c
    # only COMPLETE utc days
    today = NOW - (NOW % 86400)
    return [v for k, v in sorted(buckets.items()) if k < today]


def stats_line(name: str, vals: list[float]) -> str:
    if not vals:
        return f"  {name}: no data"
    return (f"  {name}: p50 ${pct(vals, 50):.2f} | p90 ${pct(vals, 90):.2f} | "
            f"p95 ${pct(vals, 95):.2f} | max ${max(vals):.2f}  (n={len(vals)})")


def main() -> int:
    claude = load_claude()
    codex = load_codex()
    both = sorted(claude + codex)

    print(f"# APP-263 calibration report — {DAYS} days ending {dt.datetime.fromtimestamp(NOW, dt.timezone.utc):%Y-%m-%d %H:%M UTC}")
    print("All values notional/API-equivalent (ccusage pricing), not billed cash.\n")

    print("## Per-engine 5h (sliding 5h windows, hourly samples — approximation, real plan anchors not retained)")
    print(stats_line("claude 5h", sliding(claude, 18000, 3600)))
    print(stats_line("codex  5h", sliding(codex, 18000, 3600)))

    print("\n## Combined daily (complete UTC days)")
    print(stats_line("daily TOTAL", daily_buckets(both)))

    print("\n## Rolling weekly (sliding 7×24h, daily samples)")
    weekly = sliding(both, 604800, 86400)
    print(f"  weekly TOTAL max: ${max(weekly):.2f}" if weekly else "  weekly TOTAL: no data")

    print("\n## Gate blocks + paused time (from auto-loop.log — rotated history may truncate)")
    pause_secs = int(os.environ.get("BUDGET_PAUSE_SECONDS", "1800"))
    counts = {"CLAUDE_5H": 0, "CODEX_5H": 0, "DAILY_TOTAL": 0, "WEEKLY_TOTAL": 0}
    pauses = 0
    try:
        with open(os.path.join(LOG_DIR, "auto-loop.log"), encoding="utf-8", errors="replace") as fh:
            for line in fh:
                m = re.search(r"\[GATE\] (CLAUDE_5H \+ CODEX_5H|CLAUDE_5H|CODEX_5H|DAILY_TOTAL|WEEKLY_TOTAL)", line)
                if m:
                    for g in counts:
                        if g in m.group(1):
                            counts[g] += 1
                    if "BOTH engines" in line or "CLAUDE_5H + CODEX_5H" in line:
                        pauses += 1
    except FileNotFoundError:
        print("  auto-loop.log missing — block counts unavailable")
    for g, n in counts.items():
        print(f"  {g}: {n} block line(s)")
    print(f"  approx paused time: {pauses} pause window(s) × {pause_secs}s = {pauses * pause_secs}s")

    print("\n## Operator interactive impact")
    try:
        with open(os.path.join(LOG_DIR, "operator-usage.json"), encoding="utf-8") as fh:
            op = json.load(fh)
        print(f"  latest snapshot: {json.dumps(op)[:200]}")
    except Exception:  # noqa: BLE001
        print("  no operator-usage snapshot available")
    limits = 0
    try:
        with open(os.path.join(LOG_DIR, "auto-loop.log"), encoding="utf-8", errors="replace") as fh:
            limits = sum(1 for line in fh if "[LIMIT] Claude 5h plan limit hit" in line)
    except FileNotFoundError:
        pass
    print(f"  plan-ceiling hits while the company ran ([LIMIT] lines): {limits}")
    print("  NOTE: snapshot history is not retained; impact beyond these signals is a data gap, not zero.")

    print("\nNo threshold is changed by this report — thresholds move only on a new operator decision.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
