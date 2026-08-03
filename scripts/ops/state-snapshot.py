#!/usr/bin/env python3
"""One-call cycle state snapshot — collapses the per-cycle probe fan-out into a single turn.

WHY THIS EXISTS (2026-08-03 bloat audit). Cycles #18–#25 ran 60–110 turns and every one
of them was flagged CHATTY/BLOATED. A large share of those turns was the same opening
ritual, performed as 10–20 SEPARATE tool calls: read the directive status, grep the OPREQ
ledger, query the Registry Bridge, query the EKAP Bridge, run send-gate --report, run
reply-watch. Each tool round-trip re-bills the entire ~180K-token context (~$0.055/turn
at sonnet cache-read rates), so the ritual alone cost $0.50–$1.00 per cycle before any
real work started. This script answers ALL of it in ONE call, and adds a DELTA line
against the previous snapshot so an unchanged world can be dismissed in one glance.

WHAT IT PRINTS (compact, grep-friendly):
  directive:  Status + sha16 of memories/human-directive.md. The sha is for CHANGE
              DETECTION only — when the directive changed (or you have no record of its
              content in consensus), you still read the file itself; it stays canonical.
  opreq:      count + ids of blocks in memories/operator-requests.md with `- Status: OPEN`.
  bridges:    PENDING row counts in the Registry Bridge and EKAP Bridge tables.
  sends:      send-gate.py --report verbatim (caps and counters).
  replies:    reply-watch.py --dry-run summary tail (dry-run: never touches its state).
  DELTA:      none | changed=<fields> versus logs/state-snapshot-last.json.

DELTA semantics: "none" means none of the above moved since the previous snapshot — do
not re-probe any of it, and do not re-verify past cycles' work through these surfaces.
It does NOT mean "nothing to do": the directive's standing orders still apply.

Advisory + read-only toward the world: never writes to Airtable, never edits memories/.
Its only write is its own state file under logs/. Exit 0 always (a state probe must not
kill the calling cycle); failures are printed inline as ERROR so they are visible, and an
errored field never participates in DELTA (it can neither hide a change nor invent one).

  state-snapshot.py [--app /app] [--skip-network]   # --skip-network: tests/offline
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

BASE = "appPLc31jSlgulX3D"
T_REGISTRY_BRIDGE = "tblREW6MtTMTP5h5N"
T_EKAP_BRIDGE = "tblrQfg4nS3htetcE"
STATE = "logs/state-snapshot-last.json"

STATUS_RE = re.compile(r"^## Status\s*\n(\S+)\s*$", re.MULTILINE)
OPREQ_HEAD_RE = re.compile(r"^## (OPREQ-[A-Za-z0-9_-]+)\s*$", re.MULTILINE)
OPREQ_OPEN_RE = re.compile(r"^- Status:\s*OPEN\b", re.MULTILINE)


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


def directive_state(app: str) -> tuple[str, str]:
    path = os.path.join(app, "memories", "human-directive.md")
    try:
        raw = open(path, "rb").read()
    except OSError as e:
        return ("ERROR", f"unreadable: {e}")
    sha16 = hashlib.sha256(raw).hexdigest()[:16]
    m = STATUS_RE.search(raw.decode("utf-8", errors="replace"))
    return (m.group(1) if m else "NO-STATUS-SECTION", sha16)


def opreq_open(app: str) -> list[str] | None:
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


def bridge_pending(table: str, key: str) -> int | str:
    """PENDING count via pageSize=1 pages carrying record ids only — same narrow-read
    discipline as airtable-read.py, without a subprocess per table."""
    count, offset = 0, None
    while True:
        params = {
            "filterByFormula": "{status}='PENDING'",
            "fields[]": "request_id",
            "pageSize": "100",
        }
        if offset:
            params["offset"] = offset
        url = f"https://api.airtable.com/v0/{BASE}/{table}?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.load(r)
        except Exception as e:  # noqa: BLE001 — any transport/auth failure prints, never raises
            return f"ERROR {type(e).__name__}: {e}"
        count += len(data.get("records", []))
        offset = data.get("offset")
        if not offset:
            return count


def run_tool(app: str, rel: str, extra: list[str]) -> str:
    try:
        p = subprocess.run(
            [sys.executable, os.path.join(app, rel), "--app", app] + extra,
            capture_output=True, text=True, timeout=90,
        )
        out = (p.stdout or "").strip() or (p.stderr or "").strip()
        return out if out else f"ERROR rc={p.returncode} no output"
    except Exception as e:  # noqa: BLE001
        return f"ERROR {type(e).__name__}: {e}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", default="/app")
    ap.add_argument("--skip-network", action="store_true",
                    help="local files only (tests/offline) — network fields print SKIPPED")
    args = ap.parse_args()
    app = os.path.abspath(args.app)

    d_status, d_sha = directive_state(app)
    opreqs = opreq_open(app)

    if args.skip_network:
        reg = ekap = "SKIPPED"
        sends = replies = "SKIPPED"
    else:
        key = api_key(app)
        if key:
            reg = bridge_pending(T_REGISTRY_BRIDGE, key)
            ekap = bridge_pending(T_EKAP_BRIDGE, key)
        else:
            reg = ekap = "ERROR no AIRTABLE_API_KEY"
        sends = run_tool(app, "scripts/ops/send-gate.py", ["--report"])
        # --dry-run so this observation never consumes reply-watch's own once-per-outcome state.
        rw = run_tool(app, "scripts/ops/reply-watch.py", ["--dry-run"])
        replies = " | ".join(rw.splitlines()[-2:]) if rw else "ERROR empty"

    print("=== STATE SNAPSHOT (one call — do NOT re-probe these individually) ===")
    print(f"directive: status={d_status} sha16={d_sha}")
    if opreqs is None:
        print("opreq: ERROR ledger unreadable")
    else:
        print(f"opreq: open={len(opreqs)}" + (f" ids={','.join(opreqs)}" if opreqs else ""))
    print(f"bridges: registry_pending={reg} ekap_pending={ekap}")
    print(f"sends: {' | '.join(str(sends).splitlines())}")
    print(f"replies: {replies}")

    # DELTA — errored/skipped fields are excluded from comparison on BOTH sides, so a
    # transient Airtable failure neither reports a phantom change nor masks a real one.
    current = {
        "directive_status": d_status,
        "directive_sha16": d_sha,
        "opreq_open": sorted(opreqs) if opreqs is not None else None,
        "registry_pending": reg if isinstance(reg, int) else None,
        "ekap_pending": ekap if isinstance(ekap, int) else None,
        "sends": str(sends) if "ERROR" not in str(sends) and sends != "SKIPPED" else None,
        "replies": replies if "ERROR" not in str(replies) and replies != "SKIPPED" else None,
    }
    state_path = os.path.join(app, STATE)
    prev = {}
    try:
        prev = json.load(open(state_path, encoding="utf-8"))
    except (OSError, ValueError):
        pass
    changed = [
        k for k, v in current.items()
        if v is not None and prev.get(k) is not None and prev.get(k) != v
    ]
    if not prev:
        print("DELTA: first snapshot — no previous state to compare")
    elif changed:
        print(f"DELTA: changed={','.join(changed)}")
    else:
        print(f"DELTA: none — nothing above moved since {prev.get('_ts', 'last snapshot')}")
    current["_ts"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        os.makedirs(os.path.dirname(state_path), exist_ok=True)
        tmp = state_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(current, f)
        os.replace(tmp, state_path)
    except OSError as e:
        print(f"DELTA-STATE: ERROR could not persist ({e}) — next DELTA will compare against stale state")
    return 0


if __name__ == "__main__":
    sys.exit(main())
