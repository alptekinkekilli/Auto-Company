#!/usr/bin/env python3
"""Track whether cycles are actually getting leaner — and say when this watcher can be retired.

WHY THIS EXISTS. The per-cycle verdict answers "was THAT cycle heavy?". It cannot answer the
question the operator is actually asking while optimising: **is it getting better?** A single
BLOATED line is noise; a p90 that has not moved in forty cycles is a fact. Operator, 2026-08-02:
*"bu bloat'ları takip etmek ve ölçmek için watcher kurman lazım — optimize edene kadar bu watcher
çalışmalı."*

It is deliberately quiet. Today's recalibration exists because the old bars alerted on 41% of
cycles and taught everyone to scroll past; a trend watcher that chatters would repeat that
mistake one level up. It speaks on exactly three events:

  * **REGRESSION** — the window got materially worse than the one before it.
  * **TARGET MET** — the optimisation goal held for a full window. It says so once, and says
    that it can now be switched off. A watcher with no exit condition becomes furniture.
  * **--report** — asked explicitly by a human. Always prints, never notifies.

HISTORY. Audit lines are parsed out of `auto-loop.log` and appended to
`logs/turn-audit-history.ndjson`, keyed by session id so re-parsing the same log is idempotent.
The log is truncated and rotated; the history is the record, and it outlives it.

  bloat-trend.py [--app /app] [--window 15] [--report] [--dry-run]

TARGET (override with env): BLOATED rate <= 10% and p90 turns <= 55 across a full window.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import statistics as st
import sys
from datetime import datetime, timezone

AUDIT_RE = re.compile(
    r"\[TURN-AUDIT session=(?P<session>\S+) provider=(?P<provider>\S+) turns=(?P<turns>\d+) "
    r"dur=(?P<dur>\d+)s msgs_max=(?P<msgs>\d+) .*?floor_usd=(?P<usd>[\d.]+) "
    r"tool_wall_share=(?P<share>\d+)% .*?verdict=(?P<verdict>\w+)\]")
STAMP_RE = re.compile(r"^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]")
HISTORY = "logs/turn-audit-history.ndjson"
STATE = "logs/bloat-trend-state.json"

TARGET_BLOATED_PCT = float(os.environ.get("BLOAT_TARGET_PCT", "10"))
TARGET_P90_TURNS = float(os.environ.get("BLOAT_TARGET_P90_TURNS", "55"))
# A window has to move by more than noise before it is called a regression. 20% on p90 and a
# doubling of the bloated share are both large enough that a single unlucky cycle cannot cause
# them in a 15-cycle window.
REGRESS_P90_PCT = float(os.environ.get("BLOAT_REGRESS_P90_PCT", "20"))


def ingest(app: str) -> list[dict]:
    """Fold any new audit lines from the live log into the durable history."""
    hist_path = os.path.join(app, HISTORY)
    seen, rows = set(), []
    try:
        with open(hist_path, encoding="utf-8") as fh:
            for line in fh:
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                rows.append(r)
                seen.add(r["session"])
    except OSError:
        pass

    added = 0
    try:
        with open(os.path.join(app, "logs", "auto-loop.log"), encoding="utf-8", errors="replace") as fh:
            for line in fh:
                m = AUDIT_RE.search(line)
                if not m or m.group("session") in seen:
                    continue
                stamp = STAMP_RE.match(line)
                row = {"session": m.group("session"), "provider": m.group("provider"),
                       "turns": int(m.group("turns")), "dur": int(m.group("dur")),
                       "msgs": int(m.group("msgs")), "usd": float(m.group("usd")),
                       "tool_share": int(m.group("share")), "verdict": m.group("verdict"),
                       "at": stamp.group(1) if stamp else None}
                rows.append(row)
                seen.add(row["session"])
                added += 1
    except OSError:
        pass

    if added:
        try:
            os.makedirs(os.path.dirname(hist_path), exist_ok=True)
            with open(hist_path, "w", encoding="utf-8") as fh:
                for r in rows:
                    fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        except OSError as exc:
            print("could not persist history: %s" % exc, file=sys.stderr)
    return rows


# The stored `verdict` was computed by whatever thresholds were live when the cycle ran, and
# those changed on 2026-08-02. Comparing a window scored with the old bars against one scored
# with the new ones would measure the ruler, not the cycles — so the verdict is RECOMPUTED here
# from the raw numbers, with today's thresholds, for every row in every window.
TURNS_BLOATED = float(os.environ.get("TURN_AUDIT_TURNS_BLOATED", "65"))
DUR_BLOATED = float(os.environ.get("TURN_AUDIT_DUR_BLOATED", "675"))
USD_BLOATED = float(os.environ.get("TURN_AUDIT_USD_BLOATED", "5.00"))


def is_bloated(r: dict) -> bool:
    return r["turns"] > TURNS_BLOATED or r["dur"] >= DUR_BLOATED or r["usd"] >= USD_BLOATED


def summarise(rows: list[dict]) -> dict:
    turns = sorted(r["turns"] for r in rows)
    durs = sorted(r["dur"] for r in rows)
    usd = [r["usd"] for r in rows]
    def pct(v, p):
        return v[min(len(v) - 1, int(len(v) * p))] if v else 0
    return {"n": len(rows),
            "p50_turns": st.median(turns) if turns else 0,
            "p90_turns": pct(turns, 0.9),
            "p50_dur": st.median(durs) if durs else 0,
            "p90_dur": pct(durs, 0.9),
            "mean_usd": round(sum(usd) / len(usd), 2) if usd else 0,
            "sum_usd": round(sum(usd), 2),
            "bloated_pct": round(100.0 * sum(1 for r in rows if is_bloated(r)) / len(rows), 1) if rows else 0}


def notify(app: str, text: str) -> None:
    script = os.path.join(app, "scripts", "core", "telegram-notify.sh")
    if not os.path.exists(script):
        return
    env = dict(os.environ)
    try:
        for line in open(os.path.join(app, "logs", "runtime.env"), encoding="utf-8", errors="replace"):
            if line.startswith(("TELEGRAM_BOT_TOKEN=", "TELEGRAM_CHAT_ID=")):
                k, v = line.split("=", 1)
                env[k] = v.strip().strip('"').strip("'")
    except OSError:
        pass
    subprocess.run(["bash", script], input=text, text=True, env=env,
                   capture_output=True, timeout=45, check=False)


def fmt(label: str, cur: dict, prev: dict | None) -> str:
    def d(key, unit=""):
        if not prev or not prev["n"]:
            return "%s%s" % (cur[key], unit)
        delta = cur[key] - prev[key]
        arrow = "→" if abs(delta) < 1e-9 else ("↑" if delta > 0 else "↓")
        return "%s%s (%s %+.1f)" % (cur[key], unit, arrow, delta)
    return ("%s n=%d · p50 turns %s · p90 turns %s · p50 dur %ss · bloated %s%%\n"
            "  mean $%s · window total $%s" % (
                label, cur["n"], d("p50_turns"), d("p90_turns"), d("p50_dur"),
                d("bloated_pct"), cur["mean_usd"], cur["sum_usd"]))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", default=os.environ.get("AC_APP_DIR", "/app"))
    ap.add_argument("--window", type=int, default=int(os.environ.get("BLOAT_WINDOW", "15")))
    ap.add_argument("--report", action="store_true", help="print the trend for a human")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    rows = ingest(args.app)
    if len(rows) < args.window:
        print("history has %d cycles, need %d for a window — collecting" % (len(rows), args.window))
        return 0

    cur = summarise(rows[-args.window:])
    prev = summarise(rows[-2 * args.window:-args.window]) if len(rows) >= 2 * args.window else None

    print(fmt("current ", cur, prev))
    if prev:
        print(fmt("previous", prev, None))

    state_path = os.path.join(args.app, STATE)
    try:
        state = json.loads(open(state_path, encoding="utf-8").read())
    except (OSError, json.JSONDecodeError):
        state = {}

    lines: list[str] = []
    def hits_target(w: dict | None) -> bool:
        return bool(w) and w["n"] > 0 and w["bloated_pct"] <= TARGET_BLOATED_PCT \
            and w["p90_turns"] <= TARGET_P90_TURNS
    # TWO consecutive windows, not one. The optimisation work and the first good window
    # landed on the same day, and declaring victory on a single window right after the change
    # would be indistinguishable from a lucky fortnight. Thirty cycles is cheap; a premature
    # "you can switch this off" is not.
    target_met = hits_target(cur) and hits_target(prev)
    if hits_target(cur) and not hits_target(prev):
        print("target met in the current window only — needs the previous window too "
              "(%s: bloated %s%%, p90 turns %s)" % (
                  "no previous window yet" if not prev else "previous",
                  prev["bloated_pct"] if prev else "-", prev["p90_turns"] if prev else "-"))
    if target_met and not state.get("target_announced"):
        lines.append("✅ Turn-economy hedefi İKİ ARDIŞIK PENCEREDE tuttu (%d+%d cycle): "
                     "bloated %%%s ve %%%s (hedef ≤%%%s), p90 turns %s ve %s (hedef ≤%s)."
                     % (args.window, args.window, prev["bloated_pct"], cur["bloated_pct"],
                        TARGET_BLOATED_PCT, prev["p90_turns"], cur["p90_turns"], TARGET_P90_TURNS))
        lines.append("Bu izleyicinin işi bitti; kapatılabilir (post-cycle hook'tan çıkar).")
        state["target_announced"] = True
    elif not target_met:
        state["target_announced"] = False

    if prev and prev["p90_turns"]:
        worse_p90 = (cur["p90_turns"] - prev["p90_turns"]) / prev["p90_turns"] * 100 >= REGRESS_P90_PCT
        worse_bloat = cur["bloated_pct"] > max(prev["bloated_pct"] * 2, TARGET_BLOATED_PCT)
        # Both, deliberately: either alone flips on noise, and a watcher that cries wolf about
        # noise is exactly what this whole recalibration was fixing.
        if worse_p90 and worse_bloat and not state.get("regression_announced"):
            lines.append("📈 Cycle'lar AĞIRLAŞIYOR — son %d cycle vs önceki %d:" % (args.window, args.window))
            lines.append("  p90 turns %s → %s · bloated %%%s → %%%s · ortalama $%s → $%s"
                         % (prev["p90_turns"], cur["p90_turns"], prev["bloated_pct"],
                            cur["bloated_pct"], prev["mean_usd"], cur["mean_usd"]))
            state["regression_announced"] = True
        elif not (worse_p90 and worse_bloat):
            state["regression_announced"] = False

    if lines:
        text = "\n".join(lines)
        print("--- would notify ---" if args.dry_run else "--- notifying ---")
        print(text)
        if not args.dry_run:
            notify(args.app, text)
    elif not args.report:
        print("no trend event — silent")

    if not args.dry_run:
        try:
            with open(state_path, "w", encoding="utf-8") as fh:
                json.dump(state, fh, indent=1)
        except OSError:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
