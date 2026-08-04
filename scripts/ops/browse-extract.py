#!/usr/bin/env python3
"""One bash call = one complete browse-and-extract pass. Replaces MCP micro-step chains.

Measured 2026-08-03 (tool-usage ledger): 194 mcp__browseros__* calls in one day, ~173 of
them chat turns spent on navigate/tabs/read/grep/evaluate micro-steps — each turn re-bills
the whole context. The whole sequence is deterministic plumbing; nothing in the middle
needs a model decision. So this script runs the sequence server-side, exactly like
`ekap-run.py` does for the EKAP grid, and the model spends ONE bash turn instead of 5-9
MCP turns per page.

  browse-extract.py https://example.com --grep "iletisim|kvkk"
  browse-extract.py https://firma.com.tr https://firma.com.tr/kvkk --grep "@firma"
  browse-extract.py https://spa-site.com --wait-text "©" --read text
  browse-extract.py https://firma.com.tr --read links --max-bytes 2000

Contract:
  - Opens ONE background tab, walks every URL in order in that same tab, closes it at the
    end even on error (--keep-tab to hand the page id to a follow-up `act` flow).
  - Output is CAPPED (--max-bytes, default 4000 per URL) — a truncated excerpt with the
    true size named. Fetch-late/read-narrow rules apply to bash output too.
  - grep patterns run server-side over rendered page text (over=content), so an SPA that
    curl sees as an empty shell is still searched AFTER rendering. A wait that timed out
    is reported (`waited=timeout`) — treat "0 matches" then as INCONCLUSIVE, same rule as
    site-contact-evidence.py.
  - Interactive work (clicks, forms, refs) stays on the raw MCP tools; this harness is
    read-only by design and sends no input events.

Exit codes: 0 ok · 2 usage · 3 gateway unreachable/busy · 4 tool error mid-flow.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request

DEFAULT_MCP = os.environ.get("BROWSEROS_MCP_URL", "http://172.17.0.1:9245/mcp")
CTX = ssl.create_default_context()


class Gateway:
    def __init__(self, url: str, timeout: int):
        self.url = url
        self.timeout = timeout
        self.session = None

    def post(self, payload: dict) -> dict:
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json, text/event-stream"}
        if self.session:
            headers["mcp-session-id"] = self.session
        req = urllib.request.Request(self.url, data=json.dumps(payload).encode(),
                                     headers=headers)
        ctx = CTX if self.url.startswith("https") else None
        with urllib.request.urlopen(req, context=ctx, timeout=self.timeout) as resp:
            self.session = resp.headers.get("mcp-session-id", self.session)
            body = resp.read().decode()
        if body.lstrip().startswith("{"):
            return json.loads(body)
        for line in body.splitlines():          # SSE framing
            if line.startswith("data:"):
                return json.loads(line[5:].strip())
        return {}

    def call(self, name: str, args: dict) -> tuple[str, bool]:
        data = self.post({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                          "params": {"name": name, "arguments": args}})
        res = data.get("result", data.get("error", {}))
        texts = [c.get("text", "") for c in res.get("content", []) if c.get("type") == "text"]
        err = bool(res.get("isError")) or ("error" in data and "result" not in data)
        if err and not texts:
            texts = [json.dumps(data.get("error", res))[:300]]
        return "\n".join(texts), err

    def handshake(self):
        self.post({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2024-11-05", "capabilities": {},
            "clientInfo": {"name": "browse-extract", "version": "1.0"}}})
        self.post({"jsonrpc": "2.0", "method": "notifications/initialized"})


def clip(text: str, cap: int) -> tuple[str, bool]:
    raw = text or ""
    if len(raw.encode()) <= cap:
        return raw, False
    out = raw.encode()[:cap].decode(errors="ignore")
    return out, True


def extract(gw: Gateway, page: int, url: str, args) -> dict:
    r: dict = {"url": url, "grep": {}, "waited": "ok"}
    if args.wait_text:
        out, err = gw.call("wait", {"page": page, "for": "text", "value": args.wait_text,
                                    "timeout": args.wait_timeout})
        if err or "timed out" in out.lower() or "timeout" in out.lower():
            r["waited"] = "timeout"
    else:
        gw.call("wait", {"page": page, "for": "time", "value": args.wait_ms,
                         "timeout": args.wait_ms + 500})
    for pat in args.grep or []:
        out, err = gw.call("grep", {"page": page, "pattern": pat,
                                    "over": "content", "limit": args.grep_limit})
        if err:
            raise ToolError("grep %r on %s: %s" % (pat, url, out[:200]))
        lines = [ln for ln in out.splitlines() if ln.strip()]
        r["grep"][pat] = lines[:args.grep_limit]
    if args.read or not args.grep:
        fmt = args.read or "text"
        out, err = gw.call("read", {"page": page, "format": fmt})
        if err:
            raise ToolError("read on %s: %s" % (url, out[:200]))
        r["read_total_bytes"] = len(out.encode())
        r["read"], r["truncated"] = clip(out, args.max_bytes)
        r["read_format"] = fmt
    return r


class ToolError(Exception):
    pass


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("urls", nargs="+", help="visited in order, in one background tab")
    ap.add_argument("--grep", action="append", metavar="REGEX",
                    help="case-insensitive server-side pattern over rendered text; repeatable")
    ap.add_argument("--read", choices=["markdown", "text", "links"], default=None,
                    help="page excerpt format (default: text, only when no --grep given)")
    ap.add_argument("--max-bytes", type=int, default=4000,
                    help="excerpt cap PER URL (default 4000) — output is context, keep it small")
    ap.add_argument("--grep-limit", type=int, default=20)
    ap.add_argument("--wait-ms", type=int, default=8000,
                    help="fixed render wait per URL (default 8000; SPAs need it)")
    ap.add_argument("--wait-text", default=None,
                    help="wait for this substring instead of a fixed pause")
    ap.add_argument("--wait-timeout", type=int, default=15000)
    ap.add_argument("--keep-tab", action="store_true",
                    help="leave the tab open and print its page id for a follow-up act flow")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--mcp", default=DEFAULT_MCP)
    ap.add_argument("--timeout", type=int, default=180, help="per-request timeout, seconds")
    args = ap.parse_args()

    gw = Gateway(args.mcp, args.timeout)
    try:
        gw.handshake()
        out, err = gw.call("tabs", {"action": "new", "url": args.urls[0], "background": True})
        m = None if err else re.search(r"(\d+)", out)
        if err or not m:
            print("gateway refused tab open: %s" % out[:300], file=sys.stderr)
            return 3
        page = int(m.group(1))
    except (urllib.error.URLError, OSError, TimeoutError) as exc:
        print("gateway unreachable at %s: %s" % (args.mcp, exc), file=sys.stderr)
        return 3

    results, rc = [], 0
    try:
        for i, url in enumerate(args.urls):
            if i > 0:
                _, err = gw.call("navigate", {"page": page, "action": "url", "url": url})
                if err:
                    raise ToolError("navigate to %s failed" % url)
            results.append(extract(gw, page, url, args))
    except ToolError as exc:
        results.append({"url": "-", "error": str(exc)})
        rc = 4
    finally:
        if args.keep_tab and rc == 0:
            results.append({"kept_tab_page": page})
        else:
            try:
                gw.call("tabs", {"action": "close", "page": page})
            except Exception:  # noqa: BLE001 — closing is best-effort; report already built
                pass

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=1))
        return rc
    for r in results:
        if "error" in r:
            print("ERROR: %s" % r["error"])
            continue
        if "kept_tab_page" in r:
            print("KEPT TAB: page %d (close it when the act flow ends)" % r["kept_tab_page"])
            continue
        print("== %s (waited=%s)" % (r["url"], r["waited"]))
        for pat, lines in r["grep"].items():
            print("GREP %r: %d line(s)" % (pat, len(lines)))
            for ln in lines:
                print("  " + ln[:200])
        if "read" in r:
            print("READ %s: %dB of %dB%s" % (r["read_format"], len(r["read"].encode()),
                                             r["read_total_bytes"],
                                             " [truncated]" if r["truncated"] else ""))
            print(r["read"])
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
