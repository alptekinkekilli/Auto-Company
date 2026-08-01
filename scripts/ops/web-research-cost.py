#!/usr/bin/env python3
"""What web research actually costs a cycle — measured from the kept ndjson streams.

The question this answers: when an agent researches a website, how many turns does it
spend and how many tokens does that burn? The intuition "a fetch costs one fetch" is
wrong on two counts, and both are visible in the stream:

  1. A tool RESULT enters the context and is then re-read on EVERY later turn of that
     cycle. So a 60 KB page fetched at turn 5 of a 40-turn cycle is not paid once — it is
     paid ~35 times as cache-read. Cost therefore scales with (output size x turns
     REMAINING), which is why one fat fetch early is far worse than the same fetch late.
  2. Each tool call is its own turn: the whole conversation is re-sent to get the next
     decision. Ten small fetches cost ten context re-reads regardless of payload.

Reads logs/cycle-ndjson/*.ndjson (the loop keeps the last 20 cycles) and, for each:
tool census, per-tool output bytes, the turn index each call landed on, and the
resulting "residual cost" estimate = output_tokens x turns_after_it.

Usage:
  web-research-cost.py [--app /app] [--top 12] [--json]
"""
from __future__ import annotations

import argparse
import glob
import json
import os
from collections import defaultdict

# Tools that pull EXTERNAL content into the context. Everything else (read, write, bash on
# local files) is cheap-ish and locally bounded; these are the ones that can drop tens of KB
# of someone else's HTML into a conversation that then re-reads it for the rest of the cycle.
WEB_TOOLS = ("webfetch", "websearch", "web_fetch", "web_search")
WEB_PREFIXES = ("mcp__browseros__",)

# Rough bytes->tokens for mixed Turkish/HTML text. Deliberately conservative: understating
# the divisor would overstate the problem, and this number is used to argue for changes.
BYTES_PER_TOKEN = 3.5
# sonnet-5 cache-read $/token; a re-read of context is billed at this rate.
CACHE_READ_USD_PER_TOKEN = 0.30 / 1_000_000


def is_web(name: str) -> bool:
    return name in WEB_TOOLS or any(name.startswith(p) for p in WEB_PREFIXES)


def analyse(path: str) -> dict | None:
    turns = 0
    calls = []  # {name, out_bytes, turn}
    pending = {}
    try:
        fh = open(path, encoding="utf-8", errors="replace")
    except OSError:
        return None
    with fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            t = ev.get("type")
            if t == "tokens":
                turns += 1
            elif t == "tool_start":
                pending[ev.get("id") or ev.get("name")] = ev.get("name", "?")
            elif t == "tool_done":
                name = ev.get("name") or pending.get(ev.get("id"), "?")
                out = ev.get("output")
                size = len(out if isinstance(out, str) else json.dumps(out or ""))
                calls.append({"name": name, "bytes": size, "turn": turns})
    if not turns and not calls:
        return None
    return {"file": os.path.basename(path), "turns": turns, "calls": calls}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", default=os.environ.get("AC_APP_DIR", "/app"))
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(args.app, "logs", "cycle-ndjson", "*.ndjson")))
    cycles = [c for c in (analyse(f) for f in files) if c]
    if not cycles:
        print("no cycle ndjson streams found — nothing measured")
        return 1

    tool_totals = defaultdict(lambda: {"n": 0, "bytes": 0})
    web_rows = []
    for c in cycles:
        for call in c["calls"]:
            tt = tool_totals[call["name"]]
            tt["n"] += 1
            tt["bytes"] += call["bytes"]
            # Residual cost is computed for EVERY tool, not just the web ones. The first
            # version of this script scored only webfetch/browseros and reported $0.34,
            # which was true and misleading: it silently excluded the biggest single
            # context source in the data (Airtable table dumps, ~29 KB per call). A cost
            # analysis that pre-filters by category answers the question you assumed
            # instead of the one you asked.
            if True:
                remaining = max(0, c["turns"] - call["turn"])
                tokens = call["bytes"] / BYTES_PER_TOKEN
                web_rows.append({
                    "cycle": c["file"], "tool": call["name"], "bytes": call["bytes"],
                    "external": is_web(call["name"]),
                    "turn": call["turn"], "turns_total": c["turns"], "rereads": remaining,
                    "tokens": round(tokens),
                    "residual_usd": round(tokens * remaining * CACHE_READ_USD_PER_TOKEN, 4),
                })

    if args.json:
        print(json.dumps({"cycles": len(cycles), "web_calls": web_rows}, ensure_ascii=False))
        return 0

    n_turns = sum(c["turns"] for c in cycles)
    n_calls = sum(len(c["calls"]) for c in cycles)
    all_calls = web_rows
    web_calls = [r for r in web_rows if r["external"]]
    web_bytes = sum(r["bytes"] for r in web_calls)
    residual = sum(r["residual_usd"] for r in web_calls)
    total_residual = sum(r["residual_usd"] for r in all_calls)
    by_tool = defaultdict(float)
    for r in all_calls:
        by_tool[r["tool"]] += r["residual_usd"]

    print(f"cycles analysed: {len(cycles)}   turns: {n_turns}   tool calls: {n_calls}")
    print(f"web/external calls: {len(web_calls)}  ({web_bytes:,} bytes pulled into context)")
    print(f"estimated re-read cost of that content: ${residual:,.2f}")
    print(f"re-read cost of ALL tool output: ${total_residual:,.2f}"
          f"   <- web share: {100*residual/max(total_residual,1e-9):.0f}%")
    print()
    print("RE-READ COST BY TOOL (the ranking that actually matters)")
    for name, usd in sorted(by_tool.items(), key=lambda kv: -kv[1])[:8]:
        print(f"  {name[:44]:<46} ${usd:>7.2f}")
    print()

    print("TOOL CENSUS (by call count)")
    print(f"{'tool':<42} {'calls':>6} {'total bytes':>13} {'avg':>9}")
    for name, tt in sorted(tool_totals.items(), key=lambda kv: -kv[1]["n"])[:args.top]:
        mark = " *" if is_web(name) else ""
        print(f"{name[:40]:<42} {tt['n']:>6} {tt['bytes']:>13,} {tt['bytes']//max(1,tt['n']):>9,}{mark}")
    print("  (* = pulls external content into the context)")
    print()

    if web_calls:
        print("WORST INDIVIDUAL CALLS (output size x turns it is re-read afterwards)")
        print(f"{'cycle':<26} {'tool':<26} {'bytes':>8} {'turn':>5} {'re-reads':>9} {'~cost':>8}")
        for r in sorted(all_calls, key=lambda r: -r["residual_usd"])[:args.top]:
            print(f"{r['cycle'][:24]:<26} {r['tool'][:24]:<26} {r['bytes']:>8,} "
                  f"{r['turn']:>5} {r['rereads']:>9} {r['residual_usd']:>8.3f}")
        print()
        big = [r for r in all_calls if r["bytes"] > 20000]
        early = [r for r in all_calls if r["rereads"] >= 20]
        print(f"calls dumping >20 KB into context: {len(big)}")
        print(f"calls made early enough to be re-read 20+ times: {len(early)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
