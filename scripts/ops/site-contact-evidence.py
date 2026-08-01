#!/usr/bin/env python3
"""Find a firm's published contact e-mail — without mistaking an unrendered page for an empty one.

The failure this exists to prevent, measured 2026-08-01 on a real prospect: a G4 attribution
check fetched `arkenom.com.tr` with a session-free curl, got **652 bytes** — a React shell
whose entire body is `<div id="root"></div>` plus "You need to enable JavaScript to run this
app" — and concluded "the site publishes NO email anywhere". The firm was moved to HELD on
that basis. The email was there the whole time: `info@arkenom.com.tr`, served from the site's
own JS bundle and rendered in the footer and the KVKK / Aydınlatma / İmha / Bilgi Güvenliği
policy pages that every Turkish corporate site is expected to publish.

So the rule this encodes: **a fetch that returned no rendered content is INCONCLUSIVE, never
negative.** Three escalating sources, cheapest first, and the report always says WHICH one the
evidence came from, because provenance is the whole point of a G4 check:

  1. **the browser-rendered DOM via BrowserOS — the default, and the one that decides.**
     Operator standing instruction 2026-08-01: *"ben browser os boşuna mı kurdum, oradan
     bakacaksınız — hem şirket hem sen."* A rendered read found the address immediately, in
     the footer and in the sentence "you may contact us at info@arkenom.com.tr";
  2. the served HTML (enough for classic server-rendered sites);
  3. the JavaScript bundles it references — one extra request each, where an SPA keeps its
     footer text, useful as corroboration and when no browser is reachable.

Also checks the policy pages by name: `kvkk`, `aydinlatma`, `gizlilik`, `iletisim`, `cerez`,
`politika` and their English equivalents. Those pages exist for legal reasons and carry a
contact address far more reliably than a home page does.

Usage:
  site-contact-evidence.py arkenom.com.tr
  site-contact-evidence.py --json firma1.com firma2.com.tr
  site-contact-evidence.py --no-render arkenom.com.tr     # curl only; can never prove absence
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.parse

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
SCRIPT_RE = re.compile(r'<script[^>]+src=["\']([^"\']+)', re.I)
HREF_RE = re.compile(r'href=["\']([^"\']+)', re.I)
POLICY_RE = re.compile(
    r"kvkk|aydinlat|aydınlat|gizlilik|politika|policy|privacy|iletisim|iletişim|contact|"
    r"cerez|çerez|imha|destruction|illumination|guvenlik|güvenlik|security", re.I)
# Addresses that are never the firm's own contact point.
NOISE_RE = re.compile(r"@(sentry|example|domain|email|yourdomain|godaddy|wixpress|"
                      r"sentry\.io|w3\.org)|\.(png|jpg|svg|css|js)$", re.I)
SHELL_MARKERS = ("enable JavaScript", 'id="root"', "id='root'", 'id="app"', "__NEXT_DATA__")


def fetch(url: str, timeout: int = 30) -> tuple[str, str]:
    try:
        r = subprocess.run(["curl", "-sSL", "-A", UA, "--max-time", str(timeout),
                            "-w", "\n%{http_code}", url],
                           capture_output=True, text=True, timeout=timeout + 15)
    except subprocess.TimeoutExpired:
        return "TIMEOUT", ""
    body, _, code = r.stdout.rpartition("\n")
    return code.strip() or "ERR", body


def emails(text: str) -> set[str]:
    return {e for e in EMAIL_RE.findall(text or "") if not NOISE_RE.search(e)}


def looks_unrendered(html: str) -> bool:
    """True when the response carries no content a reader would see.

    Size alone is not the test — a small page can still be a real page. What makes it a shell
    is an empty mount point or an explicit "enable JavaScript" notice with almost no text.
    """
    if not html:
        return True
    visible = re.sub(r"<[^>]+>", " ", re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", html))
    visible = re.sub(r"\s+", " ", visible).strip()
    return len(visible) < 200 and any(mark in html for mark in SHELL_MARKERS)


def render_dom(url: str, mcp: str) -> str:
    """Optional third source: the DOM as a browser builds it."""
    sys.path.insert(0, str(__import__("pathlib").Path.home() / "projects/autocompany-deploy/scripts"))
    try:
        import importlib.util
        import pathlib
        import time
        src = pathlib.Path.home() / "projects/autocompany-deploy/scripts/ekap-run.py"
        spec = importlib.util.spec_from_file_location("ekap_run", src)
        mod = importlib.util.module_from_spec(spec)
        sys.modules["ekap_run"] = mod
        spec.loader.exec_module(mod)
        if mcp:
            mod.MCP = mcp
        _, sid = mod.post({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2024-11-05", "capabilities": {},
            "clientInfo": {"name": "site-contact-evidence", "version": "1.0"}}})
        mod.post({"jsonrpc": "2.0", "method": "notifications/initialized"}, sid)
        out, _ = mod.call(sid, "tabs", {"action": "new", "url": url, "background": True})
        page = int(re.search(r"(\d+)", out).group(1))
        time.sleep(10)
        dom, _ = mod.call(sid, "evaluate", {"page": page,
                                            "code": "return document.documentElement.outerHTML;"})
        mod.call(sid, "tabs", {"action": "close", "page": page})
        return dom
    except Exception as exc:  # noqa: BLE001 — rendering is a bonus source, never a hard failure
        return "render failed: %s" % exc


def examine(domain: str, render: bool, mcp: str) -> dict:
    base = domain if domain.startswith("http") else "https://" + domain
    result = {"domain": domain, "sources": {}, "emails": {}, "verdict": None}

    code, html = fetch(base)
    result["sources"]["html"] = {"http": code, "bytes": len(html),
                                 "unrendered": looks_unrendered(html)}
    for e in emails(html):
        result["emails"].setdefault(e, []).append("html:" + base)

    if code == "200":
        # 2. the bundles — where an SPA actually keeps its footer and policy text.
        for src in SCRIPT_RE.findall(html)[:6]:
            u = urllib.parse.urljoin(base, src)
            if urllib.parse.urlparse(u).netloc != urllib.parse.urlparse(base).netloc:
                continue  # third-party analytics: not first-party publication
            c2, js = fetch(u, 40)
            result["sources"].setdefault("bundles", []).append(
                {"url": u, "http": c2, "bytes": len(js)})
            for e in emails(js):
                result["emails"].setdefault(e, []).append("bundle:" + u)

        # 3. the pages that exist for legal reasons and therefore carry a contact address.
        seen = set()
        for href in HREF_RE.findall(html):
            u = urllib.parse.urljoin(base, href)
            if urllib.parse.urlparse(u).netloc != urllib.parse.urlparse(base).netloc:
                continue
            if POLICY_RE.search(u) and u not in seen:
                seen.add(u)
                c3, page = fetch(u)
                for e in emails(page):
                    result["emails"].setdefault(e, []).append("policy:" + u)
        result["sources"]["policy_pages"] = len(seen)

    rendered_ok = False
    if render:
        dom = render_dom(base, mcp)
        rendered_ok = not dom.startswith("render failed") and len(dom) > 500
        result["sources"]["rendered"] = {"bytes": len(dom), "ok": rendered_ok}
        for e in emails(dom):
            result["emails"].setdefault(e, []).append("rendered:" + base)
    result["rendered_ok"] = rendered_ok

    host = urllib.parse.urlparse(base).netloc.replace("www.", "")
    own = [e for e in result["emails"] if e.lower().endswith("@" + host.lower())]
    if own:
        result["verdict"] = "FOUND_FIRST_PARTY"
    elif result["emails"]:
        result["verdict"] = "FOUND_OFF_DOMAIN"   # needs a common-control argument, see Rule 9
    elif code != "200":
        result["verdict"] = "INCONCLUSIVE_UNREACHABLE"
    elif not rendered_ok:
        # The distinction the whole script exists for: only a RENDERED look may return a
        # negative. Without one, "nothing found" describes the instrument, not the site.
        result["verdict"] = "INCONCLUSIVE_NOT_RENDERED"
    else:
        result["verdict"] = "NONE_PUBLISHED"
    result["first_party"] = own
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("domains", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-render", dest="render", action="store_false",
                    help="skip BrowserOS; the result can then never be a NEGATIVE finding")
    ap.set_defaults(render=True)
    ap.add_argument("--mcp", default="", help="BrowserOS MCP endpoint override")
    args = ap.parse_args()

    out = [examine(d, args.render, args.mcp) for d in args.domains]
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 0
    for r in out:
        h = r["sources"]["html"]
        print("%-28s %-26s html=%s/%dB%s" % (
            r["domain"], r["verdict"], h["http"], h["bytes"],
            " [SHELL — not evidence of absence]" if h["unrendered"] else ""))
        for e, where in sorted(r["emails"].items()):
            print("    %-34s %s" % (e, where[0][:70]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
