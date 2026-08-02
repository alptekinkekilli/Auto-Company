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

Verdicts (advisory), RECALIBRATED 2026-08-02 against 34 measured cycles.

The 40-turn / 80-message bars fired on **14 of 34 cycles (41%)**. An alarm that fires on
two cycles in five is not a signal; the operator learns to scroll past it, and the one
cycle that actually mattered arrives looking exactly like the noise. Two defects, both
visible only once the distribution was plotted:

  * The bars sat inside normal behaviour. Measured: turns p50=34, p75=49, p90=65;
    msgs p50=69, p75=102, p90=130. An 80-message bar is below the 75th percentile.
  * `msgs_max` is not an independent signal — it is almost exactly 2x turns in every
    cycle (40/81, 46/92, 78/156). Two thresholds on one underlying quantity double the
    false-alarm rate and add nothing.

What actually distinguishes the harmful cycles is not chattiness but RISK: the tail runs
601-893s against a 900s watchdog (one was killed by it, losing its tail work) and costs
$3.2-6.9. So the verdict is now anchored to that, and msgs_max is reported but no longer
judged:

  CHATTY  — turns > 55                      (~p80: talkative, still finishing safely)
  BLOATED — turns > 65 (~p90), OR dur >= 675s (75% of the 900s watchdog), OR
            floor_usd >= 5.00               (the tail that actually costs)

Note the divergence this creates with Runtime Guardrail 7's "~40 tool calls": the measured
median cycle is 34 turns and healthy cycles run to ~50. The guardrail is advisory prose;
this is the feedback signal, and a signal calibrated to a number reality never respects is
worthless. Fix the prose or the reality — do not blunt the instrument.

Loosening these is loosening a measurement, not a policy: change them only with new
distribution evidence, and say what the distribution was.
"""
import os
import re
import sys
from datetime import datetime
from collections import defaultdict

# Verdict thresholds, named so a change is visible in a diff and testable.
TURNS_CHATTY = int(os.environ.get("TURN_AUDIT_TURNS_CHATTY", "55"))
TURNS_BLOATED = int(os.environ.get("TURN_AUDIT_TURNS_BLOATED", "65"))
# 75% of the 900s watchdog: past here a cycle is at real risk of being killed and losing
# its tail work, which is the expensive failure this audit exists to anticipate.
DUR_BLOATED = float(os.environ.get("TURN_AUDIT_DUR_BLOATED", "675"))
USD_BLOATED = float(os.environ.get("TURN_AUDIT_USD_BLOATED", "5.00"))

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
    # msgs_max is still reported — it is useful when reading one cycle — but it no longer
    # votes: it tracks turns at ~2x and was only ever a second vote for the same fact.
    verdict = "ok"
    if (s["turns"] > TURNS_BLOATED or dur >= DUR_BLOATED or floor_usd(s) >= USD_BLOATED):
        verdict = "BLOATED"
    elif s["turns"] > TURNS_CHATTY:
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
