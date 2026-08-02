#!/usr/bin/env python3
"""Tell the operator the moment an outreach message produces an OUTCOME — reply, bounce or silence.

WHY THIS EXISTS. Five real messages went out on 2026-08-01. The reply path is already
automatic: the inbound worker writes `Replied` / `Reply log` / `Last reply date` onto the
firm's row, and the send path writes `Email log`. Nothing WATCHED any of it, so the outcome
of a send was only ever discovered by a human remembering to open a mailbox — and the whole
serialised send order ("#2 waits for #1's observed outcome") depends on noticing.

THREE OUTCOMES, deliberately separated, because they mean different things:

  1. REPLY — a firm answered. Alert immediately, once per row. This is the only outcome
     that can change what the company does next, and a reply naming a live İKN opens a
     Stage 2 operator request.
  2. DELIVERY FAILURE — the `Email log` records Failed / bounce / suppressed / capped. A
     message that never arrived is NOT silence, and treating it as silence would let a
     broken address masquerade as "no interest".
  3. SILENCE — no reply after `--silence-hours`. Reported once per row, as a fact with its
     age, never as a verdict: "no reply after N hours" is an observation the operator may
     act on; "not interested" is a conclusion this script must not draw.

It is advisory. It never writes to Airtable, never queues, never re-sends, never marks a
firm closed-lost. State lives in a small JSON file so a per-cycle caller cannot spam, and
each row alerts once per outcome class.

  reply-watch.py [--app /app] [--silence-hours 72] [--dry-run]
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
T_OUTREACH = "tbl1fZbNmolrEXAMy"
STATE = "logs/reply-watch-state.json"
# Substrings that mean the message did not land. Kept literal so the intent stays readable.
FAILURE_HINTS = ("Failed", "bounce", "Bounce", "Suppressed", "Capped", "rejected", "5.1.1")


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
        url = f"https://api.airtable.com/v0/{BASE}/{table}?{urllib.parse.urlencode(params)}"
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
                env.setdefault(k, v.strip().strip('"').strip("'"))
                env[k] = v.strip().strip('"').strip("'")
    except OSError:
        pass
    subprocess.run(["bash", script], input=text, text=True, env=env,
                   capture_output=True, timeout=45, check=False)


def first_ts(log: str) -> str | None:
    """The timestamp of the newest entry — the worker prepends, so it is the first line."""
    line = (log or "").strip().split("\n")[0]
    if line.startswith("[") and "]" in line:
        return line[1:line.index("]")]
    return None


def hours_since(stamp: str | None) -> float | None:
    if not stamp:
        return None
    try:
        t = datetime.strptime(stamp.replace("Z", "+0000"), "%Y-%m-%dT%H:%M:%S.%f%z")
    except ValueError:
        try:
            t = datetime.strptime(stamp.replace("Z", "+0000"), "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            return None
    return (datetime.now(timezone.utc) - t).total_seconds() / 3600.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", default=os.environ.get("AC_APP_DIR", "/app"))
    ap.add_argument("--silence-hours", type=float,
                    default=float(os.environ.get("REPLY_SILENCE_HOURS", "72")))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--fixture", default=None,
                    help="TEST ONLY: read records from a JSON file instead of Airtable")
    args = ap.parse_args()

    if args.fixture:
        rows = json.loads(open(args.fixture, encoding="utf-8").read())
        return classify(rows, args)

    key = api_key(args.app)
    if not key:
        print("no AIRTABLE_API_KEY — cannot check replies", file=sys.stderr)
        return 1

    try:
        # Sent, real firms only. TEST rows carry their own statuses and their "replies" are
        # the operator answering themselves — counting those as outcomes would be a lie.
        rows = fetch(T_OUTREACH, key,
                     "AND({Email queue}='Sent', NOT(FIND('TEST', {Status})))")
    except Exception as exc:  # noqa: BLE001 — a watcher must not become an outage
        print(f"airtable read failed: {exc}", file=sys.stderr)
        return 1
    return classify(rows, args)


def classify(rows: list[dict], args) -> int:
    """Everything after the fetch: same code path for production and for the fixtures."""
    state_path = os.path.join(args.app, STATE)
    try:
        state = json.loads(open(state_path, encoding="utf-8").read())
    except (OSError, json.JSONDecodeError):
        state = {}

    replies, failures, silent = [], [], []
    for r in rows:
        f = r["fields"]
        rid = r["id"]
        name = str(f.get("Business", "?"))[:48]
        seen = state.get(rid, {})
        elog = str(f.get("Email log", ""))
        rlog = str(f.get("Reply log", ""))
        sent_at = first_ts(elog)

        if (f.get("Replied") or rlog.strip()) and not seen.get("reply"):
            replies.append((name, first_ts(rlog) or "?", rlog.strip().split("\n")[0][:160]))
            seen["reply"] = True
        # A failure that a later attempt SUPERSEDED is not a delivery problem. Measured
        # 2026-08-02: Rayelsis logged "Failed: Missing Email/subject/body" at 14:22 and
        # "Sent" at 14:26 — the message arrived, and reporting it as undelivered would send
        # the operator chasing a resolved event. The rule "an undelivered message is not
        # silence" still stands; this only decides WHETHER it is still undelivered.
        bad_lines = [ln for ln in elog.split("\n") if any(h in ln for h in FAILURE_HINTS)]
        ok_lines = [ln for ln in elog.split("\n")
                    if "Sent:" in ln and not any(h in ln for h in FAILURE_HINTS)]
        last_bad = max((first_ts(ln) or "" for ln in bad_lines), default="")
        last_ok = max((first_ts(ln) or "" for ln in ok_lines), default="")
        unresolved = bool(last_bad) and last_bad > last_ok
        if unresolved and not seen.get("failure"):
            failures.append((name, bad_lines[0][:160] if bad_lines else elog[:160]))
            seen["failure"] = True
        age = hours_since(sent_at)
        if (age is not None and age >= args.silence_hours
                and not seen.get("reply") and not seen.get("silence")):
            silent.append((name, age))
            seen["silence"] = True
        state[rid] = seen

    print(f"sent_rows={len(rows)} new_replies={len(replies)} "
          f"new_failures={len(failures)} newly_silent={len(silent)}")

    lines: list[str] = []
    if replies:
        lines.append("📬 CEVAP GELDİ — outreach:")
        lines += [f"  • {n} ({t})\n    {snippet}" for n, t, snippet in replies]
        lines.append("")
        lines.append("Canlı bir İKN yazdıysa Stage 2 için AYRI operatör yetkisi gerekiyor.")
    if failures:
        lines.append("⚠️ TESLİMAT SORUNU — mesaj ulaşmamış olabilir:")
        lines += [f"  • {n}\n    {msg}" for n, msg in failures]
        lines.append("")
        lines.append("Teslim edilmemiş bir mesaj SESSİZLİK DEĞİLDİR — sonuç sayma.")
    if silent:
        lines.append(f"🕐 {args.silence_hours:.0f} saattir cevap yok:")
        lines += [f"  • {n} ({age:.0f} sa)" for n, age in silent]
        lines.append("")
        lines.append("Bu bir gözlem, bir hüküm değil: 'ilgilenmiyor' sonucunu bu script çıkarmaz.")

    if lines:
        text = "\n".join(lines)
        print("--- would notify ---" if args.dry_run else "--- notifying ---")
        print(text)
        if not args.dry_run:
            notify(args.app, text)
    else:
        print("no new outcomes — silent")

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
