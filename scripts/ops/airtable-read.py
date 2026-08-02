#!/usr/bin/env python3
"""Scoped Airtable reads — the only sanctioned way for a cycle to read a table.

Why this exists (measured, not assumed): `mcp__airtable__list_records_for_table` returns
the WHOLE table. Over seven cycles it averaged 28,717 bytes per call and its context
re-reads cost $2.41 — more than every external web fetch and search in the same window
combined ($0.13 / 47 calls). Nothing about the company's work needed a whole table; it
needed five rows and four columns.

A tool result is not paid once. It sits in the context and is re-read on every later turn
of the cycle, so the price of a call is (output size x turns REMAINING after it). That is
why this wrapper is strict about two different things:

  * SIZE — scope the query (`filterByFormula` / `view` / explicit record ids), name the
    columns you need (`--fields`), and cap the rows (`--max-records`). Long cell values are
    truncated to `--cell-chars`, because a 4 KB notes field re-read 40 times costs more than
    the decision it informs.
  * SHAPE — output is one compact line per record, not pretty-printed JSON. Indentation is
    tokens too.

It refuses rather than guesses. Every refusal names the flag that fixes it, because a
wrapper that fails without a remedy just gets worked around.

Airtable specifics encoded here (source: airtable.com/developers/web/api/list-records,
retrieved via Context7 2026-08-01):
  * `pageSize` <= 100; `maxRecords` larger than a page requires following `offset`.
  * Requests are capped at a 16,000-character URL. An encoded formula or a long `fields`
    list can exceed it — the documented fix is POST /listRecords with the parameters in the
    body, which this script switches to automatically at 15,000.
  * Fields whose value is empty ("", [], false) are omitted from the response entirely, so
    a missing key means empty, NOT "column does not exist".
  * `filterByFormula` accepts field IDs as well as names (2023-04-05 changelog); prefer IDs
    when a rename would otherwise silently return zero rows.

Usage:
  airtable-read.py --table tblXXXX --fields Name --fields Status --formula "{Status}='Qualified'"
  airtable-read.py --table tblXXXX --fields Name --record recAAA --record recBBB
  airtable-read.py --table tblXXXX --view "Ready to send" --fields Name --max-records 10
  airtable-read.py --table tblXXXX --formula "{Status}='PENDING'" --count-only

Auth: AIRTABLE_API_KEY (and AIRTABLE_BASE_ID unless --base is given), read from the
environment or from logs/runtime.env. The key is never printed, not even on error.
"""
from __future__ import annotations

import argparse
import json
import os
import ssl
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

API_ROOT = "https://api.airtable.com/v0"
URL_LIMIT = 16000          # Airtable's documented hard cap
URL_SWITCH = 15000         # our own switch-to-POST threshold, below the cap
PAGE_MAX = 100             # Airtable's documented pageSize ceiling
DEFAULT_MAX_RECORDS = 20
HARD_MAX_RECORDS = 200     # --force lifts this
ALL_FIELDS_MAX_RECORDS = 5  # reading every column is only ever OK for a handful of rows
COUNT_CEILING = 1000        # --count-only transfers rows but prints only the number
DEFAULT_CELL_CHARS = 200
CTX = ssl.create_default_context()


class Refusal(Exception):
    """A scoping mistake we can name precisely, with the flag that fixes it."""


def load_env(app_dir: str) -> None:
    """Fill missing AIRTABLE_* from logs/runtime.env (the loop's own secret file).

    Values are put in this process's env only — never echoed, never passed as argv.
    """
    if os.environ.get("AIRTABLE_API_KEY") and os.environ.get("AIRTABLE_BASE_ID"):
        return
    path = os.path.join(app_dir, "logs", "runtime.env")
    try:
        fh = open(path, encoding="utf-8", errors="replace")
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


def load_keychain() -> None:
    """Last resort on the operator's Mac, where there is no logs/runtime.env at all.

    Without this, every read from outside the container needed an ssh + docker exec round
    trip. The value goes into this process's env only — the subprocess call carries the
    SERVICE NAME in argv, never the secret.
    """
    if os.environ.get("AIRTABLE_API_KEY") or sys.platform != "darwin":
        return
    try:
        out = subprocess.run(["security", "find-generic-password", "-w",
                              "-s", "autocompany-airtable-pat"],
                             capture_output=True, text=True, timeout=10).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return
    if out:
        os.environ["AIRTABLE_API_KEY"] = out


