#!/usr/bin/env python3
"""Tests for scripts/ops/consensus-prune.py. Run: python3 tests/test_consensus_prune.py"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "ops" / "consensus-prune.py"
GUARD = REPO / "scripts" / "ops" / "ledger-guard.py"
_fail = []


def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        _fail.append(name)


def newapp():
    d = Path(tempfile.mkdtemp())
    (d / "memories").mkdir(); (d / "logs").mkdir(); (d / "docs/operations").mkdir(parents=True)
    return d


def consensus(d):
    return d / "memories/consensus.md"


def entry(n, size=1800):
    body = f"- **Cycle {n} — milestone {n} (ünicode: şğı).** Did things.\n"
    filler = "  continuation line with détail " + "x" * 40 + "\n"
    while len(body.encode()) < size:
        body += filler
    return body + "\n"


def doc(entries, extra_bullet=None, note=None):
    s = "# Auto Company Consensus\n\n## Last Updated\n2026-10-08\n\n## Company State\nok\n\n"
    s += "## What We Did This Cycle\n\n"
    if extra_bullet:
        s += extra_bullet
    for n in entries:
        s += entry(n)
    if note:
        s += note
    s += "## Key Decisions Made\n- keep\n\n## Next Action\n- go\n"
    return s


def run(d, cycle, env=None, dry=False):
    e = dict(os.environ)
    e["CONSENSUS_PRUNE_KEEP"] = "12"  # fixtures are built around 12; default is 8
    e.update(env or {})
    cmd = [sys.executable, str(SCRIPT), "--cycle", str(cycle), "--app", str(d)]
    if dry:
        cmd.append("--dry-run")
    p = subprocess.run(cmd, capture_output=True, text=True, env=e)
    return p.returncode, p.stdout


def guard(d, cycle):
    p = subprocess.run([sys.executable, str(GUARD), "--cycle", str(cycle), "--app", str(d)],
                       capture_output=True, text=True)
    return p.stdout


BIG = list(range(743, 703, -1))  # 40 entries newest-first, ~72 KB > 70000

# (a) big file -> keep 12 largest numbers, archive byte-exact, single note, invariants intact
d = newapp(); consensus(d).write_text(doc(BIG), encoding="utf-8")
before = consensus(d).read_bytes()
rc, out = run(d, 743)
after = consensus(d).read_text(encoding="utf-8")
nums = [int(m) for m in re.findall(r"(?m)^- \*\*Cycle (\d+)", after)]
check("(a) exit 0 + moved line", rc == 0 and "moved to docs/operations/consensus-archive-" in out)
check("(a) keeps 12 newest numbers", nums == BIG[:12])
arch = list((d / "docs/operations").glob("consensus-archive-*.md"))
check("(a) archive file created", len(arch) == 1)
atext = arch[0].read_text(encoding="utf-8")
gone = "".join(entry(n) for n in BIG[12:])
check("(a) archived entries byte-exact", gone in atext and "sha256:" in atext)
check("(a) exactly one archive note", after.count("_Archive note (cycle") == 1)
check("(a) required markers intact", all(m in after for m in ("# Auto Company Consensus", "## Next Action", "## Company State")))
check("(a) other sections untouched", "## Key Decisions Made\n- keep" in after and after.endswith("## Next Action\n- go\n"))
st = json.loads((d / "logs/consensus-prune.json").read_text())
check("(a) state has pre/post sha + post_metrics", st.get("pre_sha16") and st.get("post_sha16") and st.get("post_metrics", {}).get("sections"))
check("(a) size reduced below 70000", len(after.encode()) < 70000 < len(before))

# (f) second run -> no-op (below threshold); archive unchanged
asize = arch[0].stat().st_size
rc, out = run(d, 744)
check("(f) second run silent no-op", out.strip() == "" and arch[0].stat().st_size == asize)
# (f2) restore pre-prune copy and run again -> archive NOT duplicated (sha dedupe)
consensus(d).write_bytes(before)
rc, out = run(d, 745)
check("(f2) re-run after restore: moved again but archive block not duplicated",
      "moved" in out and arch[0].read_text(encoding="utf-8").count("sha256:") == 1)

# (b) below threshold -> no-op even with many entries
d = newapp(); consensus(d).write_text(doc(list(range(30, 0, -1))).replace("x" * 40, "x"), encoding="utf-8")
b0 = consensus(d).read_bytes(); rc, out = run(d, 1)
check("(b) below threshold: untouched + silent", consensus(d).read_bytes() == b0 and out.strip() == "")

# (c) unknown top-level bullet in section -> skip, untouched
d = newapp(); consensus(d).write_text(doc(BIG, extra_bullet="- Read something odd\n\n"), encoding="utf-8")
b0 = consensus(d).read_bytes(); rc, out = run(d, 1)
check("(c) unknown bullet: skipped + untouched", "skipped" in out and consensus(d).read_bytes() == b0)
# (c2) non-monotonic numbers -> skip
d = newapp(); consensus(d).write_text(doc([743, 700, 742] + BIG[3:]), encoding="utf-8")
b0 = consensus(d).read_bytes(); rc, out = run(d, 1)
check("(c2) non-monotonic: skipped + untouched", "skipped" in out and consensus(d).read_bytes() == b0)
# (c3) section header missing -> skip
d = newapp(); consensus(d).write_text(doc(BIG).replace("## What We Did This Cycle", "## Something Else"), encoding="utf-8")
b0 = consensus(d).read_bytes(); rc, out = run(d, 1)
check("(c3) no section: skipped + untouched", "skipped" in out and consensus(d).read_bytes() == b0)
# (c4) invalid UTF-8 -> skip
d = newapp(); consensus(d).write_bytes(doc(BIG).encode() + b"\xff\xfe bad")
b0 = consensus(d).read_bytes(); rc, out = run(d, 1)
check("(c4) invalid utf-8: skipped + untouched", "skipped" in out and consensus(d).read_bytes() == b0)

# (d) archive dir not writable -> consensus untouched
d = newapp(); consensus(d).write_text(doc(BIG), encoding="utf-8")
(d / "docs/operations").chmod(0o500)
b0 = consensus(d).read_bytes(); rc, out = run(d, 1)
(d / "docs/operations").chmod(0o700)
check("(d) archive unwritable: skipped + untouched", "skipped" in out and consensus(d).read_bytes() == b0)

# (e) kill switch
d = newapp(); consensus(d).write_text(doc(BIG), encoding="utf-8")
b0 = consensus(d).read_bytes(); rc, out = run(d, 1, env={"CONSENSUS_PRUNE_ENABLED": "0"})
check("(e) kill switch: silent + untouched", out.strip() == "" and consensus(d).read_bytes() == b0)

# (g) 3 consecutive skips above threshold -> alarm line
d = newapp(); consensus(d).write_text(doc(BIG, extra_bullet="- odd\n"), encoding="utf-8")
outs = [run(d, c)[1] for c in (1, 2, 3)]
check("(g) first two skips plain, third is alarm",
      "CONSENSUS-PRUNE —" not in outs[0] and "CONSENSUS-PRUNE —" not in outs[1] and "CONSENSUS-PRUNE —" in outs[2])

# (h) archive note must not match ledger-guard INCIDENT_RE
src = (REPO / "scripts/ops/ledger-guard.py").read_text(encoding="utf-8")
inc = re.search(r'INCIDENT_RE = re\.compile\(\s*r"([^"]+)"', src).group(1)
d = newapp(); consensus(d).write_text(doc(BIG), encoding="utf-8"); run(d, 743)
note = [l for l in consensus(d).read_text(encoding="utf-8").splitlines() if "_Archive note" in l][0]
check("(h) note does not match INCIDENT_RE", not re.search(inc, note, re.IGNORECASE))

# (i) dry-run writes nothing
d = newapp(); consensus(d).write_text(doc(BIG), encoding="utf-8")
b0 = consensus(d).read_bytes(); rc, out = run(d, 1, dry=True)
check("(i) dry-run: reports, writes nothing",
      "[dry-run]" in out and consensus(d).read_bytes() == b0
      and not list((d / "docs/operations").glob("*")) and not (d / "logs/consensus-prune.json").exists())

# (k) old archive notes are replaced by exactly one
d = newapp(); consensus(d).write_text(doc(BIG, note="- _Archive note (cycle 5): 1 older entries (cycles 1..1) moved to docs/operations/consensus-archive-2026-09.md. Not for routine reading — grep by cycle number only._\n\n"), encoding="utf-8")
run(d, 743)
check("(k) single fresh note replaces old", consensus(d).read_text(encoding="utf-8").count("_Archive note") == 1)

# (m) runtime.env override beats process env (KEEP=12 in env, 5 in runtime.env)
d = newapp(); consensus(d).write_text(doc(BIG), encoding="utf-8")
(d / "logs/runtime.env").write_text("FOO=1\nCONSENSUS_PRUNE_KEEP=5\n", encoding="utf-8")
run(d, 743)
check("(m) runtime.env KEEP override", len(re.findall(r"(?m)^- \*\*Cycle", consensus(d).read_text(encoding="utf-8"))) == 5)
(d / "logs/runtime.env").write_text("CONSENSUS_PRUNE_ENABLED=0\n", encoding="utf-8")
consensus(d).write_text(doc(BIG), encoding="utf-8"); b0 = consensus(d).read_bytes(); rc, out = run(d, 744)
check("(m2) runtime.env kill switch", out.strip() == "" and consensus(d).read_bytes() == b0)

# (n) entries <= keep while over threshold -> 'insufficient' line, NO streak alarm, untouched
d = newapp(); consensus(d).write_text(doc(BIG[:12]).replace("x" * 40, "x" * 400), encoding="utf-8")
b0 = consensus(d).read_bytes()
outs = [run(d, c)[1] for c in (1, 2, 3, 4)]
check("(n) insufficient line, no alarm, untouched",
      all("insufficient" in o for o in outs) and not any("CONSENSUS-PRUNE —" in o for o in outs)
      and consensus(d).read_bytes() == b0)

# (o) model-written multi-line archive note (prod regression, cycle 753) is dropped, not a skip
d = newapp()
model_note = ('- _Archive note (cycle 753): older "What We Did" entries for cycles 744-752 remain inline\n'
              '  because the harness archives automatically; see docs/operations/consensus-archive-2026-10.md\n\n')
consensus(d).write_text(doc(BIG, extra_bullet=model_note), encoding="utf-8")
rc, out = run(d, 754)
after = consensus(d).read_text(encoding="utf-8")
check("(o) model note: moved, single fresh note, continuation dropped",
      "moved" in out and after.count("_Archive note") == 1 and "remain inline" not in after
      and "because the harness" not in after)

# (l) guard integration: guard(N) -> prune(N) -> model appends -> guard(N+1) silent; real deletion later alarms
d = newapp(); consensus(d).write_text(doc(BIG), encoding="utf-8")
g1 = guard(d, 743); p = run(d, 743)[1]
t = consensus(d).read_text(encoding="utf-8").replace("## What We Did This Cycle\n\n", "## What We Did This Cycle\n\n" + entry(744))
consensus(d).write_text(t, encoding="utf-8")
g2 = guard(d, 744)
check("(l) guard silent across prune + new entry", "LEDGER-GUARD" not in g1 and "moved" in p and "LEDGER-GUARD" not in g2)
t2 = consensus(d).read_text(encoding="utf-8")
cut = t2.index("## Key Decisions Made"); t2 = t2[:cut] + "## Next Action\n- go\n"  # drop Key Decisions + size
consensus(d).write_text(t2 + "", encoding="utf-8")
# make the drop large enough for the size rule too: remove 6 entries
for n in BIG[6:12]:
    t2 = t2.replace(entry(n), "")
consensus(d).write_text(t2, encoding="utf-8")
g3 = guard(d, 745)
check("(l2) real deletion after prune still alarms", "LEDGER-GUARD" in g3)

print()
if _fail:
    print(f"{len(_fail)} FAILURE(S): " + ", ".join(_fail)); sys.exit(1)
print("ALL TESTS PASSED")
