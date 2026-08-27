#!/usr/bin/env python3
"""Anonim OPEX RFQ göndericisi — §15-gated, ForwardEmail doğrudan API. FAIL-CLOSED.

Bu, tender send-gate.py'ın RFQ kardeşidir ama ÜÇ noktada ayrılır (bkz. plan
dynamic-wiggling-cloud / Linear APP-269 ray doğrulaması):

  1. §15 KAPISI — her gönderim, Airtable "Sponsor İzni" checkbox'ı TRUE ise mümkün.
     Loop/makine bu kutuyu SET EDEMEZ; işaretleyemediği için tüm gönderimler operatör
     iznine kadar fail-closed REFUSE. Tender'ın "otonom dispatch"inin TERSİ.
  2. G4 YOK — biz ALICIYIZ (vendor'dan teklif istiyoruz); alıcının tüzel-kişilik atfı
     (satıcı-tarafı G4 gate) anlamsız.
  3. AYRI TABLO — frozen tender "Ihale Outreach"a DOKUNMAZ; kendi "Wowcar OPEX RFQ"
     tablosunu (tblzcGP7kNfkmPDGJ) okur/yazar.

Anonimlik: gönderilen metinde son-şirket adı/marka/hacim YOKTUR; gönderen Appricode
tedarik/danışmanlık, ismi açıklanmayan müşteri adına indikatif fiyat toplar.

Teslim: ForwardEmail /v1/emails (go.appricode.tr, has_smtp=True — 2026-08-27 doğrulandı).
Yalnız e-postalı vendor'lara; form-only vendor'lar REFUSE ("manuel") — makine form doldurmaz.

  rfq-send.py --record recXXXX            # bir vendor: ALLOW/REFUSE + render (dry-run)
  rfq-send.py --record recXXXX --send     # §15 TRUE ise gerçekten gönder
  rfq-send.py --report                     # caps + kimler eligible
"""
from __future__ import annotations

import argparse
import base64
import datetime as _dt
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

API_ROOT = "https://api.airtable.com/v0"
BASE = "appPLc31jSlgulX3D"
TABLE = "tblzcGP7kNfkmPDGJ"          # Wowcar OPEX RFQ — tender tablolarından AYRI
FE_ENDPOINT = "https://api.forwardemail.net/v1/emails"
FROM_EMAIL = "tedarik@go.appricode.tr"
FROM_NAME = "Appricode — Tedarik / Danışmanlık"
DAILY_CAP = 3
TOTAL_CAP = 20

# Anonimlik denylist — render edilen metin bunlardan HERHANGİ birini içerirse gönderim
# REFUSE (son-şirket adı/marka asla sızmamalı; isim değişecek olsa da bugünkü aday dahil).
ANON_DENY = ("wowcar",)

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")

# İçerik (subject/body/scope + imza) AYRI, protected-OLMAYAN modülde: rfq_template.py.
# Metni orada serbestçe iterasyona açık tut; send mantığı (§15/caps/teslim) burada korunur.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rfq_template  # noqa: E402
SCOPE = rfq_template.SCOPE


# ── anahtar yükleme (env → runtime.env → Keychain), send-gate deseni ──────────────
def _load_key(env_name: str, keychain_service: str) -> str | None:
    if os.environ.get(env_name):
        return os.environ[env_name]
    rt = os.path.join(_app_dir(), "logs", "runtime.env")
    try:
        for line in open(rt, encoding="utf-8"):
            if line.strip().startswith(env_name + "="):
                v = line.split("=", 1)[1].strip().strip('"').strip("'")
                if v:
                    os.environ[env_name] = v
                    return v
    except OSError:
        pass
    try:
        out = subprocess.run(["security", "find-generic-password", "-w", "-s", keychain_service],
                             capture_output=True, text=True, timeout=8).stdout.strip()
        if out:
            os.environ[env_name] = out
            return out
    except Exception:
        pass
    return None


def _app_dir() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", ".."))


# ── Airtable ──────────────────────────────────────────────────────────────────────
def _air(method: str, path: str, params: dict | None = None, body: dict | None = None) -> dict:
    key = _load_key("AIRTABLE_API_KEY", "autocompany-airtable-pat")
    if not key:
        raise SystemExit("AIRTABLE_API_KEY yok (env/runtime.env/Keychain)")
    url = f"{API_ROOT}/{BASE}/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def _record(rec: str) -> dict:
    return _air("GET", f"{urllib.parse.quote(TABLE)}/{rec}")


def _all_rows() -> list[dict]:
    out, offset = [], None
    while True:
        p = {"pageSize": 100}
        if offset:
            p["offset"] = offset
        d = _air("GET", urllib.parse.quote(TABLE), params=p)
        out += d.get("records", [])
        offset = d.get("offset")
        if not offset:
            break
    return out


# ── eligibility parçaları ───────────────────────────────────────────────────────
def _sponsor_ok(f: dict) -> bool:
    return f.get("Sponsor İzni") is True          # fail-closed: yok/false → False


def _opted_out(f: dict) -> bool:
    return bool(f.get("Opt-out"))


def _already_sent(f: dict) -> bool:
    return f.get("Durum") == "Gönderildi" or bool(f.get("Gönderim TS"))


def _email_of(f: dict) -> str | None:
    m = EMAIL_RE.search(f.get("Kanal", "") or "")
    return m.group(0) if m else None


