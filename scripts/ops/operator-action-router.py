#!/usr/bin/env python3
"""One consolidated "what needs YOU" digest for the operator (Telegram firehose → single pane).

WHY THIS EXISTS. The operator receives ≥13 distinct message types from the company on
Telegram — action-required ones (🛑 LATCHED hold, ⚠️ directive PENDING, open OPREQ, …),
pure-info ones (🔄 Cycle OK+cost, ⬆️ escalation, 📊 turn-economy) and an external alarm
(Sentry crash-liveness). Inside that stream the operator cannot tell at a glance what is
actually ON THEM right now: the existing advisory watchers (directive-staleness,
registry-queue, reply-watch) each fire in isolation and none can say "you have N open
items / none". This watcher is the missing single pane. It is ADDITIVE — it never edits
or silences the other watchers; it sits on top and answers one question: what, if anything,
requires an operator action right now, and how to resolve each.

WHY IT READS COMPANY STATE, NOT TELEGRAM. A bot cannot read back the messages it SENT — the
Telegram getUpdates API returns only messages sent TO the bot, never the bot's own outbound.
The authoritative source of "what the operator was told" is therefore the live company state
that GENERATES those messages, which is also more truthful: an OPREQ the operator already
answered is no longer OPEN, so it stops appearing here on its own.

WHAT IT COVERS. Only signals that are locally, canonically, CURRENT-STATE truthful with no
network call — the three hard blockers:
  1. LATCHED / hold      — logs/LOOP_HOLD present (mechanical latch or operator cutover lock)
  2. Open OPREQ          — memories/operator-requests.md blocks with `- Status: OPEN`
  3. Directive PENDING   — memories/human-directive.md `## Status` == PENDING, past a floor age
The OPREQ/directive parse mirrors scripts/ops/state-snapshot.py (the same definition the
session brief prints as `opreq: open=N` / `directive: status=…`), kept independent here on
purpose — the established advisory-watcher pattern is each watcher reading its own source.

DELIBERATELY OUT OF SCOPE.
  - MERSİS registry-bridge queue and outreach replies: their current open set lives in
    Airtable, not in local state (logs/.registry-queue-state.json holds only a
    last-notified timestamp; logs/reply-watch-state.json holds only per-row dedup flags).
    Re-deriving them would need a network call and would duplicate registry-queue-watch.py /
    reply-watch.py, which ALREADY notify the operator additively with their own cooldowns.
    This router does not imitate them and does not claim to cover them.
  - Sentry crash-liveness (container dead): this router runs INSIDE the container at a
    post-cycle return moment; a dead container cannot run it. That alarm stays on the
    external Sentry→Worker→Telegram path. The router is not a liveness alarm.

DISCIPLINE (same as reply-watch.py / registry-queue-watch.py).
  - Fail-soft: every read is guarded; a missing/corrupt source SKIPS that item and never
    fails the cycle. Runs at an existing return moment, no timer of its own.
  - Advisory only: never writes to Airtable/Linear/the directive, never RESOLVES anything,
    never draws a conclusion ("not interested", "done") — it reports presence, ids and age.
  - Dedup/cadence: the OPEN SET's stable identity is hashed into
    logs/.operator-action-router-state.json. It speaks when the set is non-empty AND (the
    identity changed OR ROUTER_REPEAT_HOURS elapsed). Empty set → silent, and the state file
    is cleared so the next open item alerts immediately. Age is NOT part of the identity, so
    a still-PENDING directive does not re-alert every hour — only ROUTER_REPEAT_HOURS does.

Usage:
  operator-action-router.py [--app /app] [--dry-run]
                            [--repeat-hours 24] [--directive-min-hours 12]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

# --- source parsers (mirror scripts/ops/state-snapshot.py; kept independent by design) ---
STATUS_RE = re.compile(r"^##\s*Status\s*\n+(\S+)", re.MULTILINE)
OPREQ_HEAD_RE = re.compile(r"^## (OPREQ-[A-Za-z0-9_-]+)\s*$", re.MULTILINE)
OPREQ_OPEN_RE = re.compile(r"^- Status:\s*OPEN\b", re.MULTILINE)

STATE_REL = "logs/.operator-action-router-state.json"

# priority → lower first
P_HOLD, P_OPREQ, P_DIRECTIVE = 0, 1, 2


def _now() -> datetime:
    return datetime.now(timezone.utc)


def read_hold(app: str):
    """logs/LOOP_HOLD → a short reason string, or None. Robust to either the latch
    writer's `reason <text>` line or a free-form operator cutover note."""
    path = os.path.join(app, "logs", "LOOP_HOLD")
    try:
        raw = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return None
    reason = None
    for line in raw.splitlines():
        s = line.strip()
        if s.lower().startswith("reason "):
            reason = s[len("reason "):].strip()
            break
    if not reason:
        for line in raw.splitlines():
            s = line.strip()
            if s and not s.lower().startswith(("latched ", "cleared_by ")):
                reason = s
                break
    return (reason or "hold in place")[:200]


