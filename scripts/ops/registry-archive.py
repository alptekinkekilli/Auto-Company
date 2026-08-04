#!/usr/bin/env python3
"""Deterministic, fail-closed archival for memories/candidate-registry.md.

WHY (2026-08-03). The registry is 359KB/4,668 lines and ~90% of it is append-only
history: 190 dated maintenance notes prepended above the buckets, and the frozen
Cycle-106..302 discovery-scan sections below them (dead since Discovery went OFF on
2026-07-28). The live decision core is ~450 lines. The size bill lands on the
analyst (reads the whole file into an Opus prompt daily) and the cockpit panel.

WHAT IT MOVES — nothing else:
  1. Top-region maintenance notes: paragraphs before the first `## ` heading that
     start with `**`, contain ` note (` and a parseable date older than
     --note-age-days (default 14). Undated/odd bold paragraphs stay.
  2. Frozen history sections: `## PART A — ...` / `## Cycle N — ...` sections lying
     AFTER the protected live region, whose newest embedded date is older than
     --section-age-days (default 3). A section with no date at all stays.

Moves are VERBATIM into memories/registry-archive/<YYYY-MM>.md (bucketed by content
date), replaced in the live file by one `> [archived ...]` pointer line per batch.

INVARIANTS (any failure → nothing is written, exit 2):
  - PROTECTED REGION BYTE-IDENTICAL: from the `## Selected` heading through the end
    of the `## Exhausted patterns / lessons` section. This is a superset of
    merge_registry.py's live span, so the analyst's per-run id accounting cannot
    see this tool's work inside its span.
  - ANCHOR UNIQUENESS: exactly one `## Selected` and one `## Exhausted patterns /
    lessons` heading before AND after (merge_registry hard-fails otherwise).
  - RECONSTRUCTION: original == remaining-with-pointers-stripped re-interleaved
    with the archived chunks, verified by sha256 in memory BEFORE any write.
  - CAS: the live file's mtime must not change between read and write.
Crash-safety: archive files are written first and appends are content-deduplicated,
so a rerun after any partial failure converges instead of duplicating or losing.

Modes: default = dry-run plan. --apply = execute. --check = size advisory for the
loop's return moment (prints one line above --threshold-kb, else nothing; exit 0).
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import os
import re
import shutil
import sys

NOTE_RE = re.compile(r"^\*\*[^\n]{0,160}? note \((\d{4}-\d{2}-\d{2})", re.IGNORECASE)
FROZEN_HEAD_RE = re.compile(r"^## (?:PART A — |Cycle \d+ — )")
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
SEL_RE = re.compile(r"(?m)^## Selected[ \t]*$")
EXH_RE = re.compile(r"(?m)^## Exhausted patterns / lessons[ \t]*$")
POINTER_PREFIX = "> [archived "


def die(msg: str) -> "NoReturn":  # noqa: F821
    print(f"BLOCKED: {msg} (nothing was written)", file=sys.stderr)
    sys.exit(2)


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def heading_line_starts(text: str) -> list[int]:
    return [m.start() for m in re.finditer(r"(?m)^## ", text)]


def protected_span(text: str) -> tuple[int, int]:
    """[start, end) of the region this tool must never alter: `## Selected` through
    the END of the `## Exhausted patterns / lessons` section."""
    sels, exhs = SEL_RE.findall(text), EXH_RE.findall(text)
    if len(sels) != 1 or len(exhs) != 1:
        die(f"anchor headings not unique (Selected x{len(sels)}, Exhausted x{len(exhs)})")
    start = SEL_RE.search(text).start()
    exh_start = EXH_RE.search(text).start()
    if exh_start < start:
        die("'## Exhausted patterns / lessons' precedes '## Selected'")
    nxt = [p for p in heading_line_starts(text) if p > exh_start]
    end = nxt[0] if nxt else len(text)
    return start, end


def plan_note_chunks(text: str, first_heading: int, cutoff: dt.date) -> list[tuple[int, int, dt.date]]:
    """Archivable top-region note paragraphs as (start, end, date). `end` extends
    through the blank lines that follow, so the remaining text stays well-formed."""
    chunks = []
    pos = text.find("\n") + 1  # skip the H1 line
    region = text[pos:first_heading]
    for m in re.finditer(r"(?ms)^(?=\*\*)(.*?)(?=\n\s*\n|\Z)", region):
        para = m.group(1)
        nm = NOTE_RE.match(para)
        if not nm:
            continue
        try:
            d = dt.date.fromisoformat(nm.group(1))
        except ValueError:
            continue
        if d >= cutoff:
            continue
        a = pos + m.start()
        b = pos + m.end()
        while b < first_heading and text[b] in "\n \t":
            b += 1
        chunks.append((a, b, d))
    return chunks


def plan_section_chunks(text: str, prot: tuple[int, int], cutoff: dt.date,
                        undated_month: dt.date | None) -> tuple[list[tuple[int, int, dt.date]], int]:
    """Archivable frozen sections as (start, end, max_embedded_date); also returns
    how many candidate sections were SKIPPED for having no parseable date. When
    --allow-undated-month is given, dateless frozen sections are archived into that
    month instead of skipped (explicit operator statement of when they were written
    — e.g. the Cycle 106-131 'PART A' scans all date from the 2026-07-24 rewrite)."""
    heads = heading_line_starts(text)
    chunks, undated = [], 0
    for i, h in enumerate(heads):
        line_end = text.find("\n", h)
        line = text[h:line_end if line_end != -1 else len(text)]
        if not FROZEN_HEAD_RE.match(line):
            continue
        end = heads[i + 1] if i + 1 < len(heads) else len(text)
        if h < prot[1] and end > prot[0]:  # intersects protected region: never touch
            continue
        dates = []
        for dm in DATE_RE.finditer(text[h:end]):
            try:
                dates.append(dt.date.fromisoformat(dm.group(1)))
            except ValueError:
                pass
        if not dates:
            if undated_month is not None:
                chunks.append((h, end, undated_month))
            else:
                undated += 1
            continue
        if max(dates) >= cutoff:
            continue
        chunks.append((h, end, max(dates)))
    return chunks, undated


def interleave(pieces: list[str], chunks: list[str]) -> str:
    out = []
    for i, p in enumerate(pieces):
        out.append(p)
        if i < len(chunks):
            out.append(chunks[i])
    return "".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", default="/app")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--check", action="store_true", help="size advisory only")
    ap.add_argument("--threshold-kb", type=int, default=250)
    ap.add_argument("--note-age-days", type=int, default=14)
    ap.add_argument("--section-age-days", type=int, default=3)
    ap.add_argument("--allow-undated-month", default=None, metavar="YYYY-MM",
                    help="archive dateless frozen sections into this month instead of skipping them")
    args = ap.parse_args()
    undated_month = None
    if args.allow_undated_month:
        try:
            undated_month = dt.date.fromisoformat(args.allow_undated_month + "-01")
        except ValueError:
            die(f"--allow-undated-month must be YYYY-MM, got {args.allow_undated_month!r}")
    app = os.path.abspath(args.app)
    live_path = os.path.join(app, "memories", "candidate-registry.md")
    arch_dir = os.path.join(app, "memories", "registry-archive")

    if args.check:
        try:
            size = os.path.getsize(live_path)
        except OSError:
            return 0
        kb = (size + 1023) // 1024
        if size <= args.threshold_kb * 1024:
            return 0
        # Eligible-aware (2026-08-04): a size-only advisory fired every cycle for days
        # while the dry-run said "nothing to archive" — a non-actionable alarm teaches
        # everyone to scroll past it (the 41%-alarm lesson). Only advise when an
        # --apply run would actually move something; a purely-live file over the
        # threshold shrinks by itself as notes age past --note-age-days.
        eligible = None  # None = file did not parse -> size-only advisory (operator should look)
        try:
            text = open(live_path, encoding="utf-8").read()
            heads = heading_line_starts(text)
            prot = protected_span(text)
            today = dt.date.today()
            notes = plan_note_chunks(text, heads[0] if heads else len(text),
                                     today - dt.timedelta(days=args.note_age_days))
            sections, _und = plan_section_chunks(
                text, prot, today - dt.timedelta(days=args.section_age_days), None)
            eligible = (len(notes), len(sections))
        except SystemExit:
            # the invariant checks die() on a malformed file — a check must never
            # kill the loop's return moment, and an unparseable registry is exactly
            # when the operator SHOULD look.
            pass
        if eligible is None:
            print(
                f"[REGISTRY-SIZE] candidate-registry.md is {kb} KB (threshold {args.threshold_kb}) "
                f"and did NOT parse cleanly — operator should inspect it; archival plan unavailable"
            )
        elif eligible[0] or eligible[1]:
            print(
                f"[REGISTRY-SIZE] candidate-registry.md is {kb} KB (threshold {args.threshold_kb}) "
                f"with {eligible[0]} note(s) + {eligible[1]} section(s) archivable — operator-run "
                f"`python3 scripts/ops/registry-archive.py --app . --apply` rolls frozen "
                f"history into memories/registry-archive/ (advisory; this check never writes)"
            )
        return 0

    try:
        st0 = os.stat(live_path)
        original = open(live_path, encoding="utf-8").read()
    except OSError as e:
        die(f"cannot read live registry: {e}")

    today = dt.date.today()
    heads = heading_line_starts(original)
    if not heads:
        die("no '## ' headings found — not a registry-shaped file")
    prot = protected_span(original)
    notes = plan_note_chunks(original, heads[0], today - dt.timedelta(days=args.note_age_days))
    sections, undated = plan_section_chunks(
        original, prot, today - dt.timedelta(days=args.section_age_days), undated_month)
    all_chunks = sorted(notes + sections)
    if not all_chunks:
        print(f"nothing to archive (notes eligible: 0, sections eligible: 0, undated sections skipped: {undated})")
        return 0
    for (a1, b1, _), (a2, _b2, _2) in zip(all_chunks, all_chunks[1:]):
        if b1 > a2:
            die(f"internal error: overlapping chunks at {a1}-{b1} vs {a2}")
    for a, b, _ in all_chunks:
        if a < prot[1] and b > prot[0]:
            die(f"internal error: chunk {a}-{b} intersects protected region {prot}")

    # remaining = pieces between chunks, with one pointer per batch position
    run_ts = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    pieces, cursor = [], 0
    for a, b, _ in all_chunks:
        pieces.append(original[cursor:a])
        cursor = b
    pieces.append(original[cursor:])
    chunk_texts = [original[a:b] for a, b, _ in all_chunks]

    def month_of(i: int) -> str:
        return all_chunks[i][2].strftime("%Y-%m")

    n_notes = len(notes)
    pointer_note = (
        f"{POINTER_PREFIX}{run_ts}] {n_notes} maintenance note(s) older than "
        f"{args.note_age_days}d moved verbatim to memories/registry-archive/ "
        f"(read-only history — do not edit or re-inline)\n\n"
    ) if n_notes else ""
    pointer_sect = (
        f"{POINTER_PREFIX}{run_ts}] {len(sections)} frozen discovery/cycle section(s) moved "
        f"verbatim to memories/registry-archive/ (read-only history — do not edit or re-inline)\n\n"
    ) if sections else ""
    remaining_parts, note_ptr_done, sect_ptr_done = [], False, False
    for i, p in enumerate(pieces):
        remaining_parts.append(p)
        if i < len(all_chunks):
            is_note = all_chunks[i] in notes
            if is_note and not note_ptr_done:
                remaining_parts.append(pointer_note)
                note_ptr_done = True
            if not is_note and not sect_ptr_done:
                remaining_parts.append(pointer_sect)
                sect_ptr_done = True
    remaining = "".join(remaining_parts)

    # --- verify everything in memory before touching any file ---
    # Strip only THIS run's pointers: older runs' pointers are legitimate content
    # that lives inside `pieces`, and stripping them too would fail the check.
    stripped = re.sub(r"(?m)^" + re.escape(POINTER_PREFIX + run_ts) + r"[^\n]*\n\n?", "", remaining)
    if sha(interleave(pieces, chunk_texts)) != sha(original):
        die("reconstruction sha mismatch (pieces+chunks != original)")
    if sha(stripped) != sha("".join(pieces)):
        die("pointer-strip check failed — remaining does not reduce to pieces")
    if original[prot[0]:prot[1]] not in remaining:
        die("protected region is not byte-identical in the remaining text")
    protected_span(remaining)  # re-checks anchor uniqueness, dies if violated

    by_month: dict[str, list[str]] = {}
    for i, t in enumerate(chunk_texts):
        by_month.setdefault(month_of(i), []).append(t)

    saved = sum(len(t.encode("utf-8")) for t in chunk_texts)
    print(f"plan: {n_notes} note(s) + {len(sections)} section(s) -> "
          f"{', '.join(sorted(by_month))} | {saved} bytes out of {len(original.encode('utf-8'))} "
          f"({100 * saved // max(1, len(original.encode('utf-8')))}%) | undated sections skipped: {undated}")
    if not args.apply:
        for a, b, d in all_chunks:
            first = original[a:original.find('\n', a) if original.find('\n', a) != -1 else b][:90]
            print(f"  would move [{d}] {first!r}")
        print("dry-run only — pass --apply to execute")
        return 0

    # --- write: backup -> archive files (deduped append) -> live (CAS + atomic) ---
    bdir = os.path.join(app, "logs", "registry-archive-backups")
    os.makedirs(bdir, exist_ok=True)
    shutil.copy2(live_path, os.path.join(bdir, f"candidate-registry.md.{run_ts.replace(':', '')}"))
    backups = sorted(os.listdir(bdir))
    for old in backups[:-5]:
        os.unlink(os.path.join(bdir, old))

    os.makedirs(arch_dir, exist_ok=True)
    for month, texts in sorted(by_month.items()):
        apath = os.path.join(arch_dir, f"{month}.md")
        existing = open(apath, encoding="utf-8").read() if os.path.exists(apath) else (
            f"# Registry Archive — {month}\n\nMoved verbatim from memories/candidate-registry.md "
            f"by scripts/ops/registry-archive.py. Read-only history: never edit, never re-inline.\n"
        )
        fresh = [t for t in texts if t not in existing]
        if fresh:
            existing += f"\n<!-- archived {run_ts} -->\n\n" + "\n".join(fresh)
        tmp = apath + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(existing)
        os.replace(tmp, apath)
        readback = open(apath, encoding="utf-8").read()
        for t in texts:
            if t not in readback:
                die(f"archive readback missing a chunk in {apath}")

    if os.stat(live_path).st_mtime_ns != st0.st_mtime_ns:
        die("live registry changed on disk during the run (CAS) — archives hold copies, live untouched; rerun converges")
    tmp = live_path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(remaining)
    os.replace(tmp, live_path)
    if open(live_path, encoding="utf-8").read() != remaining:
        die("live readback mismatch after write — restore from logs/registry-archive-backups/")
    print(f"APPLIED: live {len(original.encode('utf-8'))} -> {len(remaining.encode('utf-8'))} bytes; "
          f"archived {saved} bytes into {len(by_month)} month file(s); backup kept; RECONSTRUCTION-OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
