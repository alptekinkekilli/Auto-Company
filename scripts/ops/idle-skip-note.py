#!/usr/bin/env python3
"""Record a model-free idle-skip in consensus.md as ONE line per UTC day.

Why this exists: the loop can now end an idle cycle without calling a model at all
(auto-loop.sh's IDLE-SKIP, operator-approved 2026-08-06). That is the whole saving —
but a cycle that leaves no record is indistinguishable from a cycle that never ran,
and the 2026-08-13 adjudication needs "checked, nothing moved" evidence, not silence.

One line per day, updated in place (count + end time), so a day of skips costs the
prompt ~150 bytes instead of one line per skip. The machine trail is separate and
append-only: logs/idle-skip.ndjson.

Writes atomically (tmp + rename) and never partially rewrites consensus: on any
error it leaves the file untouched and exits non-zero — the loop treats that as
best-effort and carries on.
"""
import argparse
import os
import re
import sys
import tempfile

MARKER = "<!-- idle-skip:%s -->"


def build_line(day, count, start, end):
    plural = "cycle" if count == 1 else "cycles"
    return (
        "- **Idle watch %s — %d %s skipped, zero model calls** (%s→%s UTC): the "
        "pre-run state snapshot reported `DELTA: none` each time, so the loop ended "
        "the cycle mechanically instead of paying a model to re-read an unchanged "
        "world. A full cycle ran earlier the same day. Machine trail: "
        "`logs/idle-skip.ndjson`. %s" % (day, count, plural, start, end, MARKER % day)
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--consensus", required=True)
    ap.add_argument("--day", required=True, help="UTC date, YYYY-MM-DD")
    ap.add_argument("--time", required=True, help="UTC time of this skip, HH:MM")
    args = ap.parse_args()

    try:
        with open(args.consensus, "r", encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        print("idle-skip-note: cannot read consensus: %s" % exc, file=sys.stderr)
        return 1

    marker = MARKER % args.day
    existing = None
    for line in text.splitlines():
        if marker in line:
            existing = line
            break

    if existing is None:
        count, start = 1, args.time
    else:
        m = re.search(r"—\s*(\d+)\s+cycles?\s+skipped", existing)
        count = (int(m.group(1)) if m else 1) + 1
        m = re.search(r"\((\d{2}:\d{2})→", existing)
        start = m.group(1) if m else args.time

    new_line = build_line(args.day, count, start, args.time)
    if existing is None:
        if text and not text.endswith("\n"):
            text += "\n"
        text += new_line + "\n"
    else:
        text = text.replace(existing, new_line, 1)

    d = os.path.dirname(os.path.abspath(args.consensus)) or "."
    try:
        fd, tmp = tempfile.mkstemp(dir=d, prefix=".idle-skip-", suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.replace(tmp, args.consensus)
    except OSError as exc:
        print("idle-skip-note: cannot write consensus: %s" % exc, file=sys.stderr)
        try:
            os.unlink(tmp)
        except (OSError, NameError, UnboundLocalError):
            pass
        return 1

    print("idle-skip-note: %s count=%d" % (args.day, count))
    return 0


if __name__ == "__main__":
    sys.exit(main())
