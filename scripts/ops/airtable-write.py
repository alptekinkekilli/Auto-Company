#!/usr/bin/env python3
"""Single-record Airtable writes, with the before/after read-back done for you.

Why this exists. The company writes to Airtable through its MCP, but every write from
OUTSIDE a cycle — an operator-side correction, an evidence fix found during a sweep — had
no sanctioned path. What happened instead was a hand-rolled curl with the payload in argv,
which is exactly how three API keys ended up in `ps` output on 2026-08-01, and which prints
no before/after, so a bad write is invisible until someone re-reads the row by chance.

This tool encodes the rules that the standing EXTERNAL-SYSTEM WRITE AUTHORITY rule states
in prose: read the exact target first, write only the fields you named, read the result
back, and show what changed. The key comes from logs/runtime.env into this process's env
only — never argv, never printed, not even on error (same loader as airtable-read.py).

  airtable-write.py --table tblXXXX --record recAAA --set-file fix.json          # dry run
  airtable-write.py --table tblXXXX --record recAAA --set-file fix.json --apply

`fix.json` is a flat {"Field name": value} object. One record per invocation, deliberately:
a write you cannot describe in one line is a write nobody will audit.

Guards, each of which has a real failure behind it:
  * dry run is the DEFAULT; --apply is the only way to change anything.
  * clearing a field that currently has a value needs --allow-clear. Silent data loss in a
    "fix" is the bug class that got through review once already (analyst pass-2, 2026-07-31).
  * writing a field name that does not exist on the record is reported, not silently
    created — Airtable would happily accept a typo'd column and strand the value. Empty
    fields are omitted from reads, so "absent" is a warning, not a refusal (--force).
  * the read-back must equal what was sent, or the exit code is non-zero. An HTTP 200 is
    not evidence the value landed.
"""
from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.request

API_ROOT = "https://api.airtable.com/v0"
CTX = ssl.create_default_context()


def load_env(app_dir: str) -> None:
    """Fill missing AIRTABLE_* from logs/runtime.env. Never echoed, never passed as argv."""
    if os.environ.get("AIRTABLE_API_KEY") and os.environ.get("AIRTABLE_BASE_ID"):
        return
    try:
        fh = open(os.path.join(app_dir, "logs", "runtime.env"), encoding="utf-8", errors="replace")
    except OSError:
        return
    with fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            k = k.strip()
            if k in ("AIRTABLE_API_KEY", "AIRTABLE_BASE_ID") and not os.environ.get(k):
                os.environ[k] = v.strip().strip('"').strip("'")


def call(method: str, url: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": "Bearer " + os.environ["AIRTABLE_API_KEY"],
        "Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=45, context=CTX))
    except urllib.error.HTTPError as e:
        # The body can echo the request; the key is only ever in the header, so this is safe.
        raise SystemExit("Airtable %s %s: %s" % (method, e.code, e.read().decode()[:400]))


def guard(before: dict, new: dict, allow_clear: bool, force: bool) -> list[str]:
    """Everything that can refuse a write, decided from data alone so it can be tested.

    Kept out of main() on purpose: the rest of this script cannot run without a live API
    call, and a guard nobody can exercise offline is a guard nobody exercises.
    """
    problems: list[str] = []
    missing = [n for n in new if n not in before]
    if missing and not force:
        problems.append("not present on this row: %s\n"
                        "  Airtable omits empty fields from reads, so this may just be an empty"
                        " column —\n  check the spelling against --describe, then re-run with"
                        " --force." % ", ".join(missing))
    cleared = [n for n in new
               if new[n] in (None, "", []) and before.get(n) not in (None, "", [])]
    if cleared and not allow_clear:
        problems.append("would clear non-empty field(s): %s\n"
                        "  pass --allow-clear if erasing them is the intent." % ", ".join(cleared))
    return problems


def show(label: str, fields: dict, names: list[str], width: int) -> None:
    for n in names:
        v = fields.get(n)
        s = "<empty>" if v in (None, "", [], False) else str(v)
        if len(s) > width:
            s = s[:width] + "…[+%d]" % (len(s) - width)
        print("  %-6s %s = %s" % (label, n, s))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--app", default=os.environ.get("APP_DIR", "/app"))
    ap.add_argument("--base", default="")
    ap.add_argument("--table", required=True)
    ap.add_argument("--record", required=True)
    ap.add_argument("--set-file", required=True, help="flat JSON object of field -> new value")
    ap.add_argument("--apply", action="store_true", help="without this it is a dry run")
    ap.add_argument("--allow-clear", action="store_true")
    ap.add_argument("--force", action="store_true", help="write field names absent from the row")
    ap.add_argument("--cell-chars", type=int, default=220)
    args = ap.parse_args()

    load_env(args.app)
    if not os.environ.get("AIRTABLE_API_KEY"):
        print("AIRTABLE_API_KEY not set and not found in %s/logs/runtime.env" % args.app,
              file=sys.stderr)
        return 2
    base = args.base or os.environ.get("AIRTABLE_BASE_ID", "")
    if not base:
        print("no base: pass --base or set AIRTABLE_BASE_ID", file=sys.stderr)
        return 2

    with open(args.set_file, encoding="utf-8") as fh:
        new = json.load(fh)
    if not isinstance(new, dict) or not new:
        print("--set-file must be a non-empty JSON object of field -> value", file=sys.stderr)
        return 2

    url = "%s/%s/%s/%s" % (API_ROOT, base, args.table, args.record)
    before = call("GET", url).get("fields", {})
    names = list(new)

    problems = guard(before, new, args.allow_clear, args.force)
    if problems:
        for p in problems:
            print("refused: " + p, file=sys.stderr)
        return 2

    print("%s / %s / %s" % (base, args.table, args.record))
    show("BEFORE", before, names, args.cell_chars)
    show("AFTER*", new, names, args.cell_chars)
    if not args.apply:
        print("dry run — nothing written. Re-run with --apply.")
        return 0

    call("PATCH", url, {"fields": new})
    back = call("GET", url).get("fields", {})
    bad = [n for n in names if back.get(n) != new[n]]
    show("READ", back, names, args.cell_chars)
    if bad:
        print("FAILED read-back on: %s" % ", ".join(bad), file=sys.stderr)
        return 1
    print("written and verified: %s" % ", ".join(names))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
