#!/usr/bin/env python3
"""One-call cycle state snapshot — collapses the per-cycle probe fan-out into a single turn.

WHY THIS EXISTS (2026-08-03 bloat audit). Cycles #18–#25 ran 60–110 turns and every one
of them was flagged CHATTY/BLOATED; a large share was the same opening ritual performed
as 10–20 separate tool calls. This script answers ALL of it in ONE call, and adds a DELTA
line against the previous snapshot so an unchanged world can be dismissed in one glance.

2026-08-24 (Wowcar re-charter): the tender-era fields (bridge queues, send-gate counters,
reply outcomes) are retired with the Tender Track — their tools are no longer run per
cycle. The watched set is now fully LOCAL (no network), and includes the program-auditor
report hash (implements the operator-authorized OPREQ-INFRA-ANALYST-ROUTING-001 Option B:
analyst findings become DELTA-visible), the Wowcar source-set hash (the operator dropping
a new/updated source document wakes the loop), and the operator-decisions hash (a cockpit
panel answer becomes DELTA-visible the moment it lands).

WHAT IT PRINTS (compact, grep-friendly):
  directive:  Status + sha16 of memories/human-directive.md. The sha is for CHANGE
              DETECTION only — when it changed, you still read the file; it stays canonical.
  opreq:      count + ids of blocks in memories/operator-requests.md with `- Status: OPEN`.
  auditor:    sha16 of memories/analysis-directive.md (the independent program-auditor
              report) or ABSENT.
  wowcar:     sha16 over the sorted per-file sha256 set of projects/wowcar/* (source docs).
  decisions:  sha16 of memories/operator-decisions.md or ABSENT.
  DELTA:      none | changed=<fields> versus logs/state-snapshot-last.json.

DELTA semantics: "none" means none of the above moved since the previous snapshot — do
not re-probe any of it, and do not re-verify past cycles' work through these surfaces.
It does NOT mean "nothing to do": the directive's standing orders still apply.

Advisory + read-only toward the world: its only write is its own state file under logs/.
Exit 0 always (a state probe must not kill the calling cycle); failures are printed
inline as ERROR and an errored field never participates in DELTA.

  state-snapshot.py [--app /app] [--skip-network]   # --skip-network kept for interface
                                                    # compat; all fields are local now.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timezone

STATE = "logs/state-snapshot-last.json"

STATUS_RE = re.compile(r"^## Status\s*\n(\S+)\s*$", re.MULTILINE)
OPREQ_HEAD_RE = re.compile(r"^## (OPREQ-[A-Za-z0-9_-]+)\s*$", re.MULTILINE)
OPREQ_OPEN_RE = re.compile(r"^- Status:\s*OPEN\b", re.MULTILINE)


def file_sha16(path: str) -> str | None:
    """sha256[:16] of a file, None on unreadable, 'ABSENT' on missing."""
    if not os.path.exists(path):
        return "ABSENT"
    try:
        return hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]
    except OSError:
        return None


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


def wowcar_sources(app: str) -> str | None:
    """sha16 over the sorted (name, sha256) set of the Wowcar source documents.
    A new or changed file under projects/wowcar/ changes this hash → DELTA fires."""
    root = os.path.join(app, "projects", "wowcar")
    if not os.path.isdir(root):
        return "ABSENT"
    entries = []
    try:
        for name in sorted(os.listdir(root)):
            p = os.path.join(root, name)
            if os.path.isfile(p):
                entries.append(name + ":" + hashlib.sha256(open(p, "rb").read()).hexdigest())
    except OSError:
        return None
    return hashlib.sha256("\n".join(entries).encode()).hexdigest()[:16]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", default="/app")
    ap.add_argument("--skip-network", action="store_true",
                    help="deprecated no-op: every field is local since 2026-08-24")
    args = ap.parse_args()
    app = os.path.abspath(args.app)

    d_status, d_sha = directive_state(app)
    opreqs = opreq_open(app)
    auditor = file_sha16(os.path.join(app, "memories", "analysis-directive.md"))
    wowcar = wowcar_sources(app)
    decisions = file_sha16(os.path.join(app, "memories", "operator-decisions.md"))

    print("=== STATE SNAPSHOT (one call — do NOT re-probe these individually) ===")
    print(f"directive: status={d_status} sha16={d_sha}")
    if opreqs is None:
        print("opreq: ERROR ledger unreadable")
    else:
        print(f"opreq: open={len(opreqs)}" + (f" ids={','.join(opreqs)}" if opreqs else ""))
    print(f"auditor: {auditor if auditor else 'ERROR unreadable'}")
    print(f"wowcar: {wowcar if wowcar else 'ERROR unreadable'}")
    print(f"decisions: {decisions if decisions else 'ERROR unreadable'}")

    # DELTA — errored fields (None) are excluded from comparison on BOTH sides, so a
    # transient read failure neither reports a phantom change nor masks a real one.
    current = {
        "directive_status": d_status if d_status != "ERROR" else None,
        "directive_sha16": d_sha if d_status != "ERROR" else None,
        "opreq_open": sorted(opreqs) if opreqs is not None else None,
        "auditor_hash": auditor,
        "wowcar_sources": wowcar,
        "operator_decisions": decisions,
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
    main()
