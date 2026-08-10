#!/usr/bin/env python3
"""APP-263 calibration report — run after 14 complete UTC days of four-gate data.

**Regime change mid-window (APP-263 follow-up, 2026-08-10, commit 4d488c5):**
the CLAUDE_5H_BUDGET_USD / CODEX_5H_BUDGET_USD per-engine pause gate was
retired (left empty in runtime.env — code kept, never gates). The live
thresholds are now TOTAL_DAILY_BUDGET_USD / TOTAL_WEEKLY_BUDGET_USD only,
shared across both engines, with ROUTER_ALTERNATE balancing them and the tier
ladder keyed on each engine's own real DAILY spend instead of the retired 5h
figure. A report whose observation window straddles CUTOVER_EPOCH (as the
original 2026-07-31 -> 2026-08-13 window does) is measuring TWO different
policies, not one — this script says so explicitly rather than blending them
into one misleading percentile.

Produces, over the observation window:
  - per-engine 5h p50/p90/p95/max, PRE-CUTOVER ONLY (sliding 5h windows
    sampled hourly — the real plan anchors are not retained historically, so
    this is a declared approximation of window peaks, not a replay of exact
    plan windows). RETIRED as a calibration target since CUTOVER_EPOCH: kept
    for historical reference, not because a threshold still reads it.
  - per-engine DAILY p50/p90/p95/max, whole window (each engine's own spend
    per complete UTC day) — this is what the live tier ladder actually keys
    on now; the original report had no per-engine daily breakdown because the
    5h figures served that role before the follow-up.
  - combined daily p50/p90/p95/max (UTC calendar days) — the actual
    TOTAL_DAILY_BUDGET_USD gate input, live before and after the cutover.
  - rolling weekly maximum (sliding 7x24h sampled daily) — the actual
    TOTAL_WEEKLY_BUDGET_USD gate input, live before and after the cutover.
  - block counts grouped by gate type (CLAUDE_5H / CODEX_5H / DAILY_TOTAL /
    WEEKLY_TOTAL, from [GATE] log lines), CLAUDE_5H/CODEX_5H split
    pre/post-cutover so a drop to zero after CUTOVER_EPOCH reads as
    retirement, not as "the gate got better calibrated."
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

# The moment the new code was actually running in prod (first [BUDGET] line
# under commit 4d488c5, verified live in the auto-loop.log during the
# 2026-08-10 held-boot -> canary -> release sequence). Override via env for
# testing; this is a one-time historical marker, not a config knob.
CUTOVER_EPOCH = int(os.environ.get(
    "BUDGET_5H_RETIREMENT_EPOCH",
    dt.datetime(2026, 8, 10, 8, 1, 43, tzinfo=dt.timezone.utc).timestamp(),
))


def split_by_cutover(entries: list[tuple[int, float]]) -> tuple[list[tuple[int, float]], list[tuple[int, float]]]:
    """(pre-cutover, post-cutover) — the 5h gate stopped mattering at CUTOVER_EPOCH."""
    pre = [x for x in entries if x[0] < CUTOVER_EPOCH]
    post = [x for x in entries if x[0] >= CUTOVER_EPOCH]
    return pre, post


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


def sliding(entries: list[tuple[int, float]], span: int, step: int, until: int | None = None) -> list[float]:
    """Sliding-window sums, sampled every `step` seconds up to `until` (default NOW).

    Pass `until=CUTOVER_EPOCH` for a series that should stop at the regime
    change rather than trailing off into zero-filled post-cutover samples
    (post-cutover 5h entries are excluded from the `entries` list already, so
    without a bound the tail would silently understate the pre-cutover peaks).
    """
    if not entries:
        return []
    end = NOW if until is None else until
    samples = []
    t = SINCE + span
    while t <= end:
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

    cutover_dt = dt.datetime.fromtimestamp(CUTOVER_EPOCH, dt.timezone.utc)
    if SINCE < CUTOVER_EPOCH < NOW:
        print(f"## ⚠ Regime change inside this window: {cutover_dt:%Y-%m-%d %H:%M UTC}")
        print("   The CLAUDE_5H/CODEX_5H per-engine pause gate was retired at that instant")
        print("   (APP-263 follow-up, commit 4d488c5) — TOTAL_DAILY/WEEKLY_BUDGET_USD is now")
        print("   the only live threshold. Sections below are split pre/post where the")
        print("   distinction matters; do not read a pre/post difference as behavior change")
        print("   when it is actually policy change.\n")
    elif CUTOVER_EPOCH <= SINCE:
        print("   (Whole window is post-cutover: 5h gate was already retired throughout.)\n")

    claude_pre, claude_post = split_by_cutover(claude)
    codex_pre, codex_post = split_by_cutover(codex)

    print("## Per-engine 5h — PRE-CUTOVER ONLY (sliding 5h windows, hourly samples — approximation, real plan anchors not retained)")
    print("   RETIRED as a calibration target since the cutover above; kept for historical")
    print("   reference only — no threshold reads this any more.")
    print(stats_line("claude 5h", sliding(claude_pre, 18000, 3600, until=min(CUTOVER_EPOCH, NOW))))
    print(stats_line("codex  5h", sliding(codex_pre, 18000, 3600, until=min(CUTOVER_EPOCH, NOW))))
    if claude_post or codex_post:
        print(f"   ({len(claude_post)} claude / {len(codex_post)} codex spend row(s) exist after the "
              "cutover but are excluded here — they're real spend, just not calibration data "
              "for a gate that no longer exists.)")

    print("\n## Per-engine DAILY (complete UTC days, whole window) — the live tier ladder's actual input since the cutover")
    print(stats_line("claude daily", daily_buckets(claude)))
    print(stats_line("codex  daily", daily_buckets(codex)))

    print("\n## Combined daily (complete UTC days) — the live TOTAL_DAILY_BUDGET_USD gate input")
    print(stats_line("daily TOTAL", daily_buckets(both)))

    print("\n## Rolling weekly (sliding 7×24h, daily samples) — the live TOTAL_WEEKLY_BUDGET_USD gate input")
    weekly = sliding(both, 604800, 86400)
    print(f"  weekly TOTAL max: ${max(weekly):.2f}" if weekly else "  weekly TOTAL: no data")

    print("\n## Gate blocks + paused time (from auto-loop.log — rotated history may truncate)")
    pause_secs = int(os.environ.get("BUDGET_PAUSE_SECONDS", "1800"))
    # CLAUDE_5H/CODEX_5H split pre/post cutover: a drop to zero after CUTOVER_EPOCH is
    # the gate being retired, not the gate suddenly working better. DAILY_TOTAL/
    # WEEKLY_TOTAL are still live throughout, so they stay single whole-window counts.
    counts_5h = {"CLAUDE_5H": [0, 0], "CODEX_5H": [0, 0]}  # [pre, post]
    counts_total = {"DAILY_TOTAL": 0, "WEEKLY_TOTAL": 0}
    # Two DISTINCT pause causes, both printed as "affected: BOTH engines" in the
    # loop's own [GATE] line: the retired CLAUDE_5H+CODEX_5H combo, and a live
    # DAILY_TOTAL/WEEKLY_TOTAL breach. m.group(1) tells them apart precisely —
    # matching on the "BOTH engines" substring alone (the original version of
    # this script) would silently mix them.
    pauses_5h_pre = pauses_5h_post = 0
    pauses_total_gate = 0
    ts_re = re.compile(r"^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]")
    try:
        with open(os.path.join(LOG_DIR, "auto-loop.log"), encoding="utf-8", errors="replace") as fh:
            for line in fh:
                m = re.search(r"\[GATE\] (CLAUDE_5H \+ CODEX_5H|CLAUDE_5H|CODEX_5H|DAILY_TOTAL|WEEKLY_TOTAL)", line)
                if not m:
                    continue
                tm = ts_re.match(line)
                try:
                    e = int(dt.datetime.strptime(tm.group(1), "%Y-%m-%d %H:%M:%S")
                             .replace(tzinfo=dt.timezone.utc).timestamp()) if tm else None
                except ValueError:
                    e = None
                is_post = e is not None and e >= CUTOVER_EPOCH
                gate = m.group(1)
                for g in counts_5h:
                    if g in gate:
                        counts_5h[g][1 if is_post else 0] += 1
                if gate == "CLAUDE_5H + CODEX_5H":
                    pauses_5h_post += 1 if is_post else 0
                    pauses_5h_pre += 0 if is_post else 1
                elif gate in counts_total:
                    counts_total[gate] += 1
                    pauses_total_gate += 1
    except FileNotFoundError:
        print("  auto-loop.log missing — block counts unavailable")
    for g, (pre_n, post_n) in counts_5h.items():
        note = "" if not post_n else "  <- unexpected: this gate is retired, these should be 0"
        print(f"  {g}: {pre_n} pre-cutover / {post_n} post-cutover block line(s){note}")
    for g, n in counts_total.items():
        print(f"  {g}: {n} block line(s) (whole window — this gate stayed live throughout)")
    print(f"  approx paused time, CLAUDE_5H+CODEX_5H combo (retired gate): "
          f"{pauses_5h_pre} pre-cutover + {pauses_5h_post} post-cutover window(s) × {pause_secs}s "
          f"= {(pauses_5h_pre + pauses_5h_post) * pause_secs}s")
    print(f"  approx paused time, DAILY_TOTAL/WEEKLY_TOTAL (still-live gate): "
          f"{pauses_total_gate} window(s) × {pause_secs}s = {pauses_total_gate * pause_secs}s")

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

    print("\nLive thresholds: TOTAL_DAILY_BUDGET_USD / TOTAL_WEEKLY_BUDGET_USD only "
          "(CLAUDE_5H_BUDGET_USD / CODEX_5H_BUDGET_USD retired 2026-08-10, APP-263 follow-up).")
    print("No threshold is changed by this report — thresholds move only on a new operator decision.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
