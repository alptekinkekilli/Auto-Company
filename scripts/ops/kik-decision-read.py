#!/usr/bin/env python3
"""Read a KİK decision in ONE call: parties, tender, outcome, and the canonical hash.

Reading three decisions cost a cycle its life on 2026-08-01: the loop fetched each one
through the browser, hit a transient server error, re-fetched through the hash script,
re-read the text, and repeated — 65 turns, 893 s, killed by the 900 s watchdog with the
classification unfinished and the tail work lost. None of that was thinking; it was
transport. This does the transport once, returns only the fields a G1/outcome call needs,
and bounds the bytes that enter the context.

What it extracts (all from the authority's own text, never from a mirror):
  * Karar No, Karar Tarihi, Toplantı / Gündem No
  * İdare (the contracting authority) and the İKN + subject of the tender
  * BAŞVURU SAHİBİ — the COMPLAINANT, which is not the excluded firm and has been confused
    for one before; a complainant recorded as an exclusion would put a false factual claim
    in front of a prospect
  * the operative sentence(s) — "… karar verildi" — which is where the outcome actually is
  * the canonical content hash, computed by scripts/core/decision_text_hash.py itself so the
    value is comparable with what the bridge recorded (a hash produced any other way is not)

Usage:
  kik-decision-read.py <KararId|url> [more…]
  kik-decision-read.py --json <KararId>          # full JSON instead of the digest
  kik-decision-read.py --chars 700 <KararId>     # widen the operative-section excerpt
"""
from __future__ import annotations

import argparse
import html
import importlib.util
import json
import pathlib
import re
import subprocess
import sys
import time

BASE = "https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId="
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

_HASH_SRC = pathlib.Path(__file__).resolve().parents[1] / "core" / "decision_text_hash.py"


def _hasher():
    """Reuse the ONE canonical implementation; never re-implement the normalisation."""
    spec = importlib.util.spec_from_file_location("decision_text_hash", _HASH_SRC)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["decision_text_hash"] = mod
    spec.loader.exec_module(mod)
    return mod


def fetch(url: str, attempts: int = 3) -> str:
    """curl, with a browser UA. urllib fails the TLS handshake against this host on macOS.

    KararGoster returns an empty body often enough that a single miss is not a finding — the
    cycle that died was partly spent re-fetching by hand after exactly this. Retry here, so
    the caller never has to spend a turn on it.
    """
    for i in range(attempts):
        r = subprocess.run(["curl", "-sSL", "-A", UA, "--max-time", "60", url],
                           capture_output=True, text=True, timeout=90)
        if len(r.stdout) > 2000:
            return r.stdout
        time.sleep(3 * (i + 1))
    return r.stdout


def text_of(raw: str) -> str:
    t = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", raw)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def first(text: str, pattern: str) -> str | None:
    m = re.search(pattern, text)
    return m.group(1) if m else None


def field(text: str, label: str, stop: str = r"[A-ZÇĞİÖŞÜ][A-ZÇĞİÖŞÜ ]{4,}:") -> str | None:
    m = re.search(re.escape(label) + r"\s*:?\s*(.{0,220})", text)
    if not m:
        return None
    val = m.group(1)
    cut = re.search(stop, val)
    if cut:
        val = val[:cut.start()]
    return val.strip(" :–-") or None


def read(url: str, chars: int) -> dict:
    if not url.startswith("http"):
        url = BASE + url
    raw = fetch(url)
    if not raw:
        return {"url": url, "status": "FETCH_FAILED"}
    text = text_of(raw)
    digest, n = _hasher().digest(raw.encode())

    out = {
        "url": url,
        "status": "OK",
        # These four have exact shapes; a generic label-to-next-label scrape drags in the
        # "Mahkeme Kararları / Toplantıya Katılan Üyeler" block that sits between them.
        "kararNo": first(text, r"Karar No\s*:\s*(\d{4}/[A-ZÇĞİÖŞÜ.]+-\d+)"),
        "kararTarihi": first(text, r"Karar Tarihi\s*:\s*(\d{2}\.\d{2}\.\d{4})"),
        "toplantiNo": first(text, r"Toplantı No\s*:\s*(\d{4}/\d+)"),
        "gundemNo": first(text, r"Gündem No\s*:\s*(\d+)"),
        "basvuruSahibi": field(text, "BAŞVURU SAHİBİ"),
        "idare": field(text, "İHALEYİ YAPAN İDARE"),
        "ihale": field(text, "BAŞVURUYA KONU İHALE"),
        "content_hash": "sha256:%s chars=%d (scripts/core/decision_text_hash.py)" % (digest, n),
        "chars": n,
    }
    # The outcome lives in the operative sentence, not in the summary — take the LAST one,
    # since a decision quotes earlier rulings before delivering its own.
    verdicts = [m for m in re.finditer(r"[^.]{0,260}karar verildi[^.]{0,60}\.", text)]
    out["sonuc"] = verdicts[-1].group(0).strip()[-chars:] if verdicts else None
    # "Değerlendirme dışı bırakılması" marks an exclusion — but the same words appear in the
    # legislation the decision QUOTES before applying it. A quoted article is not a finding
    # about anyone, and presenting one as an exclusion ground would be a false claim about a
    # real firm, so quotes are dropped rather than ranked.
    QUOTE = re.compile(r"maddesi|başlıklı|Yönetmelik|Kanun[’'`]?un|fıkras[ıi]nda|bendinde", re.I)
    excl = [e.strip() for e in
            re.findall(r"[^.]{0,200}değerlendirme dışı bırak[^.]{0,120}\.", text, re.I)
            if not QUOTE.search(e)]
    out["exclusionSentences"] = [e[:chars] for e in excl[:3]]
    out["exclusionNote"] = ("legislation quotes removed; empty means the decision states no "
                            "exclusion in its own voice") if not excl else None
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="+", help="KararId or full KurulKararGoster URL")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--chars", type=int, default=400)
    args = ap.parse_args()

    results = [read(i, args.chars) for i in args.ids]
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=1))
        return 0
    for r in results:
        if r["status"] != "OK":
            print("%s  %s" % (r["status"], r["url"][:90]))
            continue
        print("%s  (%s, Toplantı %s / Gündem %s)" % (r["kararNo"], r["kararTarihi"],
                                                     r["toplantiNo"], r["gundemNo"]))
        print("  idare          : %s" % (r["idare"] or "-"))
        print("  ihale          : %s" % (r["ihale"] or "-"))
        print("  başvuru sahibi : %s   <- COMPLAINANT, not an excluded firm" % (r["basvuruSahibi"] or "-"))
        print("  sonuç          : %s" % (r["sonuc"] or "-"))
        for e in r["exclusionSentences"]:
            print("  exclusion      : %s" % e)
        print("  %s" % r["content_hash"])
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
