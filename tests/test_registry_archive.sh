#!/bin/bash
# Tests for scripts/ops/registry-archive.py — the invariants are the product here:
# protected live span byte-identical, anchors unique, verbatim moves, idempotence.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RA="$HERE/../scripts/ops/registry-archive.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "  PASS: $1"; }
bad() { FAIL=$((FAIL+1)); echo "  FAIL: $1"; }
has() { if printf '%s' "$2" | grep -qF -- "$3"; then ok "$1"; else bad "$1 — missing [$3]"; fi; }

REG="$TMP/memories/candidate-registry.md"
mkdir -p "$TMP/memories" "$TMP/logs"

OLD_D=$(date -v-30d +%Y-%m-%d 2>/dev/null || date -d "30 days ago" +%Y-%m-%d)
OLD_M=$(printf '%s' "$OLD_D" | cut -c1-7)
NEW_D=$(date +%Y-%m-%d)

build_fixture() {
python3 - "$REG" "$OLD_D" "$NEW_D" <<'PY'
import sys
reg, old_d, new_d = sys.argv[1], sys.argv[2], sys.argv[3]
content = f"""# Candidate Registry (Lean)

**Cycle 2 maintenance note ({old_d}T10:00Z) — old, must move:** body of the old note with `215-TF-B` mention.

**CONDITIONAL GO / EXECUTION HOLD** undated bold paragraph — must STAY.

**Cycle 3 maintenance note ({new_d}T09:00Z) — fresh, must stay:** body of the fresh note.

## Selected

| rank | id | axis | verdict |
| 1 | 215-TF-B | tender readiness | **CONDITIONAL GO** |

## Pending shortlist

(none)

## Deferred / HOLD index

(none)

## Archived

- 176-R killed by APP-256

## Exhausted patterns / lessons

**Pattern 1** deadline-only demand is not demand.

## Cycle 7 — Embedded frozen section that sits INSIDE nothing protected ({old_d})

Frozen scan text A with a date {old_d} inside.

## PART A — Cycle 106 new discovery scan

Frozen scan text B, date {old_d} embedded.

## Cycle 9 — Undated section, must stay

No date here at all.

## Something else entirely

Not a frozen-pattern heading ({old_d}) — must stay.
"""
open(reg, "w").write(content)
PY
}

build_fixture
cp "$REG" "$TMP/original-copy.md"

echo "[1] dry-run: plans moves, writes nothing"
OUT=$(python3 "$RA" --app "$TMP")
has "plans the old note" "$OUT" "would move"
has "counts 1 note + 2 sections" "$OUT" "plan: 1 note(s) + 2 section(s)"
has "reports undated skip" "$OUT" "undated sections skipped: 1"
cmp -s "$REG" "$TMP/original-copy.md" && ok "live file untouched by dry-run" || bad "dry-run wrote"
[ ! -d "$TMP/memories/registry-archive" ] && ok "no archive dir from dry-run" || bad "dry-run created archive"

echo "[2] apply: moves are verbatim, protected span identical, anchors unique"
OUT=$(python3 "$RA" --app "$TMP" --apply)
has "applied with reconstruction check" "$OUT" "RECONSTRUCTION-OK"
ARCH="$TMP/memories/registry-archive/$OLD_M.md"
[ -f "$ARCH" ] && ok "archive month file exists" || bad "no archive file $ARCH"
grep -qF "old, must move" "$ARCH" && ok "old note archived verbatim" || bad "old note not in archive"
grep -qF "Frozen scan text A" "$ARCH" && ok "frozen section A archived" || bad "section A missing"
grep -qF "Frozen scan text B" "$ARCH" && ok "frozen section B archived" || bad "section B missing"
grep -qF "old, must move" "$REG" && bad "old note still in live" || ok "old note removed from live"
grep -qF "fresh, must stay" "$REG" && ok "fresh note stayed" || bad "fresh note lost"
grep -qF "CONDITIONAL GO / EXECUTION HOLD" "$REG" && ok "undated bold paragraph stayed" || bad "undated paragraph lost"
grep -qF "No date here at all" "$REG" && ok "undated section stayed" || bad "undated section lost"
grep -qF "Something else entirely" "$REG" && ok "non-frozen heading stayed" || bad "non-frozen section lost"
grep -qF "> [archived " "$REG" && ok "pointer lines present" || bad "no pointers"
[ "$(grep -c '^## Selected$' "$REG")" = 1 ] && ok "single Selected anchor" || bad "Selected anchor count wrong"
[ "$(grep -c '^## Exhausted patterns / lessons$' "$REG")" = 1 ] && ok "single Exhausted anchor" || bad "Exhausted anchor count wrong"
# Same semantics as the script's own invariant: the ORIGINAL protected span
# (Selected -> end of the Exhausted section) must appear byte-identical in the
# live file. A pointer line may legitimately sit right AT its end boundary.
rc=0
python3 - "$REG" "$TMP/original-copy.md" <<'PY' || rc=$?
import re, sys
live, orig = open(sys.argv[1]).read(), open(sys.argv[2]).read()
a = re.search(r"(?m)^## Selected[ \t]*$", orig).start()
e = re.search(r"(?m)^## Exhausted patterns / lessons[ \t]*$", orig).start()
nxt = [m.start() for m in re.finditer(r"(?m)^## ", orig) if m.start() > e]
span = orig[a:nxt[0] if nxt else len(orig)]
sys.exit(0 if span in live else 1)
PY
[ "$rc" -eq 0 ] && ok "protected span byte-identical" || bad "protected span changed"
ls "$TMP/logs/registry-archive-backups/" | grep -q candidate-registry && ok "backup written" || bad "no backup"

echo "[3] second apply: idempotent no-op"
OUT=$(python3 "$RA" --app "$TMP" --apply)
has "nothing left to archive" "$OUT" "nothing to archive"

echo "[4] --check: silent under threshold, advisory above"
OUT=$(python3 "$RA" --app "$TMP" --check)
[ -z "$OUT" ] && ok "silent under threshold" || bad "unexpected output: $OUT"
OUT=$(python3 "$RA" --app "$TMP" --check --threshold-kb 0)
has "advisory names the tool" "$OUT" "[REGISTRY-SIZE]"

echo "[5] frozen-pattern section INSIDE protected region is never touched"
build_fixture
python3 - "$REG" "$OLD_D" <<'PY'
import re, sys
reg, old_d = sys.argv[1], sys.argv[2]
t = open(reg).read()
# plant a frozen-looking section between Selected and Exhausted
t = t.replace("## Pending shortlist", f"## Cycle 4 — planted inside live span ({old_d})\n\nplanted body\n\n## Pending shortlist")
open(reg, "w").write(t)
PY
OUT=$(python3 "$RA" --app "$TMP" --apply)
grep -qF "planted body" "$REG" && ok "planted in-span section stayed in live" || bad "in-span section was moved"

echo
echo "registry-archive: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
