#!/usr/bin/env python3
"""Deterministic daily cost audit → memories/cost-audit.md (turn-economy policy).

Runs BEFORE the Opportunity Analyst so the analyst reads measured numbers instead of
re-deriving them. Every figure here comes from a file on disk; the analyst's job is to
interpret, never to compute — a high-effort model asked to do arithmetic over logs is
both expensive and capable of inventing a plausible number.

Sources (all read-only):
  logs/spend-total.log            the one ledger (epoch engine run_id amount)
  logs/auto-loop.log              [COST] provenance, [TELEMETRY], [TURN-AUDIT], timeouts
  logs/.jcode/logs/jcode-*.log    per-turn prompt prefix, tool locking, tool calls
  logs/.jcode/mcp-schema-cache.json  advertised tool inventory per MCP server

What it deliberately does NOT do: judge, recommend, or write anything outside its own
output file. Findings are classified only as company-fixable vs infra so the analyst can
route them (the company can prune its own memories and change its own behaviour; it
cannot edit accounting code, runtime.env or the tool denylist — those are operator work).

Usage: cost-audit.py [--app /app] [--out memories/cost-audit.md] [--days 7]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import time
from collections import defaultdict

TS_RE = re.compile(r"^\[(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})\]")
TELEM_RE = re.compile(r"\[TELEMETRY\] engine=(\w+) model=(\S+) effort=(\S+) cost=(\S+)")
COST_EST_RE = re.compile(r"\[COST\] estimated \(uncalibrated model\)")
HINT_RE = re.compile(r"requested-model HINT")
TIMEOUT_RE = re.compile(r"Timed out after (\d+)s .*?cost: (\S+?)[,)]")
AUDIT_RE = re.compile(r"\[TURN-AUDIT ([^\]]+)\]")
PREFIX_RE = re.compile(r"Prompt prefix estimate: total=(\d+) tokens \(system=(\d+) tools=(\d+)\)")
LOCK_RE = re.compile(r"Locking tool list at (\d+) tools")
TOOLFIN_RE = re.compile(r"Tool finished: ([\w.-]+) in")


def utc_day(epoch: float) -> str:
    return time.strftime("%Y-%m-%d", time.gmtime(epoch))


def read_ledger(path: str, days: int) -> dict:
    cutoff = time.time() - days * 86400
    by_day: dict[str, list] = defaultdict(list)
    malformed = 0
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                parts = line.split()
                if len(parts) < 4:
                    if line.strip():
                        malformed += 1
                    continue
                try:
                    epoch, amount = int(parts[0]), float(parts[3])
                except ValueError:
                    malformed += 1
                    continue
                if epoch >= cutoff:
                    by_day[utc_day(epoch)].append((epoch, parts[1], parts[2], amount))
    except OSError:
        return {"error": f"ledger unreadable: {path}", "by_day": {}, "malformed": 0}
    return {"by_day": dict(by_day), "malformed": malformed}


def read_loop_log(path: str, today: str) -> dict:
    """Cycle-level facts for TODAY: costs, provenance, timeouts, turn audits."""
    out = {
        "cycles": [], "timeouts": [], "estimated_rows": 0, "hinted_rows": 0,
        "audits": [], "day": today,
    }
    pending_est = pending_hint = False
    try:
        fh = open(path, encoding="utf-8", errors="replace")
    except OSError:
        out["error"] = f"loop log unreadable: {path}"
        return out
    with fh:
        for line in fh:
            m = TS_RE.match(line)
            if not m or m.group(1) != today:
                continue
            if COST_EST_RE.search(line):
                pending_est = True
                if HINT_RE.search(line):
                    pending_hint = True
            mt = TELEM_RE.search(line)
            if mt:
                engine, model, effort, cost = mt.groups()
                out["cycles"].append({
                    "time": m.group(2), "engine": engine, "model": model,
                    "effort": effort, "cost": cost,
                    "estimated": pending_est, "hinted": pending_hint,
                })
                out["estimated_rows"] += 1 if pending_est else 0
                out["hinted_rows"] += 1 if pending_hint else 0
                pending_est = pending_hint = False
            mto = TIMEOUT_RE.search(line)
            if mto:
                out["timeouts"].append({"time": m.group(2), "seconds": mto.group(1),
                                        "cost": mto.group(2)})
            ma = AUDIT_RE.search(line)
            if ma:
                fields = dict(p.split("=", 1) for p in ma.group(1).split() if "=" in p)
                fields["time"] = m.group(2)
                out["audits"].append(fields)
    return out


def read_jcode_log(path: str) -> dict:
    prefixes, locks, tools = [], [], defaultdict(int)
    try:
        fh = open(path, encoding="utf-8", errors="replace")
    except OSError:
        return {"error": f"jcode log unreadable: {path}"}
    with fh:
        for line in fh:
            mp = PREFIX_RE.search(line)
            if mp:
                prefixes.append(tuple(int(x) for x in mp.groups()))
            ml = LOCK_RE.search(line)
            if ml:
                locks.append(int(ml.group(1)))
            mt = TOOLFIN_RE.search(line)
            if mt:
                tools[mt.group(1)] += 1
    return {"prefixes": prefixes, "locks": locks, "tools": dict(tools)}


def read_tool_inventory(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {}
    servers = data.get("servers", {})
    return {name: [t["name"] for t in info.get("tools", [])] for name, info in servers.items()}


def fmt_money(x: float) -> str:
    return f"${x:,.2f}"


def build_report(app: str, days: int) -> str:
    today = time.strftime("%Y-%m-%d", time.gmtime())
    logs = os.path.join(app, "logs")
    ledger = read_ledger(os.path.join(logs, "spend-total.log"), days)
    loop = read_loop_log(os.path.join(logs, "auto-loop.log"), today)
    jc = read_jcode_log(os.path.join(logs, ".jcode", "logs", f"jcode-{today}.log"))
    inventory = read_tool_inventory(os.path.join(logs, ".jcode", "mcp-schema-cache.json"))

    L = [f"# Cost audit — {today} (UTC, generated deterministically)", ""]
    L.append("Every number below is read from a file; nothing here is estimated by a model.")
    L.append("Budget figures are notional/API-equivalent (subscription), not billed cash.")
    L.append("")

    # --- 1. Ledger trend
    L.append("## 1. Claude ledger by day")
    L.append("")
    L.append("| day | cycles | total | avg/cycle |")
    L.append("|---|---|---|---|")
    for day in sorted(ledger.get("by_day", {})):
        rows = ledger["by_day"][day]
        total = sum(r[3] for r in rows)
        L.append(f"| {day} | {len(rows)} | {fmt_money(total)} | {fmt_money(total/len(rows))} |")
    if ledger.get("malformed"):
        L.append("")
        L.append(f"**{ledger['malformed']} malformed ledger row(s)** — the weekly walk aborts on these.")
    L.append("")

    # --- 2. Today's cycles + provenance
    L.append("## 2. Today's cycles and how each price was obtained")
    L.append("")
    if loop.get("error"):
        L.append(f"NOT MEASURED — {loop['error']}")
    else:
        L.append("| time | engine | effort | cost | priced from |")
        L.append("|---|---|---|---|---|")
        real = phantom = 0.0
        for c in loop["cycles"]:
            if c["hinted"]:
                basis = "requested-model HINT (cycle was killed)"
            elif c["estimated"]:
                basis = "**UNKNOWN MODEL x5 — phantom**"
            else:
                basis = "done event (calibrated)"
            L.append(f"| {c['time']} | {c['engine']} | {c['effort']} | {c['cost']} | {basis} |")
            try:
                amt = float(c["cost"])
            except ValueError:
                continue
            if c["estimated"] and not c["hinted"]:
                phantom += amt
            else:
                real += amt
        L.append("")
        L.append(f"- Calibrated/hinted total: **{fmt_money(real)}**")
        L.append(f"- Conservative-row (phantom) total: **{fmt_money(phantom)}**"
                 + ("  ← inflates the 5h window without matching real usage" if phantom else ""))
        if loop["timeouts"]:
            L.append(f"- Timeouts today: {len(loop['timeouts'])} "
                     f"({', '.join(t['time'] for t in loop['timeouts'])}) — a killed cycle "
                     "loses its work AND its calibrated price.")
    L.append("")

    # --- 3. Turn economy
    L.append("## 3. Turn economy (from the loop's own [TURN-AUDIT] lines)")
    L.append("")
    if loop.get("audits"):
        L.append("| time | turns | msgs_max | cache_read | floor_usd | verdict |")
        L.append("|---|---|---|---|---|---|")
        for a in loop["audits"]:
            L.append(f"| {a.get('time','?')} | {a.get('turns','?')} | {a.get('msgs_max','?')} "
                     f"| {a.get('cache_read','?')} | {a.get('floor_usd','?')} | {a.get('verdict','?')} |")
        bad = [a for a in loop["audits"] if a.get("verdict") not in ("ok", None)]
        if bad:
            L.append("")
            L.append(f"**{len(bad)} cycle(s) flagged CHATTY/BLOATED** — context grew past the "
                     "point where a cycle should have persisted findings and ended.")
    else:
        L.append("No [TURN-AUDIT] lines today (no jcode-claude cycle yet, or the hook is absent).")
    L.append("")

    # --- 4. Per-turn overhead
    L.append("## 4. Per-turn prompt overhead")
    L.append("")
    if jc.get("prefixes"):
        uniq = sorted(set(jc["prefixes"]))
        for total, system, tools_tok in uniq:
            L.append(f"- prefix **{total:,} tokens** = system {system:,} + **tool definitions {tools_tok:,}**")
        L.append(f"- tool list locked at: {sorted(set(jc['locks']))} tools")
        L.append("")
        L.append("Every turn re-reads this prefix. A 20-turn cycle pays the tool-definition "
                 "line ~20 times.")
    else:
        L.append("NOT MEASURED — no jcode session in today's log (e.g. all cycles ran on the CLI).")
    L.append("")

    # --- 5. Tool surface
    L.append("## 5. Advertised vs actually called tools")
    L.append("")
    if inventory:
        used = jc.get("tools", {})
        L.append("| server | advertised | called today | never called |")
        L.append("|---|---|---|---|")
        for srv, names in sorted(inventory.items()):
            called = {n for n in used if n.startswith(f"mcp__{srv}__")}
            L.append(f"| {srv} | {len(names)} | {len(called)} | {len(names) - len(called)} |")
        L.append("")
        L.append("An advertised tool costs prompt tokens on every turn whether or not it is "
                 "ever called. Trimming is a denylist change — operator work, not company work.")
    else:
        L.append("NOT MEASURED — MCP schema cache unreadable.")
    L.append("")

    # --- 6. Routing for the analyst
    L.append("## 6. How to route what you find (for the Opportunity Analyst)")
    L.append("")
    L.append("**Company-fixable — may go into the pasted directive's `## Ops hygiene` block:**")
    L.append("- consensus.md / memory bloat → prune resolved material into `docs/<role>/`")
    L.append("- cycles flagged CHATTY/BLOATED, or timeouts → persist findings and end the "
             "cycle earlier instead of riding into the 900s kill")
    L.append("- long command output flowing into context instead of a file + `tail`")
    L.append("")
    L.append("**Infra — NEVER a directive; raise an OPREQ instead:**")
    L.append("- budget/accounting code, the tier ladder, LOOP_INTERVAL, the MCP tool denylist,")
    L.append("  the hold mechanism, anything requiring a redeploy.")
    L.append("- Reason: a directive telling the company to edit its own brakes is exactly the "
             "failure mode the guardrail invariant exists to prevent.")
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", default="/app")
    ap.add_argument("--out", default=None)
    ap.add_argument("--days", type=int, default=7)
    args = ap.parse_args()

    report = build_report(args.app, args.days)
    out = args.out or os.path.join(args.app, "memories", "cost-audit.md")
    tmp = out + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as fh:
            fh.write(report)
        os.replace(tmp, out)
    except OSError as exc:
        print(f"cannot write {out}: {exc}")
        return 1
    print(f"cost audit written: {out} ({len(report)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