def build_params(args) -> dict:
    """Turn the flags into Airtable query parameters, refusing anything unscoped."""
    scopes = [bool(args.formula), bool(args.view), bool(args.record)]
    if not any(scopes):
        raise Refusal(
            "unscoped read refused — a whole-table pull is the single most expensive thing "
            "a cycle does.\n"
            "  Give it a scope: --formula \"{Status}='Qualified'\", or --view \"<view name>\", "
            "or --record recXXXX (repeatable).\n"
            "  To count rows without pulling them, add --count-only to any scoped query."
        )
    if not args.fields and not args.all_fields:
        raise Refusal(
            "no columns named — refusing to return every field.\n"
            "  Name what you need: --fields Name --fields Status (repeatable).\n"
            "  If you genuinely need the full row shape, --all-fields is allowed for at most "
            f"{ALL_FIELDS_MAX_RECORDS} records; use --describe once instead if you only want "
            "to learn the column names."
        )

    max_records = args.max_records
    if args.all_fields and max_records > ALL_FIELDS_MAX_RECORDS and not args.force:
        raise Refusal(
            f"--all-fields with --max-records {max_records} refused (ceiling "
            f"{ALL_FIELDS_MAX_RECORDS}).\n"
            "  Either name the columns with --fields, or lower --max-records. --force overrides, "
            "and the footer will report what it cost."
        )
    if max_records > HARD_MAX_RECORDS and not args.force:
        raise Refusal(
            f"--max-records {max_records} exceeds the {HARD_MAX_RECORDS}-row ceiling.\n"
            "  Narrow the formula, or pass --force if you have actually decided the whole set "
            "belongs in this context."
        )

    params: dict = {"maxRecords": max_records, "pageSize": min(PAGE_MAX, max_records)}
    if args.fields:
        # Accept BOTH forms. The flag is repeatable, but a comma-separated list is the obvious
        # guess and the company spent a turn rediscovering that twice in two cycles
        # (2026-08-02 cycle summaries: "--fields needs to be repeated, not comma-joined").
        # Refusing a reasonable guess to defend a convention costs more than supporting it.
        expanded: list[str] = []
        for f in args.fields:
            expanded.extend(x.strip() for x in f.split(",") if x.strip())
        params["fields[]"] = expanded
    if args.view:
        params["view"] = args.view
    if args.record:
        # RECORD_ID() over a literal OR() is the cheapest exact-row fetch that still costs
        # one response instead of one request per id.
        rec_formula = "OR(%s)" % ",".join("RECORD_ID()='%s'" % r for r in args.record)
        params["filterByFormula"] = (
            "AND(%s,%s)" % (rec_formula, args.formula) if args.formula else rec_formula
        )
    elif args.formula:
        params["filterByFormula"] = args.formula
    if args.sort_field:
        params["sort[0][field]"] = args.sort_field
        params["sort[0][direction]"] = args.sort_direction
    return params


def encode(params: dict) -> str:
    flat: list[tuple[str, str]] = []
    for key, value in params.items():
        if isinstance(value, list):
            flat.extend((key, str(v)) for v in value)
        else:
            flat.append((key, str(value)))
    return urllib.parse.urlencode(flat)


def to_body(params: dict) -> dict:
    """The POST /listRecords body form of the same query (used past URL_SWITCH)."""
    body: dict = {}
    for key, value in params.items():
        if key == "fields[]":
            body["fields"] = value
        elif key == "sort[0][field]":
            body.setdefault("sort", [{}])[0]["field"] = value
        elif key == "sort[0][direction]":
            body.setdefault("sort", [{}])[0]["direction"] = value
        else:
            body[key] = value
    return body


