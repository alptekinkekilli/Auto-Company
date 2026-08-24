#!/usr/bin/env python3
"""Per-cycle tool-consultation ledger — the data behind the cockpit's text-only
"Tool Analytics" panel (operator request, 2026-08-03).

WHY. cycle-ndjson retention is ~20 files (half a day), so any multi-day view of "how
often does the company actually consult ctx7 / Airtable / Linear / BrowserOS" needs a
durable ledger. Same architecture as turn-audit-history.ndjson: parse the finished
cycle's ndjson at the loop's return moment, append ONE small JSON line, never delete.

COUNTING. Tool calls are reassembled from jcode's event stream (tool_start + streamed
tool_input deltas — measured 2026-08-03: inputs arrive as fragments, tool_exec carries
no input). Categories, by bash-command substring or MCP tool name:
  ctx7        "ctx7" in the command (the find-docs skill's whole surface)
  airtable_r  airtable-read.py | mcp__airtable__* without update/create/delete/upload
  airtable_w  airtable-write.py | mcp__airtable__* with    update/create/delete/upload
  linear      "linear" in command or tool name (linear-track.py, api.linear.app, MCPs)
  browser     site-contact-evidence | browseros (gateway renders)
A call lands in every category it matches (a curl to api.linear.app piped through
airtable-read.py would double-count — no such command exists; keep the rule simple).

Idempotent: processed ndjson filenames live in logs/.tool-usage-state.json; a file is
processed once (the hook runs after the cycle closed its stream). Backfill is free —
any retained-but-unprocessed ndjson is picked up on the next run, so activating the
loop hook late loses nothing that retention hasn't already deleted. Exit 0 always.

  tool-usage-audit.py [--app /app] [--report]   # --report: print aggregate, no writes
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys

NDJSON_DIR = "logs/cycle-ndjson"
LEDGER = "logs/tool-usage-history.ndjson"
STATE = "logs/.tool-usage-state.json"

AIRTABLE_WRITE_HINTS = ("update", "create", "delete", "upload")


def calls_from_ndjson(path: str) -> list[tuple[str, str]]:
    """(tool_name, assembled_input_text) per call, in order."""
    calls, cur_name, cur_buf = [], None, []
    try:
        f = open(path, encoding="utf-8", errors="replace")
    except OSError:
        return []
    with f:
        for line in f:
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            t = ev.get("type")
            if t == "tool_start":
                if cur_name is not None:
                    calls.append((cur_name, "".join(cur_buf)))
                cur_name, cur_buf = ev.get("name", "?"), []
            elif t == "tool_input" and cur_name is not None:
                cur_buf.append(ev.get("delta", ""))
    if cur_name is not None:
        calls.append((cur_name, "".join(cur_buf)))
    return calls


def categorize(calls: list[tuple[str, str]]) -> dict:
    c = {"calls": len(calls), "ctx7": 0, "airtable_r": 0, "airtable_w": 0,
         "linear": 0, "browser": 0, "browser_mcp": 0, "graft": 0, "names": {}}
    for name, raw in calls:
        # Match on the TOOL NAME and, for bash, the COMMAND — never on arbitrary input
        # text: measured 2026-08-03, apply_patch/read calls EDITING browser-related code
        # matched a substring rule and inflated `browser` (and would inflate `linear`).
        cmd = ""
        if name == "bash":
            try:
                cmd = json.loads(raw).get("command", "") or ""
            except (json.JSONDecodeError, AttributeError):
                cmd = raw
        low = cmd.lower()
        lname = name.lower()
        if "ctx7" in low:
            c["ctx7"] += 1
        if "airtable-read.py" in low:
            c["airtable_r"] += 1
        elif "airtable-write.py" in low:
            c["airtable_w"] += 1
        elif name.startswith("mcp__airtable__"):
            key = "airtable_w" if any(h in name for h in AIRTABLE_WRITE_HINTS) else "airtable_r"
            c[key] += 1
        if "linear" in lname or "linear-track.py" in low or "api.linear.app" in low:
            c["linear"] += 1
        # TWO browser counters, because the harness A/B needs an honest denominator
        # (added 2026-08-04 with browse-extract.py): `browser` is ALL browser-touching
        # work — raw MCP steps, site-contact-evidence.py AND the harness — so moving work
        # into the harness cannot fake a drop by going uncounted. `browser_mcp` counts only
        # raw mcp__browseros__* micro-steps: that is the number the harness is supposed to
        # reduce, and the one the pre-registered metric names.
        if ("browseros" in lname or "browseros" in low
                or "site-contact-evidence" in low or "browse-extract" in low):
            c["browser"] += 1
        if lname.startswith("mcp__browseros__"):
            c["browser_mcp"] += 1
        # Graft kartı danışması (2026-08-24): kartlar dosya olarak okunur, bu yüzden
        # bash komutundaki YOL kalıplarıyla sayılır — çıplak "graft" kelimesi DEĞİL
        # ("grafting" gibi metinler yanlış-pozitif olurdu). Ölçüm amacı: kartlara
        # yatırım geri dönüyor mu (graft-kit README'nin kendi etiği: ölçmeden iddia etme).
        if ("graft/" in low or ".graft-kit" in low
                or "graft ask" in low or "graft callers" in low):
            c["graft"] += 1

        # Per-TOOL-NAME counts for MCP tools (2026-08-06). The category counters above
        # answer "how much Airtable", never "which Airtable tools" — so a proposal to trim
        # a server to "the ~4 tools actually used" had no way to name those four, and the
        # first such proposal (OPREQ-INFRA-MCP-DENYLIST-001) argued from a ledger that
        # began AFTER the tools in question were already denied. Names are recorded only
        # for mcp__ tools: bash/edit/read dominate the count and are not denylist material.
        if lname.startswith("mcp__"):
            c["names"][name] = c["names"].get(name, 0) + 1
    return c


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", default="/app")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--names", action="store_true",
                    help="per-MCP-tool-name totals (ledger + transcripts still on disk); "
                         "read-only, writes nothing")
    args = ap.parse_args()
    app = os.path.abspath(args.app)
    nd_dir = os.path.join(app, NDJSON_DIR)
    ledger = os.path.join(app, LEDGER)
    state_path = os.path.join(app, STATE)

    if args.report:
        try:
            for line in open(ledger, encoding="utf-8"):
                sys.stdout.write(line)
        except OSError:
            print("no ledger yet")
        return 0

    if args.names:
        # Two sources, kept apart on purpose. The LEDGER is durable and grows from here;
        # the TRANSCRIPTS on disk are a rotating window (~20 cycles) that happens to be
        # readable right now. Reporting them merged would hide that the ledger's own
        # coverage starts today, which is exactly the mistake being corrected here.
        led_names, led_rows, led_span = {}, 0, []
        try:
            for line in open(ledger, encoding="utf-8"):
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                led_rows += 1
                if row.get("ts"):
                    led_span.append(row["ts"])
                for k, v in (row.get("names") or {}).items():
                    led_names[k] = led_names.get(k, 0) + v
        except OSError:
            pass

        tr_names, tr_files = {}, 0
        try:
            for fn in sorted(os.listdir(nd_dir)):
                if not fn.endswith(".ndjson"):
                    continue
                tr_files += 1
                for k, v in categorize(calls_from_ndjson(
                        os.path.join(nd_dir, fn)))["names"].items():
                    tr_names[k] = tr_names.get(k, 0) + v
        except OSError:
            pass

        def dump(title, data, note):
            print(f"\n== {title} ==")
            print(f"   {note}")
            if not data:
                print("   (no MCP tool calls recorded)")
                return
            for name, n in sorted(data.items(), key=lambda kv: (-kv[1], kv[0])):
                print(f"   {n:6d}  {name}")
            servers = {}
            for name, n in data.items():
                servers[name.split("__")[1] if "__" in name else "?"] = (
                    servers.get(name.split("__")[1] if "__" in name else "?", 0) + n)
            print("   per server: " + ", ".join(
                f"{s}={n}" for s, n in sorted(servers.items(), key=lambda kv: -kv[1])))

        span = f"{min(led_span)} .. {max(led_span)}" if led_span else "empty"
        dump("LEDGER (durable)", led_names,
             f"{led_rows} rows, {span} — name data only exists for rows written after 2026-08-06")
        dump("TRANSCRIPTS ON DISK (rotating window)", tr_names,
             f"{tr_files} cycle transcripts currently present; older ones are already rotated away")
        print("\nA server absent from BOTH lists was not called in the window covered above.")
        print("That is not evidence it is unused: check whether its tools were denied")
        print("(JCODE_TOOLS_DENY in scripts/core/auto-loop.sh) before concluding anything.")
        return 0

    state = {}
    try:
        state = json.load(open(state_path, encoding="utf-8"))
    except (OSError, ValueError):
        pass
    processed = state.get("processed", {})

    try:
        files = sorted(os.listdir(nd_dir))
    except OSError:
        return 0
    new_lines = []
    for fn in files:
        if not fn.endswith(".ndjson"):
            continue
        path = os.path.join(nd_dir, fn)
        try:
            st = os.stat(path)
        except OSError:
            continue
        # Dedup on (name, size, mtime) — NOT on the name alone. The loop's cycle counter
        # restarts at 1 on every container restart, so cycle-0001.ndjson is REWRITTEN by a
        # brand-new cycle whose filename is already in `processed`. Measured 2026-08-04:
        # five post-restart cycles (including the first real use of the browse harness)
        # never reached the ledger, so the cockpit panel silently under-reported the day.
        # A file whose size or mtime moved carries different content and is audited again.
        prev = processed.get(fn)
        prev_size = prev if isinstance(prev, int) else (prev or {}).get("size")
        prev_mtime = None if isinstance(prev, int) else (prev or {}).get("mtime")
        if prev is not None and prev_size == st.st_size and (
                prev_mtime is None or prev_mtime == int(st.st_mtime)):
            continue
        row = categorize(calls_from_ndjson(path))
        row["file"] = fn
        row["ts"] = dt.datetime.fromtimestamp(st.st_mtime, tz=dt.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ")
        new_lines.append(json.dumps(row, separators=(",", ":")))
        processed[fn] = {"size": st.st_size, "mtime": int(st.st_mtime)}
    if not new_lines:
        return 0
    try:
        with open(ledger, "a", encoding="utf-8") as f:
            f.write("\n".join(new_lines) + "\n")
        tmp = state_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"processed": processed}, f)
        os.replace(tmp, state_path)
    except OSError as e:
        print(f"tool-usage-audit: write failed: {e}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
