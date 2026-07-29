#!/usr/bin/env python3
"""Which rules live ONLY in a directive?

The directive slot is overwritten by the next write, so any rule stated only there
is one write away from gone. This walks every directive body we still have (the
ops-repo files plus the live one) and asks, for each rule-shaped line, whether a
distinctive phrase from it survives in a standing file.

Deliberately noisy: it reports candidates for a human to judge, it does not decide.
A false positive costs a glance; a false negative is the thing that already happened.
"""
import re, subprocess, sys
from pathlib import Path

REPO = Path("/Users/akekilli/projects/autocompany")
OPS = Path("/Users/akekilli/projects/autocompany-deploy/directives")
standing = "\n".join((REPO / f).read_text(encoding="utf-8")
                     for f in ("PROMPT.md", "CLAUDE.md", "PROJECT_EVALUATION_FRAMEWORK.md"))
standing_l = standing.lower()

# Live directive from the container.
_live = subprocess.run(
    ["ssh", "powerupp-ts",
     "docker exec $(docker ps --format '{{.Names}}' | grep z12a992 | head -1) "
     "sh -lc 'cat /app/memories/human-directive.md'"],
    capture_output=True, text=True)
# A failed ssh used to leave `live` empty, and an empty live directive is
# indistinguishable from a skipped one — partial coverage reported as complete.
# Coverage you could not measure is UNKNOWN, never zero.
if _live.returncode != 0 or not _live.stdout.strip():
    print("SCAN FAILED / COVERAGE UNKNOWN — could not read the live directive "
          f"(rc={_live.returncode}): {(_live.stderr or '').strip()[:160]}", file=sys.stderr)
    sys.exit(3)
live = _live.stdout

# A line is rule-shaped if it asserts permanence or prohibition.
RULE = re.compile(
    r"\b(never|always|must not|must |may not|do not|don't|forbidden|hard stop|"
    r"non-negotiable|standing|unchanged|from now on|going forward|is fixed)\b", re.I)
STOP = re.compile(r"^\s*(#|<!--|\|)")

# Words too common to identify a rule by.
COMMON = set("""the a an and or of to in is are be it that this for with as on at by not no
never always must may do does not don't from now going forward standing unchanged rule rules
you your we our they their any all one two if then than when while which who what where
company operator directive cycle prompt file line read write set use used using""".split())


def key_phrases(line):
    """Distinctive tokens: long, not common, not pure punctuation."""
    toks = re.findall(r"[A-Za-zÇĞİÖŞÜçğıöşü0-9./_-]{4,}", line)
    return [t for t in toks if t.lower() not in COMMON and not t.isdigit()][:14]


def covered(line):
    """Token overlap is a SCREEN, not a verdict.

    It is trusted only in the negative direction: a low score means "a human must
    look at this". A high score means "probably fine", never "certified covered" —
    a rule whose words are individually common in standing text (WTP, EKAP, G1)
    can score high while the rule itself is absent. Never report a clean run as
    proof that nothing is missing.
    """
    ph = key_phrases(line)
    if not ph:
        return True, 0.0
    hits = sum(1 for t in ph if t.lower() in standing_l)
    return (hits / len(ph)) >= 0.6, hits / len(ph)


CANARY = REPO / "tests" / "fixtures" / "intentionally-uncovered-standing-rule.md"
CANARY_MARK = "zibberflux"

sources = [(p.name, p.read_text(encoding="utf-8")) for p in sorted(OPS.glob("*.md"))]
if not CANARY.exists():
    print(f"INVALID SCAN — canary fixture missing: {CANARY}", file=sys.stderr)
    sys.exit(3)
sources.append((CANARY.name, CANARY.read_text(encoding="utf-8")))
if live.strip():
    sources.append(("LIVE human-directive.md", live))

seen, findings = set(), []
for name, text in sources:
    for raw in text.splitlines():
        line = raw.strip()
        if len(line) < 40 or STOP.match(raw) or not RULE.search(line):
            continue
        norm = re.sub(r"\W+", " ", line.lower()).strip()
        if norm in seen:
            continue
        seen.add(norm)
        ok, ratio = covered(line)
        if not ok:
            findings.append((ratio, name, line))

findings.sort()
if not any(CANARY_MARK in line for _, _, line in findings):
    print("INVALID SCAN — the canary rule was NOT flagged. The token heuristic has "
          "gone blind; treat this run as no coverage information at all, not as a "
          "clean result.", file=sys.stderr)
    sys.exit(3)

print(f"scanned {len(sources)} directive bodies, {len(seen)} distinct rule-shaped lines")
print("canary: FLAGGED (heuristic still discriminating)")
print(f"NOT clearly covered by PROMPT.md / CLAUDE.md / framework: {len(findings)}\n")
for ratio, name, line in findings[:40]:
    print(f"[{ratio:.0%} covered] {name}")
    print(f"   {line[:190]}\n")
