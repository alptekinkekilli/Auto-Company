#!/usr/bin/env python3
"""Tell the operator when a MERSİS session is worth their time (APP-277 follow-up).

WHY THIS EXISTS. The company can discover firms without any human help — 16 distinct
procurements / 28 firms so far — but it cannot QUALIFY most of them alone. Since Rule 9
made trade directories discovery-only, the only accepted G4 bridge is a registry datum,
and MERSİS is CAPTCHA-gated, so every such lookup costs one operator keystroke. The
company therefore queues its requests in the Registry Bridge and waits. Nothing watched
that queue: on 2026-08-01 a PENDING Vestan request sat unnoticed until the operator asked
an unrelated question, and the cohort stayed one procurement short of its own gate.

WHAT IT REPORTS. Two different problems, deliberately separated:
  1. RESOLVABLE NOW — Registry Bridge rows in PENDING. These are ready-made questions;
     a single operator session clears them at ~1 CAPTCHA each.
  2. NOT EVEN ASKED — Ihale Outreach rows Held on attribution while NO bridge row names
     that firm. That is a company-side gap: it should have queued them. Reporting it
     separately keeps "the operator is the bottleneck" from hiding "we never asked".

It never writes to Airtable, never queues anything itself, and never edits a firm's
status. Advisory only.

Escalation: notify once at/above the threshold, then at most once per REPEAT_HOURS while
the queue stays non-empty; state in a small JSON file so a per-cycle caller cannot spam.
Clears itself when the queue empties, so the next backlog alerts immediately.

  registry-queue-watch.py [--app /app] [--threshold 3] [--repeat-hours 24] [--dry-run]
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
T_BRIDGE = "tblREW6MtTMTP5h5N"
T_OUTREACH = "tbl1fZbNmolrEXAMy"
# A Held row counts as "attribution-blocked" when its status says Held and its notes name
# the gate. Kept as substrings, not a regex, so the intent stays readable.
ATTRIBUTION_HINTS = ("G4", "attribution", "Rule 9", "Rule-9")


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
    """All records of a table (paginated), optionally filtered server-side."""
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", default=os.environ.get("AC_APP_DIR", "/app"))
    ap.add_argument("--threshold", type=int, default=int(os.environ.get("REGISTRY_QUEUE_THRESHOLD", "3")))
    ap.add_argument("--repeat-hours", type=float, default=float(os.environ.get("REGISTRY_QUEUE_REPEAT_HOURS", "24")))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    key = api_key(args.app)
    if not key:
        print("no AIRTABLE_API_KEY — cannot check the queue", file=sys.stderr)
        return 1

    try:
        pending = fetch(T_BRIDGE, key, "{status}='PENDING'")
        bridge_all = fetch(T_BRIDGE, key)
        outreach = fetch(T_OUTREACH, key)
    except Exception as exc:  # noqa: BLE001 — a watcher must not become an outage
        print(f"airtable read failed: {exc}", file=sys.stderr)
        return 1

    named = " ".join(str(r["fields"].get("firm", "")) for r in bridge_all).lower()
    unasked = []
    for r in outreach:
        f = r["fields"]
        status = str(f.get("Status", ""))
        if not status.startswith("Held"):
            continue
        notes = str(f.get("Notes", ""))
        if not any(h in notes for h in ATTRIBUTION_HINTS):
            continue
        biz = str(f.get("Business", "")).strip()
        # Match on the distinctive first word — bridge rows and outreach rows spell the
        # long legal titles differently (abbreviations, San./Tic.), so a whole-title
        # comparison would report every firm as unasked.
        token = biz.split()[0].lower() if biz else ""
        if token and token not in named:
            unasked.append(biz)

    print(f"bridge_pending={len(pending)} unasked_attribution_holds={len(unasked)}")

    state_path = os.path.join(args.app, "logs", ".registry-queue-state.json")
    if len(pending) < args.threshold and not (len(unasked) >= args.threshold * 2):
        if not args.dry_run:
            try:
                os.remove(state_path)
            except OSError:
                pass
        print("below threshold — silent")
        return 0

    now = datetime.now(timezone.utc)
    try:
        state = json.load(open(state_path, encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        state = {}
    last = state.get("last_notified_iso")
    if last and not args.dry_run:
        try:
            since = (now - datetime.fromisoformat(last)).total_seconds() / 3600.0
            if since < args.repeat_hours:
                print(f"notified {since:.1f}h ago — silent")
                return 0
        except ValueError:
            pass

    # The headline names whichever problem actually fired. Leading with "0 bekleyen
    # sorgu" because the OTHER branch tripped would train the operator to ignore this.
    lines = []
    if pending:
        lines.append(f"🔎 MERSİS oturumu zamanı — Registry Bridge kuyruğunda {len(pending)} bekleyen sorgu var.")
        for r in pending[:8]:
            f = r["fields"]
            lines.append(f"  • {f.get('request_id','?')} — {str(f.get('firm','?'))[:60]} (anahtar: {f.get('query_key','?')})")
        if len(pending) > 8:
            lines.append(f"  … +{len(pending) - 8} tane daha")
        lines += ["", "Her sorgu ~1 CAPTCHA; login operatöre ait. Claude'a 'MERSİS turu yapalım' de."]
        if unasked:
            lines += ["", f"Ayrıca {len(unasked)} firma atıf (G4) nedeniyle Held ama hiç bridge talebi açılmamış."]
    else:
        lines.append(f"📋 Registry Bridge kuyruğu BOŞ, ama {len(unasked)} firma atıf (G4) nedeniyle Held ve "
                     "hiçbiri için bridge talebi açılmamış.")
        lines += ["", "Bu operatör darboğazı DEĞİL — şirket bu firmalar için sorgu talebi açmamış. "
                      "Sorulmamış bir soruyu MERSİS turu çözmez; önce şirketin bunları kuyruğa alması gerekiyor."]
        lines += [f"  • {b[:60]}" for b in unasked[:5]]
        if len(unasked) > 5:
            lines.append(f"  … +{len(unasked) - 5} tane daha")
    msg = "\n".join(lines)

    if args.dry_run:
        print("--- would notify ---")
        print(msg)
        return 0

    notify_sh = os.path.join(args.app, "scripts", "core", "telegram-notify.sh")
    if os.path.exists(notify_sh):
        env = {**os.environ}
        for var in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"):
            if not env.get(var):
                try:
                    for line in open(os.path.join(args.app, "logs", "runtime.env"), encoding="utf-8", errors="replace"):
                        if line.startswith(var + "="):
                            env[var] = line.split("=", 1)[1].strip().strip('"').strip("'")
                except OSError:
                    pass
        try:
            subprocess.run(["bash", notify_sh, msg], capture_output=True, timeout=25, env=env)
        except Exception:  # noqa: BLE001
            pass

    state["last_notified_iso"] = now.isoformat()
    state["pending_at_notify"] = len(pending)
    try:
        tmp = state_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(state, fh)
        os.replace(tmp, state_path)
    except OSError as exc:
        print(f"state not persisted: {exc}", file=sys.stderr)
    print("notified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