def read_opreqs(app: str):
    """Open OPREQ ids, or None if the ledger is unreadable (skip, do not invent)."""
    path = os.path.join(app, "memories", "operator-requests.md")
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return None
    heads = [(m.start(), m.group(1)) for m in OPREQ_HEAD_RE.finditer(text)]
    open_ids = []
    for i, (pos, rid) in enumerate(heads):
        end = heads[i + 1][0] if i + 1 < len(heads) else len(text)
        if OPREQ_OPEN_RE.search(text[pos:end]):
            open_ids.append(rid)
    return open_ids


def read_directive(app: str):
    """(status, age_hours, sha8) for memories/human-directive.md, or None if unreadable/absent.
    age_hours is derived from the file mtime (same signal directive-staleness-watch uses)."""
    path = os.path.join(app, "memories", "human-directive.md")
    try:
        raw = open(path, "rb").read()
        mtime = os.path.getmtime(path)
    except OSError:
        return None
    sha8 = hashlib.sha256(raw).hexdigest()[:8]
    m = STATUS_RE.search(raw.decode("utf-8", errors="replace"))
    status = m.group(1).strip().upper() if m else "NO-STATUS"
    age_h = max(0.0, (_now().timestamp() - mtime) / 3600.0)
    return (status, age_h, sha8)


def collect_items(app: str, directive_min_hours: float) -> list[dict]:
    """The current set of operator-actionable items. Each item:
        {key: <stable identity for hashing>, priority, line: <digest bullet>}
    Every source is independently fail-soft: a skip removes only that item."""
    items: list[dict] = []

    reason = read_hold(app)
    if reason:
        items.append({
            "key": f"hold:{reason}",
            "priority": P_HOLD,
            "line": f"[HOLD] LOOP_HOLD aktif — {reason}. "
                    f"→ /release ya da sebebi gider (host-side, operatör-only)",
        })

    opreqs = read_opreqs(app)
    if opreqs:
        ids = ", ".join(opreqs)
        items.append({
            "key": "opreq:" + ",".join(sorted(opreqs)),
            "priority": P_OPREQ,
            "line": f"[OPREQ] {len(opreqs)} açık: {ids}. "
                    f"→ Cockpit karar kartı / operator-decisions.md",
        })

    d = read_directive(app)
    if d:
        status, age_h, sha8 = d
        if status == "PENDING" and age_h >= directive_min_hours:
            items.append({
                "key": f"directive:{sha8}",  # age excluded on purpose (no hourly re-alert)
                "priority": P_DIRECTIVE,
                "line": f"[DIRECTIVE] PENDING {age_h:.0f}s (sha {sha8}). "
                        f"→ cevapla/kapat (cockpit veya directive slot)",
            })

    items.sort(key=lambda it: it["priority"])
    return items


