#!/usr/bin/env python3
"""Alert when the human directive has been PENDING too long (APP-276 follow-up).

WHY: `human-directive.md` is a single slot holding ONE live instruction. Its own
Completion clause can only be satisfied by market evidence or an explicit terminal
decision — neither of which the company can produce alone. So a directive whose
preconditions the operator has not met simply sits PENDING, silently, while every
cycle correctly reports "no completion route met" and every analyst run is correctly
BLOCKED from replacing it. Measured 2026-08-01: the 2026-07-31T04:58Z directive had
been PENDING for 31 hours and the operator only found out by asking.

This watcher is the missing signal. It does NOT judge the directive, never edits it,
and never clears anything — it reports age and escalates on a schedule:

    >= WARN_HOURS   one notice, then one per REPEAT_HOURS while it stays PENDING
    (state is kept in a small JSON file so a 15-minute cron does not spam)

It also reports the two facts that explain WHY it is stuck, straight from the audit
logs: the most recent write-refusal (an operator tried to replace it and the in-flight
gate said no) and the most recent promotion block (the analyst tried and was blocked).

Usage:
  directive-staleness-watch.py [--app /app] [--warn-hours 12] [--repeat-hours 12]
  directive-staleness-watch.py --dry-run     # print, never notify, never touch state
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

UPDATED_RE = re.compile(r"^##\s*Updated\s*$", re.MULTILINE)
STATUS_RE = re.compile(r"^##\s*Status\s*\n+(\S+)", re.MULTILINE)


def read_directive(path: str) -> tuple[str, datetime | None]:
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return "MISSING", None
    m = STATUS_RE.search(text)
    status = m.group(1).strip().upper() if m else "UNPARSEABLE"
    updated = None
    m2 = UPDATED_RE.search(text)
    if m2:
        tail = text[m2.end():].strip().splitlines()
        if tail:
            try:
                updated = datetime.fromisoformat(tail[0].strip().replace("Z", "+00:00"))
            except ValueError:
                updated = None
    return status, updated


def last_line_matching(path: str, needle: str) -> str:
    """Last line of a log containing `needle` — the audit trail's own words, not a paraphrase."""
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            hits = [ln.strip() for ln in fh if needle in ln]
        return hits[-1] if hits else ""
    except OSError:
        return ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", default=os.environ.get("AC_APP_DIR", "/app"))
    ap.add_argument("--warn-hours", type=float, default=float(os.environ.get("DIRECTIVE_WARN_HOURS", "12")))
    ap.add_argument("--repeat-hours", type=float, default=float(os.environ.get("DIRECTIVE_REPEAT_HOURS", "12")))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    app = args.app
    directive = os.path.join(app, "memories", "human-directive.md")
    state_path = os.path.join(app, "logs", ".directive-staleness-state.json")
    notify_sh = os.path.join(app, "scripts", "core", "telegram-notify.sh")

    status, updated = read_directive(directive)
    now = datetime.now(timezone.utc)

    if status != "PENDING":
        # Not pending → clear the state so the NEXT pending period starts fresh.
        if not args.dry_run:
            try:
                os.remove(state_path)
            except OSError:
                pass
        print(f"status={status} — nothing to watch")
        return 0

    if updated is None:
        age_h = -1.0
        age_txt = "unknown age (## Updated unparseable)"
    else:
        age_h = (now - updated).total_seconds() / 3600.0
        age_txt = f"{age_h:.1f}h (since {updated.isoformat()})"

    print(f"status=PENDING age={age_txt}")
    if 0 <= age_h < args.warn_hours:
        return 0

    # Escalation bookkeeping: notify once at the threshold, then every repeat-hours.
    state = {}
    try:
        state = json.load(open(state_path, encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        state = {}
    last_notified = state.get("last_notified_iso")
    if last_notified and not args.dry_run:
        try:
            since = (now - datetime.fromisoformat(last_notified)).total_seconds() / 3600.0
            if since < args.repeat_hours:
                print(f"already notified {since:.1f}h ago (repeat every {args.repeat_hours}h) — silent")
                return 0
        except ValueError:
            pass

    refused = last_line_matching(os.path.join(app, "memories", "directive-audit.log"), "write-refused")
    blocked = last_line_matching(os.path.join(app, "memories", "directive-promotion-audit.log"), "BLOCKED")

    lines = [
        f"⏳ Human directive has been PENDING for {age_txt}.",
        "",
        "The company cannot clear this by itself — the Completion clause needs market "
        "evidence or an explicit terminal decision.",
    ]
    if refused:
        lines += ["", f"Last write-refusal: {refused[:300]}"]
    if blocked:
        lines += ["", f"Last analyst promotion block: {blocked[:300]}"]
    lines += [
        "",
        "To replace it deliberately: AC_ALLOW_PENDING=1 apply-directive.sh <file>",
        "To close it: directive_writer.py status (PENDING->DONE) with a receipt.",
    ]
    msg = "\n".join(lines)

    if args.dry_run:
        print("--- would notify ---")
        print(msg)
        return 0

    if os.path.exists(notify_sh):
        try:
            subprocess.run(["bash", notify_sh, msg], capture_output=True, timeout=25)
        except Exception:  # noqa: BLE001 — a failed notification must not fail the watcher
            pass
    else:
        print("telegram-notify.sh absent — printed only", file=sys.stderr)

    state["last_notified_iso"] = now.isoformat()
    state["age_hours_at_notify"] = round(age_h, 1)
    try:
        tmp = state_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(state, fh)
        os.replace(tmp, state_path)
    except OSError as exc:
        print(f"could not persist state: {exc}", file=sys.stderr)
    print("notified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
