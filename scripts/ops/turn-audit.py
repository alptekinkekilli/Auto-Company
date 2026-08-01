#!/usr/bin/env python3
"""Turn-level waste accounting over a jcode daily log (turn-economy policy, sec. 2).

The cost unit of an LLM agent is the TURN: every tool round-trip re-bills the whole
context and produces reasoning tokens. This classifier reads jcode's own daily log
(logs/.jcode/logs/jcode-YYYY-MM-DD.log) and reports, per session: turn count, context
growth, cache traffic, a priced floor (sonnet-5 1h-cache tariff — in/out tokens are
redacted in the log, so this UNDERSTATES real cost by the in/out share), the tool
census, and a wait-share estimate (bash calls whose wall time dominates the turn and
whose command smells like sleep/poll cannot be told apart here because commands are
redacted — the proxy is tool wall time vs turn wall time).

Usage:
  turn-audit.py <jcode-daily-log>                 # all sessions, human-readable
  turn-audit.py <jcode-daily-log> --summary-last  # ONE machine line for the newest
                                                  # session (post-cycle hook)

Summary line fields:
  TURN-AUDIT session=<id> provider=<prv> turns=<n> dur=<s> msgs_max=<n>
  cache_read=<tok> cache_write=<tok> floor_usd=<x> tool_wall_share=<pct>
  fast_gaps=<n>/<n> verdict=<ok|CHATTY|BLOATED>

Verdicts (advisory, thresholds from the 2026-08-01 baseline):
  CHATTY  — turns > 60 in one cycle (cycle #2 timed out at 73)
  BLOATED — msgs_max > 120 (context ~200K+ = premium-tariff territory)
"""
import re
import sys
from datetime import datetime
from collections import defaultdict

TS = re.compile(r"^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\.(\d{3})\]")
SES = re.compile(r"\[ses:(session_[a-z]+_\d+)\|prv:(\w+)\|mod:(\w[\w.-]*)\]")
STREAM = re.compile(r"AGENT_PROVIDER_STREAM_LIFECYCLE.*?cache_read=(\d+) cache_write=(\d+)")
APICALL = re.compile(r"API call starting: (\d+) messages, (\d+) tools")
TOOLFIN = re.compile(r"Tool finished: (\w+) in ([\d.]+)s")


def ts_of(line):
    m = TS.match(line)
    if not m:
        return None
    return datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S").timestamp() + int(m.group(2)) / 1000


def scan(path):
    sessions = defaultdict(lambda: {
        "provider": "", "model": "", "turns": 0, "first": None, "last": None,
        "cache_read": 0, "cache_write": 0, "msgs_max": 0,
        "tools": defaultdict(lambda: [0, 0.0]), "api_times": [],
    })
    for line in open(path, errors="replace"):
        m = SES.search(line)
        if not m:
            continue
        sid, prv, mod = m.groups()
        s = sessions[sid]
        s["provider"], s["model"] = prv, mod
        t = ts_of(line)
        if t:
            s["first"] = s["first"] or t
            s["last"] = t
        ma = APICALL.search(line)
        if ma:
            s["turns"] += 1
            s["msgs_max"] = max(s["msgs_max"], int(ma.group(1)))
            if t:
                s["api_times"].append(t)
        ms = STREAM.search(line)
        if ms:
            s["cache_read"] += int(ms.group(1))
            s["cache_write"] += int(ms.group(2))
        mt = TOOLFIN.search(line)
        if mt:
            s["tools"][mt.group(1)][0] += 1
            s["tools"][mt.group(1)][1] += float(mt.group(2))
    return {k: v for k, v in sessions.items() if v["turns"]}


def floor_usd(s):
    # sonnet-5 $/Mtok: cache-write(1h) 6, cache-read 0.30 — in/out are redacted in
    # the log, so this is a FLOOR, not the bill.
    return (s["cache_write"] * 6 + s["cache_read"] * 0.30) / 1e6


def summary_line(sid, s):
    dur = (s["last"] - s["first"]) if s["first"] else 0
    gaps = [b - a for a, b in zip(s["api_times"], s["api_times"][1:])]
    fast = sum(1 for g in gaps if g < 60)
    tool_wall = sum(c[1] for c in s["tools"].values())
    share = (100.0 * tool_wall / dur) if dur else 0.0
    verdict = "ok"
    if s["msgs_max"] > 120:
        verdict = "BLOATED"
    elif s["turns"] > 60:
        verdict = "CHATTY"
    return (
        f"TURN-AUDIT session={sid} provider={s['provider']} turns={s['turns']} "
        f"dur={dur:.0f}s msgs_max={s['msgs_max']} cache_read={s['cache_read']} "
        f"cache_write={s['cache_write']} floor_usd={floor_usd(s):.2f} "
        f"tool_wall_share={share:.0f}% fast_gaps={fast}/{len(gaps)} verdict={verdict}"
    )


def main():
    path = sys.argv[1]
    sessions = scan(path)
    if not sessions:
        print("TURN-AUDIT no sessions found")
        return
    if "--summary-last" in sys.argv:
        sid = max(sessions, key=lambda k: sessions[k]["first"] or 0)
        print(summary_line(sid, sessions[sid]))
        return
    for sid, s in sorted(sessions.items(), key=lambda kv: kv[1]["first"] or 0):
        print(summary_line(sid, s))
        tools = sorted(s["tools"].items(), key=lambda kv: -kv[1][0])
        print("  tools: " + ", ".join(f"{n}x{c[0]} ({c[1]:.0f}s)" for n, c in tools[:10]))


if __name__ == "__main__":
    main()