def render(items: list[dict]) -> str:
    n = len(items)
    lines = [f"🧭 Sende {n} açık iş:"]
    for i, it in enumerate(items, 1):
        lines.append(f"{i}) {it['line']}")
    lines.append("Gerisi normal.")
    return "\n".join(lines)


def set_hash(items: list[dict]) -> str:
    return hashlib.sha256(
        "\n".join(sorted(it["key"] for it in items)).encode("utf-8")
    ).hexdigest()[:16]


def should_notify(items, state, now, repeat_hours):
    """(bool, reason). Speak when non-empty AND (identity changed OR repeat window elapsed)."""
    if not items:
        return (False, "empty")
    cur = set_hash(items)
    if state.get("hash") != cur:
        return (True, "changed")
    last = state.get("last_notified_iso")
    if last:
        try:
            since_h = (now - datetime.fromisoformat(last)).total_seconds() / 3600.0
            if since_h < repeat_hours:
                return (False, f"dedup ({since_h:.1f}h < {repeat_hours}h)")
        except ValueError:
            return (True, "bad-timestamp")
    return (True, "repeat-window")


def load_state(path: str) -> dict:
    try:
        return json.loads(open(path, encoding="utf-8").read())
    except (OSError, json.JSONDecodeError):
        return {}


def write_state(path: str, state: dict) -> None:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(state, fh, indent=1)
        os.replace(tmp, path)
    except OSError as exc:
        print(f"could not persist state: {exc}", file=sys.stderr)


def clear_state(path: str) -> None:
    try:
        os.remove(path)
    except OSError:
        pass


def notify(app: str, text: str) -> None:
    """Send via the shared telegram-notify.sh, sourcing the loop's runtime.env for the
    token/chat id (a fresh shell never sourced it). Mirrors reply-watch.py's notify()."""
    script = os.path.join(app, "scripts", "core", "telegram-notify.sh")
    if not os.path.exists(script):
        return
    env = dict(os.environ)
    try:
        for line in open(os.path.join(app, "logs", "runtime.env"),
                         encoding="utf-8", errors="replace"):
            if line.startswith(("TELEGRAM_BOT_TOKEN=", "TELEGRAM_CHAT_ID=")):
                k, v = line.split("=", 1)
                env[k] = v.strip().strip('"').strip("'")
    except OSError:
        pass
    subprocess.run(["bash", script], input=text, text=True, env=env,
                   capture_output=True, timeout=45, check=False)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", default="/app")
    ap.add_argument("--dry-run", action="store_true",
                    help="compute + print the decision, but never send and never write state")
    ap.add_argument("--repeat-hours", type=float,
                    default=float(os.environ.get("ROUTER_REPEAT_HOURS", "24")))
    ap.add_argument("--directive-min-hours", type=float,
                    default=float(os.environ.get("ROUTER_DIRECTIVE_MIN_HOURS", "12")))
    args = ap.parse_args()
    app = os.path.abspath(args.app)
    state_path = os.path.join(app, STATE_REL)

    try:
        items = collect_items(app, args.directive_min_hours)
    except Exception as exc:  # noqa: BLE001 — advisory: a bug here must never fail the cycle
        print(f"collect failed, staying silent: {exc}", file=sys.stderr)
        return 0

    if not items:
        if not args.dry_run:
            clear_state(state_path)
        print("no open operator items — silent")
        return 0

    state = load_state(state_path)
    do, why = should_notify(items, state, _now(), args.repeat_hours)
    text = render(items)

    if not do:
        print(f"suppressed ({why}) — {len(items)} item(s) still open")
        return 0

    if args.dry_run:
        print(f"WOULD-NOTIFY ({why}):")
        print(text)
        return 0

    notify(app, text)
    write_state(state_path, {"hash": set_hash(items),
                             "last_notified_iso": _now().isoformat()})
    print(f"NOTIFIED ({why}) — {len(items)} item(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
