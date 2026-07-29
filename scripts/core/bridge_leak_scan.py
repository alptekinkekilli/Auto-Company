#!/usr/bin/env python3
"""Value-sensitive session-leak scanner for EKAP Bridge records — the ONE implementation.

Why value-sensitive: the first scanner blocked on word PRESENCE, so the record's
own assurance sentence — "No cookie/token/header/localStorage/session material
crossed the bridge" — flagged itself as a leak (observed 2026-07-29 on the 1280
readback, a false positive per the operator's review). Words about secrets are
not secrets. What must never appear is a KEY TOGETHER WITH A REAL VALUE.

FAIL (key + non-empty value adjacency):
  - `Cookie:` / `Set-Cookie:` header carrying `name=value`
  - `Authorization: Bearer <token>`
  - a named credential/session key (`access_token`, `refresh_token`, `id_token`,
    `apiSecretKey`, `ASP.NET_SessionId`, `JSESSIONID`, `PHPSESSID`, `sessionid`)
    assigned a value of credential-like length
  - a localStorage/sessionStorage DUMP (the word followed by a populated object)

PASS (explicitly allowed, never flag):
  - assurance sentences naming the words without values
  - `KararId=<hex>` — an opaque PUBLIC identifier, part of the public_url evidence
  - `content_hash` / source-page hashes — public-evidence fields by design

The false-positive fix must never loosen the gate: run --selftest (one negative
fixture that must PASS, four positive fixtures that must FAIL) — it is wired to
refuse the scanner itself if any fixture misbehaves, the same canary idea as
directive-rule-sweep.

Usage:
    bridge_leak_scan.py <file>      # scan a file (use - for stdin)
    bridge_leak_scan.py --selftest  # regression fixtures; rc 0 only if all behave
Exit codes: 0 = CLEAN, 1 = LEAK FOUND, 3 = selftest failure (scanner untrustworthy).
"""
from __future__ import annotations

import re
import sys

RULES: list[tuple[str, re.Pattern]] = [
    ("cookie-header-with-value",
     re.compile(r"\b(set-cookie|cookie)\s*:\s*[^\s;=,\"']+=[^\s;,\"']+", re.I)),
    # Any Authorization/Proxy-Authorization header WITH a credential — not just
    # Bearer (operator hardening, 2026-07-29). Two shapes: a known scheme
    # followed by its credential, or a bare opaque token of credential length.
    # Deliberately NOT "any text after the colon": bridge/OPREQ prose contains
    # phrases like "authorization: granted" — short plain words are not
    # credentials, and flagging them would recreate the word-presence bug.
    ("authorization-header-with-credential",
     re.compile(r"\b(proxy-)?authorization\s*:\s*"
                r"(basic|bearer|digest|negotiate|ntlm|hoba|mutual|oauth|token|aws4-hmac-sha256)"
                r"\s+\S+", re.I)),
    ("authorization-header-opaque-token",
     re.compile(r"\b(proxy-)?authorization\s*:\s*[A-Za-z0-9\-._~+/=]{16,}(?=[\s,\"']|$)", re.I)),
    ("named-credential-key-with-value",
     re.compile(r"\b(access_token|refresh_token|id_token|apisecretkey|"
                r"asp\.?net_sessionid|jsessionid|phpsessid|sessionid)\b"
                r"[\"']?\s*[=:]\s*[\"']?[A-Za-z0-9+/._\-]{8,}", re.I)),
    ("webstorage-dump-with-values",
     re.compile(r"\b(localstorage|sessionstorage)\b[^{\n]{0,40}\{[^}]*"
                r"[\"'][^\"']+[\"']\s*:\s*[\"'][^\"']{4,}", re.I)),
]


def scan(text: str) -> list[tuple[str, str]]:
    findings = []
    for name, rx in RULES:
        for m in rx.finditer(text):
            excerpt = text[max(0, m.start() - 20):m.end() + 10].replace("\n", " ")
            findings.append((name, excerpt))
    return findings


# --- regression fixtures -----------------------------------------------------
# NEG must stay CLEAN; every POS must be caught. If either direction breaks, the
# scanner is not to be trusted and selftest exits 3.
NEG_FIXTURES = {
    "assurance-sentence-and-public-evidence": (
        "Session use: visible search + Detay only. No cookie/token/header/"
        "localStorage/session material crossed the bridge.\n"
        "public_url: https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx"
        "?KararId=69a570df623c1e8c2dc00cbd6652b3c3090d9272852d30c58c4ceaf3ed4031a2\n"
        "content_hash: sha256:404320c73ef629d7 chars=28561 (canonical tool); "
        "source page hash 1b1440c34dd111c8"),
    "authorization-prose-without-credential": (
        "Authorization for OPREQ-215TFB-004: granted by operator 2026-07-28. "
        "authorization: pending review; do not send without the separate "
        "authority gate. Proxy-Authorization headers are never exported."),
}
POS_FIXTURES = {
    "session-cookie": "Set-Cookie: ASP.NET_SessionId=x4kq2vbn3rty8uio; path=/; HttpOnly",
    "bearer-token": "Authorization: Bearer eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJvcGVyYXRvciJ9.k9WqTz3v",
    "non-bearer-auth-header": "Proxy-Authorization: Basic dXNlcjpwYXNzd29yZA==",
    "opaque-auth-token": "authorization: 9f8e7d6c5b4a3210ffee1122",
    "storage-dump": 'localStorage: {"apiSecretKey": "9f8e7d6c5b4a3210ffee"}',
    "named-token-assignment": "refresh_token=1//0dXk2mPqLbn4vCgYIARAAGA0SNwF",
}


def selftest() -> int:
    ok = True
    for name, text in NEG_FIXTURES.items():
        got = scan(text)
        if got:
            ok = False
            print(f"SELFTEST FAIL: negative fixture '{name}' was flagged: {got}")
    for name, text in POS_FIXTURES.items():
        if not scan(text):
            ok = False
            print(f"SELFTEST FAIL: positive fixture '{name}' was NOT caught — scanner gone blind")
    print(f"SELFTEST OK: {len(NEG_FIXTURES)} negative passes, {len(POS_FIXTURES)} positives caught"
          if ok else "SELFTEST FAILED — do not trust this scanner's CLEAN verdict")
    return 0 if ok else 3


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__.strip().splitlines()[0], file=sys.stderr)
        return 2
    if argv[0] == "--selftest":
        return selftest()
    text = sys.stdin.read() if argv[0] == "-" else open(argv[0], encoding="utf-8", errors="replace").read()
    findings = scan(text)
    if not findings:
        print("CLEAN")
        return 0
    for name, excerpt in findings:
        print(f"LEAK [{name}]: …{excerpt}…")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
