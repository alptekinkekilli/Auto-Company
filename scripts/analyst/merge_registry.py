#!/usr/bin/env python3
"""Deterministic PASS-2 registry merge (2026-07-27).

Built after the operator caught a real gap in the initial E2BIG fix: letting a
model reproduce the ENTIRE ~280KB registry (including ~180KB of append-only
historical cycle-scan logs the pass-2 prompt never even asked it to preserve)
risked silent, catastrophic data loss even on a "successful" run (rc=0, valid
JSON, plausible-looking output). This script never asks a model to reproduce
content it might drop — it mechanically isolates the one span of the file that
is genuinely "live decision state" (## Selected / ## Pending shortlist /
## Deferred / HOLD index / ## Archived) from everything else, and only a
model-proposed replacement for THAT span is ever considered.

Everything before "## Selected" and everything from "## Exhausted patterns /
lessons" onward is NEVER touched, no matter what the model returns — proven by
exact string splitting, not model instruction-following.

Exit code is always 0 (never breaks the caller). Stdout is exactly one of:
  MERGED: <summary>
  BLOCKED: <reason>
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

APP = Path(__file__).resolve().parents[2]
AUDIT_LOG = APP / "memories" / "registry-merge-audit.log"

# Section boundaries are matched as HEADINGS, not as exact surrounding-whitespace
# literals. The literals used to be "\n\n## Selected\n" / "\n\n## Exhausted patterns
# / lessons\n"; on 2026-07-29 a company cycle reformatted the registry and inserted a
# "---" rule before each heading, so both literals stopped matching and pass-2 died
# with "marker not found (START=False, END=False)". A cosmetic markdown edit must not
# be able to break the merge — the heading text is the contract, its decoration is not.
HEADING_LIVE_START = re.compile(r"(?m)^## Selected[ \t]*$")
HEADING_LIVE_END = re.compile(r"(?m)^## Exhausted patterns / lessons[ \t]*$")

# Candidate-ID token shapes actually observed in this registry: "176-R",
# "266-A", "192-REM", "216-C12-P", "215-TF-B", "Candidate #25".
ID_TOKEN_RE = re.compile(r"\b\d{2,4}-[A-Z][A-Za-z0-9-]*\b|Candidate #\d+")
# The optional word prefix is load-bearing: real IDs in this registry include
# `H-120-B1` and `Cycle 97-A`, which a bare numeric anchor silently drops.
ID_AT_START_RE = re.compile(
    r"^[`*_\s]*((?:[A-Za-z]{1,8}[- ])?(?:\d{2,4}-[A-Z][A-Za-z0-9-]*|Candidate #\d+))\b"
)

# ...but only where an IDENTIFIER can actually live. Scanning the whole span was
# assumed to be "stricter, therefore safe"; in practice it was neither, and it is
# what blocked the 2026-07-29 merge. It flagged four supposedly-missing candidates
# that were never candidates at all: `100-SKU` out of "≤100-SKU category inventory
# file", `500-RAW` out of "≤1,500-RAW catalog", `990-PF` out of "Free Candid/990-PF
# research" (a US tax form), and `177-R` out of a historical narrative sentence.
# Prose is the model's to rewrite; the moment it legitimately rephrases a sentence,
# an ID-shaped token vanishes and the merge is blocked forever.
#
# This NARROWS where identifiers are looked for, not what counts as one. Every
# candidate in this registry occupies either a table row (ID in the first or second
# cell, across the three column layouts in use) or a `- \`ID\` — ...` bullet in the
# HOLD index. A token that appears ONLY in prose or in an axis description is not a
# candidate, so nothing real loses protection.
def identifier_fields(text: str) -> list[str]:
    fields: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            fields.extend(cells[:2])
        elif s.startswith(("- ", "* ")):
            head = s[2:]
            fields.append(head.split("—", 1)[0])
    return fields


def audit(msg: str) -> None:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with AUDIT_LOG.open("a", encoding="utf-8") as f:
        f.write(f"[{stamp}] {msg}\n")


def blocked(reason: str) -> None:
    audit(f"BLOCKED: {reason}")
    print(f"BLOCKED: {reason}")
    sys.exit(0)


def extract_ids(text: str) -> set[str]:
    """Candidate IDs, anchored to the START of an identifier field.

    Anchoring is the second half of the narrowing. Restricting to the first two
    cells alone still leaked, because the axis cell IS cell 2 in the `| ID | axis |
    ... |` layout — so `≤100-SKU category inventory file` and `≤1,500-RAW catalog`
    were still read as candidates. A real ID owns its cell; a measurement buried in
    a sentence does not.
    """
    ids = set()
    for field in identifier_fields(text):
        m = ID_AT_START_RE.match(field)
        if m:
            ids.add(m.group(1))
    return ids


def extract_axes(text: str) -> list[str]:
    """Longest '×'-containing cell in each pipe-table row — robust to the
    three different table column layouts actually used across sections."""
    axes = []
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|") or set(s) <= {"|", "-", " ", ":"}:
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        candidates = [c for c in cells if "×" in c]
        if candidates:
            axes.append(max(candidates, key=len))
    return axes


def table_rows(text: str) -> list[list[str]]:
    """Data rows of every pipe table in `text`, as lists of stripped cells."""
    rows = []
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|") or set(s) <= {"|", "-", " ", ":"}:
            continue
        rows.append([c.strip() for c in s.strip("|").split("|")])
    return rows


def row_identity(cells: list[str]) -> tuple[str, str, str] | None:
    """(id, axis, verdict) for a candidate row, or None if it isn't one.

    The ID sits in cell 0 or cell 1 depending on the table layout (the Pending
    shortlist leads with a rank column); the axis is always the cell right after it.
    The verdict is the first bolded cell after the axis, falling back to the last.
    """
    for k in (0, 1):
        if k >= len(cells):
            break
        m = ID_AT_START_RE.match(cells[k])
        if not m or k + 1 >= len(cells):
            continue
        axis = cells[k + 1]
        rest = cells[k + 2 :]
        verdict = next((c for c in rest if "**" in c), rest[-1] if rest else "")
        return m.group(1), axis, verdict
    return None


def sections(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    current = ""
    for line in text.splitlines(keepends=True):
        if line.startswith("## "):
            current = line.strip()
            out.setdefault(current, "")
        elif current:
            out[current] += line
    return out


def active_candidates(live: str) -> dict[str, tuple[str, str]]:
    """The candidates whose IDENTITY an automated merge may not rewrite: anything in
    `## Selected`, plus rank 1 of `## Pending shortlist`. Returns {id: (axis, verdict)}.

    Deliberately table-only. Bullet entries in the HOLD index are research-stage and
    are not the live offer, so leaving them out keeps the guard narrow enough to stay
    useful — pass-2's whole job is reshaping those.
    """
    secs = sections(live)
    active: dict[str, tuple[str, str]] = {}
    for cells in table_rows(secs.get("## Selected", "")):
        ident = row_identity(cells)
        if ident:
            active[ident[0]] = (ident[1], ident[2])
    for cells in table_rows(secs.get("## Pending shortlist", "")):
        if cells and cells[0] == "1":
            ident = row_identity(cells)
            if ident:
                active[ident[0]] = (ident[1], ident[2])
            break
    return active


def normalize_axis(axis: str) -> str:
    return re.sub(r"\s+", " ", axis).strip().lower()


def resolve_span(value: str) -> str:
    """Dereference the file-reference shorthand pass-2 sometimes emits instead of
    inlining the span (2026-07-28: the model wrote a correct 105KB JSON payload to
    /tmp/registry-updated.json and replied only `{"registry_live_span":
    "@/tmp/registry-updated.json"}`, a 28-char path the <100-char guard rejected —
    fail-closed and correct, but the real content never reached the merge).

    This dereferences the pointer; it does NOT relax any check. Every invariant
    below (ID preservation, duplicate axis, prefix/suffix byte-identity,
    read-back) still runs on the resolved content exactly as if it had been
    inlined. Deliberately narrow: a single-line absolute path to an existing
    regular file. Anything else is returned untouched and hits the normal guards.
    """
    if not isinstance(value, str):
        return ""
    candidate = value.strip()
    if not candidate or "\n" in candidate or len(candidate) > 400:
        return value
    if candidate.startswith("@"):
        candidate = candidate[1:].strip()
    if not candidate.startswith("/"):
        return value
    ref = Path(candidate)
    if not ref.is_file():
        audit(f"span-ref: {candidate} is not a regular file — falling through to normal guards")
        return value
    try:
        content = ref.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        audit(f"span-ref: could not read {candidate}: {exc}")
        return value
    # The referenced file is usually the whole JSON payload, not the bare span.
    try:
        inner = json.loads(content)
        if isinstance(inner, dict) and isinstance(inner.get("registry_live_span"), str):
            content = inner["registry_live_span"]
    except Exception:
        pass  # not JSON — treat the file's contents as the span itself
    audit(f"span-ref: dereferenced {candidate} -> {len(content)} chars (invariants still enforced)")
    return content


def _rewind_over_separators(text: str, idx: int) -> int:
    """Walk `idx` (start of a heading line) back over the run of blank and `---`
    lines that immediately precedes it, so those decorations stay in the UNTOUCHED
    suffix rather than becoming trailing junk the model has to reproduce."""
    while idx > 0 and text[idx - 1] == "\n":
        line_start = text.rfind("\n", 0, idx - 1) + 1
        line = text[line_start : idx - 1].strip()
        if line == "" or (len(line) >= 3 and set(line) == {"-"}):
            idx = line_start
        else:
            break
    return idx


def split_registry(text: str) -> tuple[str, str, str]:
    """Split into (before, live, after) at the two section headings.

    `before` and `after` are returned as exact slices of `text` and are never
    modified — that byte-identity, not instruction-following, is what protects the
    ~180KB append-only historical journal in `after`.
    """
    starts = HEADING_LIVE_START.findall(text)
    ends = HEADING_LIVE_END.findall(text)
    if len(starts) != 1:
        raise ValueError(f"expected exactly one '## Selected' heading, found {len(starts)}")
    if len(ends) != 1:
        raise ValueError(
            f"expected exactly one '## Exhausted patterns / lessons' heading, found {len(ends)}"
        )

    m_start = HEADING_LIVE_START.search(text)
    m_end = HEADING_LIVE_END.search(text)
    i_start = m_start.start()
    i_end = _rewind_over_separators(text, m_end.start())
    if i_end <= i_start:
        raise ValueError("'## Exhausted patterns / lessons' precedes '## Selected'")

    return text[:i_start], text[i_start:i_end], text[i_end:]


def main() -> None:
    # Extraction mode. The orchestrator used to carry its OWN inline copy of the
    # splitting logic, so the boundary was defined in two places and the 2026-07-29
    # "---" reformat broke both. One definition now; the shell calls this.
    if len(sys.argv) == 3 and sys.argv[1] == "--extract-live-span":
        try:
            _before, live, _after = split_registry(
                Path(sys.argv[2]).read_text(encoding="utf-8")
            )
        except Exception as exc:
            print(f"{exc}", file=sys.stderr)
            sys.exit(1)
        sys.stdout.write(live)
        sys.exit(0)

    if len(sys.argv) != 4:
        blocked(
            "usage: merge_registry.py <registry.md path> "
            "<model-json-output path> <target registry.md path to write>"
        )
    registry_path = Path(sys.argv[1])
    model_output_path = Path(sys.argv[2])
    target_path = Path(sys.argv[3])

    if not registry_path.is_file():
        blocked(f"registry missing: {registry_path}")
    if not model_output_path.is_file() or model_output_path.stat().st_size == 0:
        blocked("model produced no output")

    original = registry_path.read_text(encoding="utf-8")
    try:
        before, old_live, after = split_registry(original)
    except ValueError as exc:
        blocked(f"could not isolate live span in current registry: {exc}")
    # Logged on every outcome from here on (operator's monitoring ask,
    # 2026-07-27): the untouched prefix/suffix are byte-identical by
    # construction — these hashes make that trivially checkable per run
    # without re-diffing, across BLOCKED and MERGED outcomes alike.
    before_hash = hashlib.sha256(before.encode()).hexdigest()
    after_hash = hashlib.sha256(after.encode()).hexdigest()

    raw = model_output_path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"```json\s*(\{.*?\})\s*```", raw, re.S) or re.search(r"(\{.*\})", raw, re.S)
    if not m:
        blocked("no json block in model output")
    try:
        payload = json.loads(m.group(1))
    except Exception as exc:
        blocked(f"bad json: {exc}")

    new_live = resolve_span(payload.get("registry_live_span", ""))
    if not new_live or len(new_live) < 100:
        blocked("model's registry_live_span missing or too short")
    if not new_live.startswith("\n## Selected") and "## Selected" not in new_live[:50]:
        blocked("model's registry_live_span does not start with ## Selected — refusing to guess")

    # --- invariant 1: no candidate silently disappears ---
    old_ids = extract_ids(old_live)
    new_ids = extract_ids(new_live)
    missing = old_ids - new_ids
    if missing:
        blocked(
            f"{len(missing)} candidate ID(s) present before but missing after: "
            + ", ".join(sorted(missing)[:20])
            + f" | prefix_hash={before_hash[:12]} suffix_hash={after_hash[:12]} (registry untouched)"
        )

    # --- invariant 2: no duplicate axis in the new live span ---
    new_axes = extract_axes(new_live)
    seen: dict[str, int] = {}
    dupes = []
    for axis in new_axes:
        key = normalize_axis(axis)
        seen[key] = seen.get(key, 0) + 1
        if seen[key] == 2:
            dupes.append(axis[:80])
    if dupes:
        blocked(
            f"{len(dupes)} duplicate axis row(s) in proposed registry: "
            + " | ".join(dupes[:5])
            + f" | prefix_hash={before_hash[:12]} suffix_hash={after_hash[:12]} (registry untouched)"
        )

    # --- invariant 3: the active candidate's IDENTITY is not the merge's to rewrite ---
    # Added 2026-07-29 after pass-2 autonomously redefined the live offer: it rewrote
    # 215-TF-B's buyer from "opted-in existing Turkish bidder" to one "already seeking
    # help with one self-identified live tender" and declared the company's actual
    # outreach segment NO-GO. The directive-promotion gate held, but nothing stopped the
    # registry write, and a later cycle then treated the rewritten row as settled state.
    # A verdict change (HOLD -> CONDITIONAL GO) is pass-2's job and stays allowed — it is
    # surfaced in the summary instead. Redefining WHO the buyer is and WHAT is delivered
    # is not, and needs the operator.
    old_active = active_candidates(old_live)
    new_rows = {}
    for cells in table_rows(new_live):
        ident = row_identity(cells)
        if ident:
            new_rows[ident[0]] = (ident[1], ident[2])

    verdict_changes = []
    for cid, (old_axis, old_verdict) in old_active.items():
        if cid not in new_rows:
            blocked(
                f"active candidate {cid} is no longer a table row in the proposed registry "
                f"| prefix_hash={before_hash[:12]} suffix_hash={after_hash[:12]} (registry untouched)"
            )
        new_axis, new_verdict = new_rows[cid]
        if normalize_axis(old_axis) != normalize_axis(new_axis):
            blocked(
                f"active candidate {cid}: axis rewritten, which needs the operator. "
                f"BEFORE: {old_axis[:160]!r} AFTER: {new_axis[:160]!r} "
                f"| prefix_hash={before_hash[:12]} suffix_hash={after_hash[:12]} (registry untouched)"
            )
        if normalize_axis(old_verdict) != normalize_axis(new_verdict):
            verdict_changes.append(f"{cid}: {old_verdict[:70]} -> {new_verdict[:70]}")

    # --- assemble, write, read back, verify ---
    # `before` ends with the newline that closes the line above the heading, and
    # `after` begins with the blank line that precedes the next heading's rule —
    # so the span must start exactly at "## Selected" and end with exactly one
    # newline. Do not pad either side; that is what keeps reassembly lossless.
    new_live = new_live.lstrip("\n").rstrip("\n") + "\n"
    new_full = before + new_live + after
    # before/after are byte-identical to the original by construction — only
    # new_live differs. Confirm that explicitly before writing anything.
    if before not in original or after not in original:
        blocked("internal error: before/after span mismatch — aborting, not writing")

    target_path.write_text(new_full, encoding="utf-8")
    readback = target_path.read_text(encoding="utf-8")
    if readback != new_full:
        target_path.write_text(original, encoding="utf-8")
        blocked("read-back verification failed — restored original, did not write")

    added = new_ids - old_ids
    old_lines, new_lines = len(old_live.splitlines()), len(new_live.splitlines())
    final_hash = hashlib.sha256(target_path.read_bytes()).hexdigest()
    audit(
        "MERGED: "
        f"old_live_lines={old_lines} new_live_lines={new_lines} "
        f"old_id_count={len(old_ids)} new_id_count={len(new_ids)} "
        f"ids_added={sorted(added)} ids_removed=[] "
        f"prefix_hash={before_hash[:12]} suffix_hash={after_hash[:12]} "
        f"active_verdict_changes={verdict_changes} "
        f"final_sha256={final_hash}"
    )
    # Verdict changes on the active candidate are allowed but must not be quiet — this
    # line lands in the cron log and the report header, where the operator sees it.
    notice = f" ACTIVE_VERDICT_CHANGED[{'; '.join(verdict_changes)}]" if verdict_changes else ""
    print(
        f"MERGED: old_live_lines={old_lines} new_live_lines={new_lines} "
        f"ids_preserved={len(old_ids)} ids_added={len(added)} "
        f"final_sha256={final_hash[:12]}...{notice}"
    )


if __name__ == "__main__":
    main()