def request(url: str, token: str, body: dict | None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Authorization": "Bearer %s" % token}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers,
                                 method="POST" if data is not None else "GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:400]
        # Never let the token reach stdout/stderr, whatever the API echoed back.
        detail = detail.replace(token, "<redacted>")
        raise SystemExit("airtable HTTP %s: %s" % (exc.code, detail))
    except urllib.error.URLError as exc:
        raise SystemExit("airtable unreachable: %s" % exc.reason)


def fetch(base: str, table: str, params: dict, token: str) -> list[dict]:
    records: list[dict] = []
    offset = None
    wanted = int(params.get("maxRecords", DEFAULT_MAX_RECORDS))
    endpoint = "%s/%s/%s" % (API_ROOT, base, urllib.parse.quote(table, safe=""))
    while True:
        page = dict(params)
        if offset:
            page["offset"] = offset
        query = encode(page)
        if len(endpoint) + 1 + len(query) >= URL_SWITCH:
            # Documented remedy for the 16,000-character URL cap.
            data = request(endpoint + "/listRecords", token, to_body(page))
        else:
            data = request(endpoint + "?" + query, token, None)
        records.extend(data.get("records", []))
        offset = data.get("offset")
        if not offset or len(records) >= wanted:
            break
    return records[:wanted]


def clip(value, limit: int):
    """Truncate long cell values, marking the cut so nobody mistakes it for the whole value."""
    if isinstance(value, str) and len(value) > limit:
        return value[:limit] + "…[+%d chars, re-read with --cell-chars]" % (len(value) - limit)
    if isinstance(value, list):
        return [clip(v, limit) for v in value]
    return value


def main() -> int:
    ap = argparse.ArgumentParser(description="Scoped Airtable read (see module docstring).")
    ap.add_argument("--app", default=os.environ.get("AC_APP_DIR", "/app"))
    ap.add_argument("--base", default=None, help="appXXXX (default: AIRTABLE_BASE_ID)")
    ap.add_argument("--table", required=True, help="tblXXXX or table name")
    ap.add_argument("--fields", action="append", default=[], help="column to return (repeatable)")
    ap.add_argument("--all-fields", action="store_true",
                    help="return every column — capped at %d records" % ALL_FIELDS_MAX_RECORDS)
    ap.add_argument("--formula", default=None, help="filterByFormula, e.g. \"{Status}='PENDING'\"")
    ap.add_argument("--view", default=None, help="restrict to a view")
    ap.add_argument("--record", action="append", default=[], help="recXXXX (repeatable)")
    ap.add_argument("--sort-field", default=None)
    ap.add_argument("--sort-direction", default="asc", choices=("asc", "desc"))
    ap.add_argument("--max-records", type=int, default=DEFAULT_MAX_RECORDS)
    ap.add_argument("--cell-chars", type=int, default=DEFAULT_CELL_CHARS)
    ap.add_argument("--count-only", action="store_true", help="print the row count, no rows")
    ap.add_argument("--describe", action="store_true",
                    help="print the column names from one sample row and exit")
    ap.add_argument("--format", default="compact", choices=("compact", "json", "tsv"))
    ap.add_argument("--force", action="store_true", help="lift the row ceilings deliberately")
    ap.add_argument("--print-query", action="store_true",
                    help="show the query that would be sent and exit (no network, no auth)")
    args = ap.parse_args()

    # --describe is exempt from scoping: it reads exactly one row on purpose, and the point
    # is to make "what are this table's columns?" cheap enough that nobody dumps the table
    # to find out.
    params: dict = {}
    if not args.describe:
        try:
            params = build_params(args)
        except Refusal as exc:
            print("REFUSED: %s" % exc, file=sys.stderr)
            return 2

    if args.print_query:
        print(json.dumps({"table": args.table, "params": to_body(params)},
                         ensure_ascii=False, sort_keys=True))
        return 0

    load_env(args.app)
    load_keychain()
    token = os.environ.get("AIRTABLE_API_KEY", "")
    base = args.base or os.environ.get("AIRTABLE_BASE_ID", "")
    if not token:
        print("AIRTABLE_API_KEY not set and not found in %s/logs/runtime.env" % args.app,
              file=sys.stderr)
        return 3
    if not base:
        print("no base id — pass --base appXXXX or set AIRTABLE_BASE_ID", file=sys.stderr)
        return 3

    if args.describe:
        # Learning a table's shape should cost one row, once — not a table dump per cycle.
        records = fetch(base, args.table, {"maxRecords": 1, "pageSize": 1}, token)
        if not records:
            print("table is empty — no column names to report")
            return 0
        print("\n".join(sorted((records[0].get("fields") or {}).keys())))
        print("-- columns present on one sample row; empty-valued fields are omitted by the "
              "API, so this is a lower bound", file=sys.stderr)
        return 0

    if args.count_only:
        # Counting is not a context cost: the rows are transferred and discarded, only the
        # number is printed. So the row ceiling does not apply here.
        params = dict(params, maxRecords=COUNT_CEILING, pageSize=PAGE_MAX)
        records = fetch(base, args.table, params, token)
        suffix = "+ (ceiling reached)" if len(records) >= COUNT_CEILING else ""
        print("%d%s record(s) match" % (len(records), suffix))
        return 0

    records = fetch(base, args.table, params, token)

    rows = [{"id": r.get("id"), **{k: clip(v, args.cell_chars)
                                   for k, v in (r.get("fields") or {}).items()}}
            for r in records]
    if args.format == "json":
        out = json.dumps(rows, ensure_ascii=False)
    elif args.format == "tsv":
        cols = args.fields or sorted({k for row in rows for k in row if k != "id"})
        lines = ["\t".join(["id"] + list(cols))]
        lines += ["\t".join([row.get("id", "")] +
                            [str(row.get(c, "")).replace("\t", " ").replace("\n", " ")
                             for c in cols]) for row in rows]
        out = "\n".join(lines)
    else:
        out = "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows)
    print(out)
    # The footer is the point: every scoped read tells you what it just put in the context.
    print("-- %d record(s), %d bytes into context (measured whole-table pulls averaged 28,717 "
          "bytes per call)" % (len(rows), len(out.encode())), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
