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
live = subprocess.run(
    ["ssh", "powerupp-ts",
     "docker exec $(docker ps --format '{{.Names}}' | grep z12a992 | head -1) "
     "sh -lc 'cat /app/memories/human-directive.md'"],
    capture_output=True, text=True).stdout

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
    ph = key_phrases(line)
    if not ph:
        return True, 0.0
    hits = sum(1 for t in ph if t.lower() in standing_l)
    return (hits / len(ph)) >= 0.6, hits / len(ph)


sources = [(p.name, p.read_text(encoding="utf-8")) for p in sorted(OPS.glob("*.md"))]
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
print(f"scanned {len(sources)} directive bodies, {len(seen)} distinct rule-shaped lines")
print(f"NOT clearly covered by PROMPT.md / CLAUDE.md / framework: {len(findings)}\n")
for ratio, name, line in findings[:40]:
    print(f"[{ratio:.0%} covered] {name}")
    print(f"   {line[:190]}\n")
