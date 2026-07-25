#!/usr/bin/env python3
"""Extract every screened axis WITH its body from the discovery scans.

The previous shell version used `awk '/^## Axis/,/^## Axis/'`, whose range opens and
closes on the same header line, so it emitted titles and dropped every kill reason —
and its counter only recognised `## Axis`, missing 19 axes written as `### Shape`,
`## A —`, `## Screen`, etc. It failed silently, which is how an "evidence pack" that
contained no evidence got shipped.

This version fails CLOSED: it asserts that every detected heading yields a non-empty
body and that the heading count matches the extracted-body count, and exits non-zero
with a diagnostic if not.
"""
import os, re, sys, glob

SCAN_GLOB = sys.argv[1] if len(sys.argv) > 1 else "/app/docs/research/cycle1*-*.md"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/tmp/kill-evidence-v2.md"

# Every heading form observed in the corpus, not just "## Axis".
AXIS_RE = re.compile(
    r"^#{2,4}\s*(?:"
    r"axis\s*[0-9A-Za-z]+|"
    r"shape\s*[0-9A-Za-z]*|"
    r"screen\s*[0-9A-Za-z]*|"
    r"candidate\s*[0-9A-Za-z]*|"
    r"[A-C]\s*[—–-]"
    r")\b",
    re.IGNORECASE,
)
# Section headings that end an axis body without being an axis themselves.
STOP_RE = re.compile(r"^#{2,4}\s*(overall|verdict|result|summary|dedup|conclusion)", re.IGNORECASE)

axes, problems = [], []
files = sorted(glob.glob(SCAN_GLOB))
for path in files:
    try:
        lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    except OSError as e:
        problems.append(f"unreadable {path}: {e}")
        continue
    idx = [i for i, l in enumerate(lines) if AXIS_RE.match(l)]
    for n, start in enumerate(idx):
        end = len(lines)
        for j in range(start + 1, len(lines)):
            if AXIS_RE.match(lines[j]) or STOP_RE.match(lines[j]):
                end = j
                break
        body = [l for l in lines[start + 1:end] if l.strip()]
        if not body:
            problems.append(f"EMPTY BODY: {os.path.basename(path)} :: {lines[start][:70]}")
        axes.append((os.path.basename(path), lines[start].strip(), body))

with open(OUT, "w", encoding="utf-8") as f:
    f.write("# Evidence pack v2 — every screened axis WITH its stated reasoning\n\n")
    f.write(f"Scans parsed: {len(files)} · axes extracted: {len(axes)}\n\n")
    cur = None
    for fname, head, body in axes:
        if fname != cur:
            f.write(f"\n## {fname}\n")
            cur = fname
        f.write(f"\n### {head}\n")
        for l in body:
            f.write(l + "\n")

print(f"scans={len(files)} axes={len(axes)} bodyless={sum(1 for _,_,b in axes if not b)}")
print(f"bytes={os.path.getsize(OUT)}")
if problems:
    print("PROBLEMS:")
    for p in problems[:20]:
        print("  " + p)
    sys.exit(2)   # fail closed
