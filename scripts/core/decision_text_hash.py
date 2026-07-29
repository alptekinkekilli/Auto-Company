#!/usr/bin/env python3
"""Canonical content hash for a KİK decision page — the ONE implementation.

Why this exists as a script rather than a paragraph of instructions:

`KararGoster.aspx` is an ASP.NET page whose RAW bytes differ by client — a default
`curl` gets 329,600 bytes for 2025/UY.II-1098, a browser User-Agent gets 332,091 —
and `__VIEWSTATE` varies independently at constant length. So a raw-HTML hash makes
two honest actors disagree every time. Hashing the extracted TEXT fixes that: the
text is byte-identical across clients.

But "hash the extracted text" is still not a specification. Two reasonable
implementations disagree on whether entities are unescaped before or after tags are
dropped, whether NBSP counts as whitespace, whether a dropped tag leaves a space
behind. On 2026-07-29 that gap cost a real evidence row: the resolver published
`275765205d6d63f0` for 2026/UY.II-1318, the consumer computed something else, and —
correctly — quarantined the evidence rather than proceed on a mismatch it could not
explain. The consumer was right; the spec was underdetermined.

So: both ends call THIS file. A hash produced any other way is not comparable and
must not be written to the bridge.

The normalization, in order, each step load-bearing:
  1. decode UTF-8, replacing undecodable bytes (never raise on a stray byte)
  2. drop <script> and <style> ELEMENTS including their contents
  3. drop every remaining tag, replacing each with a single space — NOT with the
     empty string, or `a<br>b` becomes `ab` while a client that renders the break
     sees `a b`
  4. unescape HTML entities — AFTER tag removal, so a literal `&lt;div&gt;` in the
     decision text is never mistaken for markup
  5. map NBSP (U+00A0) to a plain space
  6. collapse every whitespace run to one space, then strip

Usage:
    decision_text_hash.py <url>              # fetch and hash
    decision_text_hash.py <path.html>        # hash a saved file
    decision_text_hash.py --text <path.txt>  # hash already-extracted text

Prints:  sha256:<first 16 hex>  chars=<n>
"""
from __future__ import annotations

import hashlib
import html
import re
import sys
import urllib.request

SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b[^>]*>.*?</\1\s*>", re.S | re.I)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def normalize(raw: bytes | str) -> str:
    text = raw.decode("utf-8", "replace") if isinstance(raw, bytes) else raw
    text = SCRIPT_STYLE_RE.sub(" ", text)
    text = TAG_RE.sub(" ", text)
    text = html.unescape(text)
    text = text.replace(" ", " ")
    return WS_RE.sub(" ", text).strip()


def digest(raw: bytes | str) -> tuple[str, int]:
    text = normalize(raw)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16], len(text)


def fetch(url: str) -> bytes:
    """Fetch the page, by whatever transport actually works here.

    A browser User-Agent is set, and that is safe precisely because of what this
    file guarantees: the raw bytes DO vary by User-Agent, the normalized text does
    not. Verified on 2025/UY.II-1098 — 329,600 vs 332,091 raw bytes, identical
    83,416-char text, identical hash.

    urllib is tried first and curl is the fallback: ekap.kik.gov.tr rejects the TLS
    handshake from some Python builds (observed on macOS/py3.14) while accepting
    curl from the same host. A hash tool that only runs in one of the two places
    the bridge spans would be useless for the thing it exists to settle.
    """
    ua = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
          "(KHTML, like Gecko) Chrome/131.0 Safari/537.36")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": ua})
        with urllib.request.urlopen(req, timeout=60) as resp:  # noqa: S310
            return resp.read()
    except Exception as exc:  # noqa: BLE001
        import shutil
        import subprocess
        if not shutil.which("curl"):
            raise
        print(f"[note] urllib failed ({type(exc).__name__}), falling back to curl",
              file=sys.stderr)
        out = subprocess.run(["curl", "-sS", "--max-time", "60", "-A", ua, url],
                             capture_output=True, check=True)
        return out.stdout


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__.strip().splitlines()[0], file=sys.stderr)
        return 2
    if argv[0] == "--text":
        raw = open(argv[1], encoding="utf-8", errors="replace").read()
        text = WS_RE.sub(" ", raw).strip()
        h, n = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16], len(text)
    else:
        target = argv[0]
        raw = fetch(target) if target.startswith(("http://", "https://")) else open(target, "rb").read()
        h, n = digest(raw)
    print(f"sha256:{h}  chars={n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
