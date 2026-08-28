#!/usr/bin/env python3
"""RFQ (OPEX tedarik) yanıtlarını FARK ET ve operatöre haber ver — advisory, YAZMAZ.

Bu, tender `reply-watch.py`'ın RFQ ikizidir. Tender'da olduğu gibi iki parçalı bir
mimarinin İKİNCİ yarısıdır: CF Worker `/inbound` gelen bir yanıtı RFQ satırına YAZAR
(`Reply log` + `Son yanıt`); bu script yalnız NOTİCE eder. Ayrıldığı noktalar:

  1. AYRI TABLO — Wowcar OPEX RFQ (tblzcGP7kNfkmPDGJ), tender "Ihale Outreach"a DOKUNMAZ.
  2. ALICI dili — biz teklif İSTİYORUZ; "İKN / Stage 2" gibi tender-satıcı dili YOK.
     Nötr: "yanıt geldi" / "N saattir sessiz". Anonimlik: son-şirket adı hiç geçmez.
  3. İki outcome — REPLY ve SILENCE. rfq-send.py başarısız gönderimi satıra yazmaz
     (yalnız başarıda Durum=Gönderildi + Gönderim TS), o yüzden tender'ın "teslimat
     sorunu" dalı burada YOK; olmayan bir alanı outcome sayamayız.

Advisory: Airtable'a asla yazmaz, kuyruğa atmaz, yeniden göndermez. State küçük bir JSON
dosyasında, her satır her outcome-sınıfı için bir kez uyarır (per-cycle çağıran spam yapamaz).

  rfq-reply-watch.py [--app /app] [--silence-hours 72] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

BASE = "appPLc31jSlgulX3D"
TABLE = "tblzcGP7kNfkmPDGJ"        # Wowcar OPEX RFQ — tender tablosundan AYRI
STATE = "logs/rfq-reply-watch-state.json"


def api_key(app: str) -> str:
    key = os.environ.get("AIRTABLE_API_KEY", "")
    if key:
        return key
    try:
        for line in open(os.path.join(app, "logs", "runtime.env"), encoding="utf-8", errors="replace"):
            if line.startswith("AIRTABLE_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except OSError:
        pass
    return ""


def fetch(table: str, key: str, formula: str = "") -> list[dict]:
    out, offset = [], None
    while True:
        params = {"pageSize": "100"}
        if formula:
            params["filterByFormula"] = formula
        if offset:
            params["offset"] = offset
        url = f"https://api.airtable.com/v0/{BASE}/{urllib.parse.quote(table)}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}"})
        with urllib.request.urlopen(req, timeout=25) as resp:
            data = json.loads(resp.read().decode())
        out.extend(data.get("records", []))
        offset = data.get("offset")
        if not offset:
            return out


def notify(app: str, text: str) -> None:
    script = os.path.join(app, "scripts", "core", "telegram-notify.sh")
    if not os.path.exists(script):
        return
    env = dict(os.environ)
    try:  # the loop's own secret file; a fresh shell never sourced it
        for line in open(os.path.join(app, "logs", "runtime.env"), encoding="utf-8", errors="replace"):
            if line.startswith(("TELEGRAM_BOT_TOKEN=", "TELEGRAM_CHAT_ID=")):
                k, v = line.split("=", 1)
                env[k] = v.strip().strip('"').strip("'")
    except OSError:
        pass
    subprocess.run(["bash", script], input=text, text=True, env=env,
                   capture_output=True, timeout=45, check=False)


def first_ts(log: str) -> str | None:
    """En yeni girdinin zaman damgası — worker başa ekler, ilk satır en yenidir."""
    line = (log or "").strip().split("\n")[0]
    if line.startswith("[") and "]" in line:
        return line[1:line.index("]")]
    return None


def hours_since(stamp: str | None) -> float | None:
    """rfq-send 'Gönderim TS'yi UTC '%Y-%m-%dT%H:%M' (tz'siz) yazar; worker 'Reply log'a
    tam ISO (…Z / +00:00, saniyeli/mikrosaniyeli) yazar. Hepsini UTC kabul et."""
    if not stamp:
        return None
    s = stamp.strip().replace("Z", "+0000")
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M"):
        try:
            t = datetime.strptime(s, fmt)
            if t.tzinfo is None:
                t = t.replace(tzinfo=timezone.utc)
            return (datetime.now(timezone.utc) - t).total_seconds() / 3600.0
        except ValueError:
            continue
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", default=os.environ.get("AC_APP_DIR", "/app"))
    ap.add_argument("--silence-hours", type=float,
                    default=float(os.environ.get("RFQ_REPLY_SILENCE_HOURS", "72")))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--fixture", default=None,
                    help="TEST ONLY: read records from a JSON file instead of Airtable")
    args = ap.parse_args()

    if args.fixture:
        rows = json.loads(open(args.fixture, encoding="utf-8").read())
        return classify(rows, args)

    key = api_key(args.app)
    if not key:
        print("no AIRTABLE_API_KEY — cannot check RFQ replies", file=sys.stderr)
        return 1

    try:
        # Yalnız gönderilmiş satırlar. Gönderilmemiş bir vendor'ın "sessizliği" outcome değil.
        rows = fetch(TABLE, key, "OR({Durum}='Gönderildi', NOT({Gönderim TS}=BLANK()))")
    except Exception as exc:  # noqa: BLE001 — a watcher must not become an outage
        print(f"airtable read failed: {exc}", file=sys.stderr)
        return 1
    return classify(rows, args)


def classify(rows: list[dict], args) -> int:
    """Fetch sonrası her şey: prod ve fixture aynı kod yolundan geçer."""
    state_path = os.path.join(args.app, STATE)
    try:
        state = json.loads(open(state_path, encoding="utf-8").read())
    except (OSError, json.JSONDecodeError):
        state = {}

    replies, silent = [], []
    for r in rows:
        f = r["fields"]
        rid = r["id"]
        name = str(f.get("Firma", "?"))[:48]
        kume = str(f.get("Küme", ""))[:24]
        seen = state.get(rid, {})
        rlog = str(f.get("Reply log", ""))
        sent_at = f.get("Gönderim TS") or ""

        if rlog.strip() and not seen.get("reply"):
            replies.append((name, kume, first_ts(rlog) or "?", rlog.strip().split("\n")[0][:160]))
            seen["reply"] = True
        age = hours_since(sent_at)
        if (age is not None and age >= args.silence_hours
                and not rlog.strip() and not seen.get("silence")):
            silent.append((name, kume, age))
            seen["silence"] = True
        state[rid] = seen

    print(f"sent_rows={len(rows)} new_replies={len(replies)} newly_silent={len(silent)}")

    lines: list[str] = []
    if replies:
        lines.append("📬 RFQ YANITI GELDİ — tedarik teklifi:")
        lines += [f"  • {n} [{k}] ({t})\n    {snippet}" for n, k, t, snippet in replies]
        lines.append("")
        lines.append("Teklifi RFQ tablosuna işleyip (Yanıt alanı) OPEX mutabakatına al.")
    if silent:
        lines.append(f"🕐 {args.silence_hours:.0f} saattir RFQ yanıtı yok:")
        lines += [f"  • {n} [{k}] ({age:.0f} sa)" for n, k, age in silent]
        lines.append("")
        lines.append("Bu bir gözlem, bir hüküm değil: takip/hatırlatma operatör kararıdır.")

    if lines:
        text = "\n".join(lines)
        print("--- would notify ---" if args.dry_run else "--- notifying ---")
        print(text)
        if not args.dry_run:
            notify(args.app, text)
    else:
        print("no new RFQ outcomes — silent")

    if not args.dry_run:
        try:
            os.makedirs(os.path.dirname(state_path), exist_ok=True)
            with open(state_path, "w", encoding="utf-8") as fh:
                json.dump(state, fh, indent=1)
        except OSError as exc:
            print(f"could not persist state: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