def _caps_now() -> tuple[int, int]:
    today = _dt.datetime.now(_dt.timezone.utc).date().isoformat()
    total = day = 0
    for r in _all_rows():
        f = r.get("fields", {})
        ts = f.get("Gönderim TS") or ""
        if f.get("Durum") == "Gönderildi" or ts:
            total += 1
            if str(ts).startswith(today):
                day += 1
    return day, total


def render(f: dict) -> tuple[str, str]:
    sablon = f.get("Şablon", "")
    scope = SCOPE.get(sablon)
    if not scope:
        raise ValueError(f"bilinmeyen şablon: {sablon!r}")
    kume = f.get("Küme", "")
    return (rfq_template.subject(kume),
            rfq_template.body(kume, scope),
            rfq_template.body_html(kume, scope))


def anonymity_scan(text: str) -> str | None:
    low = text.lower()
    for bad in ANON_DENY:
        if bad in low:
            return f"anonimlik ihlali: '{bad}' render edilen metinde"
    return None


def decide(f: dict) -> dict:
    if _opted_out(f):
        return {"ok": False, "reason": "opt-out"}
    if _already_sent(f):
        return {"ok": False, "reason": "zaten gönderildi (never-twice)"}
    email = _email_of(f)
    if not email:
        return {"ok": False, "reason": "form-only vendor — manuel gönderim (makine form doldurmaz)"}
    try:
        subject, text, html = render(f)
    except ValueError as e:
        return {"ok": False, "reason": str(e)}
    leak = anonymity_scan(subject + "\n" + text + "\n" + html)
    if leak:
        return {"ok": False, "reason": leak}
    day, total = _caps_now()
    if day >= DAILY_CAP:
        return {"ok": False, "reason": f"günlük cap dolu ({day}/{DAILY_CAP})"}
    if total >= TOTAL_CAP:
        return {"ok": False, "reason": f"toplam cap dolu ({total}/{TOTAL_CAP})"}
    if not _sponsor_ok(f):        # §15 — EN SON, en pahalı; hepsi geçse bile izin şart
        return {"ok": False, "reason": "§15 Sponsor İzni YOK (fail-closed) — operatör işaretlemeli"}
    return {"ok": True, "reason": "ALLOW", "email": email,
            "subject": subject, "text": text, "html": html}


# ── ForwardEmail teslim ─────────────────────────────────────────────────────────
def _encode_subject(s: str) -> str:
    # RFC 2047: tüm konuyu tek encoded-word yap (Türkçe karakter mangle olmasın).
    b = base64.b64encode(s.encode("utf-8")).decode("ascii")
    return f"=?UTF-8?B?{b}?="


def send_fe(to: str, subject: str, text: str, html: str = "") -> dict:
    key = _load_key("FORWARDEMAIL_API_KEY", "autocompany-forwardemail-key")
    if not key:
        raise SystemExit("FORWARDEMAIL_API_KEY yok (env/runtime.env/Keychain)")
    auth = base64.b64encode(f"{key}:".encode()).decode("ascii")
    fields = {
        "from": f"{FROM_NAME} <{FROM_EMAIL}>",
        "to": to,
        "subject": _encode_subject(subject),
        "text": text,        # text/plain FIRST (MIME alternatif sırası: az→çok tercih)
    }
    if html:
        fields["html"] = html
    form = urllib.parse.urlencode(fields).encode("utf-8")
    req = urllib.request.Request(FE_ENDPOINT, data=form, method="POST", headers={
        "Authorization": "Basic " + auth,
        "Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return {"status": r.status, "body": json.loads(r.read().decode("utf-8", "replace"))}


def _mark_sent(rec: str) -> None:
    now = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M")
    _air("PATCH", f"{urllib.parse.quote(TABLE)}/{rec}",
         body={"fields": {"Durum": "Gönderildi", "Gönderim TS": now}})


# ── CLI ────────────────────────────────────────────────────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--record")
    ap.add_argument("--send", action="store_true", help="§15 TRUE ise gerçekten gönder")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()

    if a.report:
        day, total = _caps_now()
        rows = _all_rows()
        elig = [r for r in rows if decide(r["fields"]).get("ok")]
        print(f"caps: bugün {day}/{DAILY_CAP}, toplam {total}/{TOTAL_CAP}")
        print(f"kayıt: {len(rows)}, ALLOW: {len(elig)}")
        for r in elig:
            print("  ALLOW:", r["fields"].get("Firma"))
        for r in rows:
            d = decide(r["fields"])
            if not d.get("ok"):
                print(f"  REFUSE [{r['fields'].get('Firma')}]: {d['reason']}")
        return 0

    if not a.record:
        ap.error("--record veya --report gerekli")
    f = _record(a.record).get("fields", {})
    d = decide(f)
    firma = f.get("Firma", "?")
    if not d["ok"]:
        print(f"REFUSE [{firma}]: {d['reason']}")
        return 0
    print(f"ALLOW [{firma}] → {d['email']}")
    print("SUBJECT:", d["subject"])
    print("---- BODY ----"); print(d["text"]); print("---- /BODY ----")
    if not a.send:
        print("(dry-run — gönderim için --send)")
        return 0
    res = send_fe(d["email"], d["subject"], d["text"], d.get("html", ""))
    ok = 200 <= res["status"] < 300 and res["body"].get("_id") or res["body"].get("id")
    if ok:
        _mark_sent(a.record)
        print(f"GÖNDERİLDİ id={res['body'].get('_id') or res['body'].get('id')}")
    else:
        print(f"GÖNDERİM BAŞARISIZ status={res['status']} body={str(res['body'])[:200]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
