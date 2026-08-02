#!/usr/bin/env python3
"""Did the cycle write code against an external library without consulting Context7?

CLAUDE.md has said "check Context7 before writing code against any external library" for
days. Measured 2026-08-02 over the last 12 cycles: 291 MCP calls, **zero** to Context7. The
tool is not the problem — the probe records `context7 reachable: true, tool_count: 2`, and it
is not in `JCODE_TOOLS_DENY`. The rule simply has no mechanical check, which is the same
shape as Guardrail 7, and Guardrail 7 measurably did not hold either.

So this is the check. It reads what the cycle actually did, from the same ndjson the turn
audit uses, and answers one question with evidence attached.

## What it will and will not fire on

The naive trigger — "a .py file was written and Context7 was not called" — would fire on our
own ops scripts, which import `urllib`, `json` and `subprocess` and need no documentation.
So the trigger is narrower: an import of a module that is **not** in the standard library and
**not** a relative/local path. That is the case the rule was written for.

It reports, it does not block, and it goes to the LOG, never to Telegram (alarm-design rule
4: escalate what you push, not what you log). A cycle that legitimately knew the API already
will occasionally be flagged; the line names the file and the module so that is a two-second
judgement rather than a mystery.

  context7-check.py --cycle /app/logs/cycle-ndjson/cycle-0033.ndjson   # one cycle, one line
  context7-check.py --report --last 12                                 # calibration/backfill
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

# Enough of the two standard libraries that our own tooling never trips the check. A module
# missing from here is only ever a FALSE POSITIVE (a flag to eyeball), never a missed one.
PY_STDLIB = {
    "abc", "argparse", "ast", "base64", "collections", "contextlib", "csv", "datetime",
    "decimal", "difflib", "email", "enum", "functools", "glob", "hashlib", "html", "http",
    "importlib", "inspect", "io", "itertools", "json", "logging", "math", "os", "pathlib",
    "platform", "random", "re", "shlex", "shutil", "signal", "smtplib", "socket", "sqlite3",
    "ssl", "statistics", "string", "subprocess", "sys", "tempfile", "textwrap", "threading",
    "time", "traceback", "types", "typing", "unicodedata", "unittest", "urllib", "uuid",
    "warnings", "xml", "zipfile", "zoneinfo", "__future__",
}
NODE_BUILTIN = {
    "assert", "buffer", "child_process", "crypto", "dns", "events", "fs", "http", "https",
    "net", "os", "path", "process", "querystring", "readline", "stream", "string_decoder",
    "timers", "tls", "url", "util", "zlib",
}
SRC_EXT = (".py", ".js", ".mjs", ".ts", ".tsx", ".jsx", ".go", ".rb", ".java", ".rs")

PY_IMPORT = re.compile(r"^\s*(?:import|from)\s+([A-Za-z_][\w.]*)", re.M)
JS_IMPORT = re.compile(r"""(?:require\(|from\s+)['"]([^'"]+)['"]""")


def externals(path: str, content: str) -> set[str]:
    """External modules this file imports. Relative and standard-library imports don't count."""
    found: set[str] = set()
    if path.endswith(".py"):
        for mod in PY_IMPORT.findall(content):
            top = mod.split(".")[0]
            if top and top not in PY_STDLIB:
                found.add(top)
    elif path.endswith((".js", ".mjs", ".ts", ".tsx", ".jsx")):
        for mod in JS_IMPORT.findall(content):
            if mod.startswith(".") or mod.startswith("/"):
                continue          # a local file, not a library
            top = mod[1:].split("/")[0] if mod.startswith("@") else mod.split("/")[0]
            if mod.startswith("node:") or top in NODE_BUILTIN:
                continue
            found.add(mod if mod.startswith("@") else top)
    return found


def scan(path: str) -> dict:
    """One cycle -> {context7_calls, mcp_calls, writes: {file: [modules]}}."""
    c7 = mcp = seen = 0
    writes: dict[str, set[str]] = {}
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if '"mcp__' in line:
                mcp += line.count('"mcp__')
                c7 += line.count('"mcp__context7__')
            # Whitespace-independent on purpose. An earlier version prefiltered on the exact
            # string '"name":"write"'; the harness's own logs happen to be written without a
            # space after the colon, so it worked in production and silently matched NOTHING
            # against a fixture built with json.dumps' default spacing. A prefilter is an
            # optimisation — it must never be the thing that decides correctness.
            if '"write"' not in line and '"edit"' not in line:
                continue
            # Parse rather than regex the content out: a code payload is full of quotes and
            # newlines, and a regex over it silently truncates at the first escaped one.
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            for call in walk_calls(rec):
                seen += 1
                args = call.get("input") or call.get("arguments") or {}
                f = args.get("file_path") or args.get("path") or ""
                if not f.endswith(SRC_EXT):
                    continue
                body = args.get("content") or args.get("new_string") or ""
                writes.setdefault(f, set()).update(externals(f, body))
    return {"context7_calls": c7, "mcp_calls": mcp, "writes": writes, "writes_seen": seen}


def walk_calls(node) -> list:
    """Tool-call objects, wherever the harness nested them in this record."""
    out = []
    if isinstance(node, dict):
        if node.get("name") in ("write", "edit"):
            out.append(node)
        for v in node.values():
            out += walk_calls(v)
    elif isinstance(node, list):
        for v in node:
            out += walk_calls(v)
    return out


def verdict(res: dict) -> tuple[str, str]:
    risky = {f: sorted(m) for f, m in res["writes"].items() if m}
    if not risky:
        # Say what was inspected, not just the conclusion. A bare "nothing found" is
        # indistinguishable from "the parser saw nothing", and this check has already had
        # exactly that bug once (the whitespace prefilter above).
        return "OK", "%d write/edit call(s) seen, %d to source files, none importing an external library" % (
            res["writes_seen"], len(res["writes"]))
    if res["context7_calls"]:
        return "OK", "%d Context7 call(s) alongside %d file(s)" % (
            res["context7_calls"], len(risky))
    detail = "; ".join("%s -> %s" % (os.path.basename(f), ",".join(m[:4]))
                       for f, m in sorted(risky.items())[:4])
    return "NO-CHECK", "wrote external-library code with 0 Context7 calls: " + detail


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--app", default=os.environ.get("APP_DIR", "/app"))
    ap.add_argument("--cycle", help="one cycle ndjson (default: the most recent)")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--last", type=int, default=12)
    args = ap.parse_args()

    pattern = os.path.join(args.app, "logs", "cycle-ndjson", "*.ndjson")
    files = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
    if args.cycle:
        files = [args.cycle]
    elif args.report:
        files = files[: args.last]
    else:
        files = files[:1]
    if not files:
        print("no cycle ndjson under %s" % pattern, file=sys.stderr)
        return 0            # nothing to say is not a failure

    flagged = 0
    for f in files:
        res = scan(f)
        v, why = verdict(res)
        flagged += v == "NO-CHECK"
        if args.report or v == "NO-CHECK":
            print("[CONTEXT7 %s] %s — %s" % (v, os.path.basename(f), why))
    if args.report:
        print("%d/%d cycle(s) flagged" % (flagged, len(files)))
    return 0                # a report, not a gate


if __name__ == "__main__":
    raise SystemExit(main())
