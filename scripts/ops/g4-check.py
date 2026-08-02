#!/usr/bin/env python3
"""Decide G4 identity attribution from EVIDENCE, so nobody has to take "G4 PASS" on trust.

Why this exists (operator, 2026-08-02): the G4 task sat inside a directive whose completion
clause is built for an unbounded commercial validation, so a small, mechanically checkable
job could only be closed by a human saying so. That is the wrong gate in the wrong place.
The closing decision should follow the EVIDENCE, not the org chart — and it only belongs to
the operator where the evidence genuinely lives with them (inbox state, settled payment).
G4's evidence lives on the public web and in the register, so a script can rule on it.

## The one thing this must never do

Believe the row. If it simply grepped `result_notes` for "G4 PASS" it would be laundering a
self-declaration through a script — exactly the failure the completion clause was written to
stop. So the claim in the row is treated as an ASSERTION TO BE TESTED, never as input to the
verdict, and a row that claims PASS while the evidence fails is reported LOUDLY as
`CLAIMED_PASS_UNVERIFIED` rather than quietly downgraded.

## What a PASS requires (standing Rule 9), both halves, checked live

1. **First-party contact** — an address on the firm's own domain, established by the
   render-first examiner (`site-contact-evidence.py`), whose negatives are only trusted when
   a render actually happened.
2. **An anchor to the REGISTERED identity** — the firm's own pages carrying the registered
   address, or the MERSİS number, or the ticaret sicil number. A third-party directory can
   never be the anchor: directories match TRADING names, and one gave an address for RAYELSİS
   that conflicts with the register.

Anything less is a HOLD with the gap named. A named HOLD is a finding; a bare "insufficient"
is not.

  g4-check.py --record recXXXX [--record recYYYY]
  g4-check.py --all                 # every VERIFIED row in the registry bridge
  g4-check.py --record recXXXX --domain example.com.tr    # when the row names no site yet
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_DEFAULT = "appPLc31jSlgulX3D"
BRIDGE_TABLE = "tblREW6MtTMTP5h5N"
API_ROOT = "https://api.airtable.com/v0"

# Address abbreviations as the register writes them vs. how a website writes them. Matching
# without this fails on exactly the pair that motivated the tool: the register's
# "YENİ BATI MAH. 2374 SK. NO: 3" and the site's "Yeni Batı Mahallesi 2374 Sokak No: 3".
ABBREV = {
    "MAHALLESI": "MAH", "MAHALLE": "MAH", "MH": "MAH",
    "SOKAGI": "SK", "SOKAK": "SK", "SOK": "SK",
    "CADDESI": "CAD", "CADDE": "CAD", "CD": "CAD",
    "BULVARI": "BLV", "BULVAR": "BLV", "BUL": "BLV",
    "APARTMANI": "APT", "APARTMAN": "APT",
    "NUMARA": "NO", "NUMARASI": "NO",
    "ISMERKEZI": "ISMERKEZI", "SITESI": "SIT", "SITE": "SIT",
    "BLOK": "BLOK", "KAT": "KAT", "DAIRE": "D", "DAIRESI": "D",
}
# Words that carry no identifying power: present in every Turkish address.
STOP = {"MAH", "SK", "CAD", "BLV", "APT", "NO", "SIT", "KAT", "D", "BLOK", "TURKEY",
        "TURKIYE", "ISMERKEZI"}


def load_key(app_dir: str) -> None:
    if os.environ.get("AIRTABLE_API_KEY"):
        return
    try:
        fh = open(os.path.join(app_dir, "logs", "runtime.env"), encoding="utf-8", errors="replace")
    except OSError:
        fh = None
    if fh:
        with fh:
            for line in fh:
                k, _, v = line.strip().partition("=")
                if k.strip() == "AIRTABLE_API_KEY" and not os.environ.get(k.strip()):
                    os.environ["AIRTABLE_API_KEY"] = v.strip().strip('"').strip("'")
    if not os.environ.get("AIRTABLE_API_KEY") and sys.platform == "darwin":
        out = subprocess.run(["security", "find-generic-password", "-w",
                              "-s", "autocompany-airtable-pat"],
                             capture_output=True, text=True, timeout=10).stdout.strip()
        if out:
            os.environ["AIRTABLE_API_KEY"] = out


def norm(text: str) -> list[str]:
    """Turkish-aware address tokens. Casing matters here: dotted/dotless İ-I make a plain
    upper() produce tokens that never match, so fold explicitly before uppercasing."""
    t = (text or "")
    for a, b in (("ı", "i"), ("İ", "i"), ("ş", "s"), ("Ş", "s"), ("ğ", "g"), ("Ğ", "g"),
                 ("ü", "u"), ("Ü", "u"), ("ö", "o"), ("Ö", "o"), ("ç", "c"), ("Ç", "c")):
        t = t.replace(a, b)
    t = re.sub(r"[^A-Za-z0-9]+", " ", t).upper()
    return [ABBREV.get(w, w) for w in t.split() if w]


def address_anchor(registered: str, page_text: str) -> tuple[bool, str]:
    """Does the page carry the REGISTERED address? Returns (ok, explanation).

    Deliberately strict about the door number and at least one distinctive name token: a
    match on 'MAH SK NO' alone would fire on every address in Turkey.
    """
    reg = norm(registered)
    page = set(norm(page_text))
    if not reg:
        return False, "no registered address on the row to anchor against"
    numbers = [w for w in reg if w.isdigit()]
    names = [w for w in reg if not w.isdigit() and w not in STOP and len(w) > 2]
    hit_numbers = [n for n in numbers if n in page]
    hit_names = [n for n in names if n in page]
    # Two independent number hits (e.g. street 2374 + door 3), or one number plus a
    # distinctive name, is the bar. One lone number is a coincidence waiting to happen.
    strong = (len(hit_numbers) >= 2) or (hit_numbers and hit_names)
    detail = "numbers matched %s/%s (%s), name tokens %s/%s (%s)" % (
        len(hit_numbers), len(numbers), ",".join(hit_numbers) or "-",
        len(hit_names), len(names), ",".join(hit_names[:4]) or "-")
    return strong, detail


def registry_id_anchor(row_text: str, page_text: str) -> tuple[bool, str]:
    """The site printing a REGISTRY NUMBER for the firm: MERSİS, vergi no, or ticaret sicil.

    Operator, 2026-08-02: Turkish company sites are legally required to publish exactly this
    block (ünvan, MERSİS, sicil, vergi dairesi/no, registered address, KEP) — most simply do
    not comply. wowwo.com/iletisim is a compliant example and prints all of it. So when a
    site publishes none of it that is a fact about the SITE's compliance, not a doubt about
    the firm — but it also means there is nothing to anchor to, and the verdict stays HOLD.

    Digit length decides how much context is demanded, because a short number can coincide:
      16 digits (MERSİS)  — unique enough to accept bare
      10 digits (vergi no)— accept bare
      <=8 digits (sicil)  — only with a 'sicil' word nearby, or it would match a phone number,
                            a postcode, or a price
    """
    page = page_text or ""
    digits = re.sub(r"[^0-9]", "", page)
    low = page.lower()
    for m in re.findall(r"\b\d{16}\b", row_text or ""):
        if m in digits:
            return True, "site prints MERSİS no %s" % m
    for v in re.findall(r"\b\d{10}\b", row_text or ""):
        if v in digits:
            return True, "site prints vergi no %s" % v
    if "sicil" in low:
        for sn in re.findall(r"\b\d{4,8}\b", row_text or ""):
            if sn in digits:
                return True, "site prints ticaret sicil no %s (page mentions 'sicil')" % sn
    return False, ("site prints no registry number from the row (MERSİS / vergi no / sicil) — "
                   "note this is a site-compliance gap, not evidence against the firm")


def field(row_text: str, label: str) -> str:
    m = re.search(re.escape(label) + r"\s*:\s*([^|\n]+)", row_text or "")
    return m.group(1).strip() if m else ""


def domains_in(text: str) -> list[str]:
    found = []
    for u in re.findall(r"https?://([A-Za-z0-9.\-]+)", text or ""):
        d = u.lower().lstrip("www.")
        if d.endswith((".gov.tr", ".airtable.com")) or "kik.gov" in d or "mersis" in d:
            continue          # authority sources and our own tooling are not the firm's site
        if d not in found:
            found.append(d)
    return found


def air_get(base: str, table: str, rec: str) -> dict:
    req = urllib.request.Request("%s/%s/%s/%s" % (API_ROOT, base, table, rec),
                                 headers={"Authorization": "Bearer " + os.environ["AIRTABLE_API_KEY"]})
    return json.load(urllib.request.urlopen(req, timeout=45)).get("fields", {})


def air_list(base: str, table: str, formula: str) -> list[dict]:
    q = urllib.parse.urlencode({"filterByFormula": formula, "maxRecords": 50})
    req = urllib.request.Request("%s/%s/%s?%s" % (API_ROOT, base, table, q),
                                 headers={"Authorization": "Bearer " + os.environ["AIRTABLE_API_KEY"]})
    return json.load(urllib.request.urlopen(req, timeout=45)).get("records", [])


def site_evidence(domain: str, mcp: str) -> tuple[dict, str]:
    """Reuse the sanctioned render-first examiner, and take its page text for anchoring."""
    spec = importlib.util.spec_from_file_location("sce", os.path.join(HERE, "site-contact-evidence.py"))
    sce = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sce)
    res = sce.examine(domain, True, mcp)
    base = domain if domain.startswith("http") else "https://" + domain
    text = ""
    try:
        text += sce.render_dom(base, mcp) or ""
    except Exception:
        pass
    for path in ("/iletisim", "/iletisim/", "/contact", "/hakkimizda"):
        try:
            code, html = sce.fetch(urllib.parse.urljoin(base, path))
            if code == "200":
                text += " " + re.sub(r"<[^>]+>", " ", html)
        except Exception:
            pass
    return res, text


def judge(fields: dict, domain_override: str, mcp: str) -> dict:
    # Read the STRUCTURED fields too, not just the prose. The registry bridge has dedicated
    # columns (result_data, mersis_no, ticaret_sicil_no) and the address lives in result_data
    # on every properly-filled row — this checker only read result_notes and therefore
    # reported "no registered address on the row" for rows that plainly had one (Arkenom,
    # 2026-08-02). Same class as the label bug above: looking in one place and calling the
    # absence a finding.
    notes = "\n".join(str(fields.get(k) or "") for k in
                      ("result_notes", "result_data", "mersis_no", "ticaret_sicil_no"))
    firm = fields.get("firm", "") or ""
    claimed = bool(re.search(r"G4[^\n]{0,40}PASS", notes))
    # Accept every label the rows actually use. The first live run returned "no registered
    # address on the row" on a row that plainly had one — under a different label — and that
    # near-miss is the difference between a checker and a rubber stamp pointed the other way.
    registered = ""
    for label in ("Tescilli Adres (MERKEZ)", "Tescilli Adres", "Firma Adres Bilgisi",
                  "Adres", "Registered address"):
        # result_data is pipe-separated ("... | Adres: X | E-tebligat: ...") so stop at the
        # separator, or the "address" swallows the rest of the line and matches nothing.
        registered = field(notes, label)
        if registered:
            break
    doms = [domain_override] if domain_override else domains_in(notes)
    out = {"firm": firm[:70], "claims_pass": claimed, "domain": doms[0] if doms else None}

    if not doms:
        out["verdict"] = "HOLD"
        out["reason"] = "no candidate domain recorded on the row and none given with --domain"
        return out

    res, text = site_evidence(doms[0], mcp)
    out["site_verdict"] = res.get("verdict")
    out["first_party"] = sorted(res.get("first_party") or [])
    if res.get("verdict") != "FOUND_FIRST_PARTY":
        out["verdict"] = "HOLD"
        out["reason"] = "no first-party contact: examiner says %s" % res.get("verdict")
        return out

    ok_addr, addr_detail = address_anchor(registered, text)
    ok_id, id_detail = registry_id_anchor(notes, text)
    out["anchor_address"] = addr_detail
    out["anchor_registry_id"] = id_detail
    if not (ok_addr or ok_id):
        out["verdict"] = "HOLD"
        out["reason"] = ("first-party contact found, but nothing anchors it to the REGISTERED "
                         "identity — %s; %s" % (addr_detail, id_detail))
        return out
    out["verdict"] = "PASS"
    out["reason"] = "first-party %s + %s" % (
        ",".join(out["first_party"][:2]), "registered address on site" if ok_addr else id_detail)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--app", default=os.environ.get("APP_DIR", "/app"))
    ap.add_argument("--base", default=BASE_DEFAULT)
    ap.add_argument("--table", default=BRIDGE_TABLE)
    ap.add_argument("--record", action="append", default=[])
    ap.add_argument("--all", action="store_true", help="every VERIFIED row in the bridge table")
    ap.add_argument("--domain", default="", help="site to examine, when the row names none")
    ap.add_argument("--mcp", default=os.environ.get("BROWSEROS_MCP", "http://172.17.0.1:9245/mcp"))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    load_key(args.app)
    if not os.environ.get("AIRTABLE_API_KEY"):
        print("AIRTABLE_API_KEY not found (env, %s/logs/runtime.env, Keychain)" % args.app,
              file=sys.stderr)
        return 2

    rows = []
    if args.all:
        for r in air_list(args.base, args.table, "{status}='VERIFIED'"):
            rows.append((r["id"], r.get("fields", {})))
    for rec in args.record:
        rows.append((rec, air_get(args.base, args.table, rec)))
    if not rows:
        print("nothing to check: pass --record or --all", file=sys.stderr)
        return 2

    results, bad = [], 0
    for rec, fields in rows:
        v = judge(fields, args.domain, args.mcp)
        v["record"] = rec
        # The anti-self-certification case, called out rather than folded into HOLD.
        if v["claims_pass"] and v["verdict"] != "PASS":
            v["verdict"] = "CLAIMED_PASS_UNVERIFIED"
        results.append(v)
        bad += v["verdict"] != "PASS"

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=1))
    else:
        for v in results:
            print("[G4 %s] %s (%s)" % (v["verdict"], v["firm"], v.get("domain") or "no domain"))
            print("    %s" % v.get("reason", ""))
            if v.get("anchor_address"):
                print("    address anchor: %s" % v["anchor_address"])
        print("%d/%d PASS" % (len(results) - bad, len(results)))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
