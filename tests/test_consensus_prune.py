#!/usr/bin/env python3
"""Tests for scripts/ops/consensus-prune.py (v2). Run: python3 tests/test_consensus_prune.py

Cases (a)-(o) are the v1 suite (fixtures built around KEEP=12, so the What We Did byte cap
is lifted for them); (p)-(z) are the v2 spec cases. (p) and (v) need the real prod copy:
set CONSENSUS_PRUNE_PROD_FIXTURE=/path/to/consensus-prod-2.md, else they print SKIP.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "ops" / "consensus-prune.py"
GUARD = REPO / "scripts" / "ops" / "ledger-guard.py"
PROD = os.environ.get("CONSENSUS_PRUNE_PROD_FIXTURE", "")
_fail = []


def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        _fail.append(name)


def skip(name, why):
    print(f"SKIP {name} — {why}")


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


def para(n, size=1500, prefix="**Cycle"):
    body = f"{prefix} {n} — note {n}.** Status text (ünicode şğı)."
    while len(body.encode()) < size:
        body += " more-" + "y" * 20
    return body + "\n\n"


def doc(entries, extra_bullet=None, note=None):
    """v1 fixture: a canonical-only file whose only entries are What We Did bullets."""
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


def doc2(wwd=(), na=(), cp=(), cs=(), tail=(), na_extra="", cp_extra="", kd_bytes=72000, head=""):
    """v2 fixture: full canonical block with paragraph entries + optional head/tail sections.
    `tail` items: (header, body) tuples; kd_bytes pads Key Decisions to keep the file over
    the 70000 threshold independently of what gets pruned."""
    s = "# Auto Company Consensus\n\n" + head
    s += "## Last Updated\n2026-10-09\n\n## Current Phase\n" + cp_extra
    for n in cp:
        s += para(n)
    s += "## What We Did This Cycle\n\n"
    for n in wwd:
        s += entry(n)
    s += "## Key Decisions Made\n- keep " + "k" * kd_bytes + "\n\n"
    s += "## Execution Controls\n- Program State: x\n\n## Active Projects\n- none\n\n## WTP Evidence\n- NONE\n\n"
    s += "## Next Action\n" + na_extra
    for n in na:
        s += para(n)
    s += "## Company State\n"
    for n in cs:
        s += para(n)
    s += "- Revenue: $0\n\n## Open Questions\n- none\n\n"
    for h, b in tail:
        s += f"{h}\n{b}\n\n"
    return s


BASE_ENV = {"CONSENSUS_PRUNE_KEEP": "12", "CONSENSUS_PRUNE_CAP_WWD": "1000000"}  # v1 fixtures


def run(d, cycle, env=None, dry=False, v1=True):
    e = dict(os.environ)
    if v1:
        e.update(BASE_ENV)
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


def headers(text):
    return re.findall(r"(?m)^(## .*)$", text)


def section(text, header, nth=0):
    """Body of the nth `header` section (header line excluded)."""
    parts = re.split(r"(?m)^(?=## )", text)
    hits = [p for p in parts if p.split("\n", 1)[0] == header]
    return hits[nth].split("\n", 1)[1] if len(hits) > nth else None


def non_cycle_paras(body):
    return [p for p in re.split(r"\n\s*\n", body) if p.strip() and not re.match(r"^\*\*Cycle\s+\d+", p)]


def archive_pieces(d):
    """Every archived piece: a whole section (kind=section) or one removed paragraph /
    bullet (kind=entries blocks are concatenations of non-adjacent pieces)."""
    files = list((d / "docs/operations").glob("consensus-archive-*.md"))
    if not files:
        return []
    t = files[0].read_text(encoding="utf-8")
    parts = re.split(r"(?m)^(## Archived at cycle .*)\n\n", t)
    pieces = []
    for i in range(1, len(parts), 2):
        header, body = parts[i], parts[i + 1].rstrip("\n")
        if "— section —" in header:
            pieces.append(body)
        else:
            pieces += [p for p in re.split(r"(?m)^(?=\*\*Cycle |- \*\*Cycle )", body) if p.strip()]
    return pieces


BIG = list(range(743, 703, -1))  # 40 entries newest-first, ~72 KB > 70000

# (a) big file -> keep 12 largest numbers, archive byte-exact, single note, invariants intact
d = newapp(); consensus(d).write_text(doc(BIG), encoding="utf-8")
before = consensus(d).read_bytes()
rc, out = run(d, 743)
after = consensus(d).read_text(encoding="utf-8")
nums = [int(m) for m in re.findall(r"(?m)^- \*\*Cycle (\d+)", after)]
check("(a) exit 0 + moved line", rc == 0 and "moved" in out and "docs/operations/consensus-archive-" in out)
check("(a) keeps 12 newest numbers", nums == BIG[:12])
arch = list((d / "docs/operations").glob("consensus-archive-*.md"))
check("(a) archive file created", len(arch) == 1)
atext = arch[0].read_text(encoding="utf-8")
gone = "".join(entry(n) for n in BIG[12:])
check("(a) archived entries byte-exact", gone in atext and "sha256:" in atext and "— entries — What We Did This Cycle —" in atext)
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
# (c2) non-monotonic numbers: v2 selects by NUMBER, no monotonicity requirement (spec §1)
d = newapp(); consensus(d).write_text(doc([743, 700, 742] + BIG[3:]), encoding="utf-8")
rc, out = run(d, 1)
nums = [int(m) for m in re.findall(r"(?m)^- \*\*Cycle (\d+)", consensus(d).read_text(encoding="utf-8"))]
check("(c2) non-monotonic: pruned by number, 700 archived, order of survivors kept",
      "moved" in out and 700 not in nums and nums == [743, 742] + BIG[3:13])
# (c3) What We Did header missing (tail pass off so the odd section is not simply archived) -> skip
d = newapp(); consensus(d).write_text(doc(BIG).replace("## What We Did This Cycle", "## Something Else"), encoding="utf-8")
b0 = consensus(d).read_bytes(); rc, out = run(d, 1, env={"CONSENSUS_PRUNE_TAIL": "0"})
check("(c3) no section: skipped + untouched", "skipped" in out and "wwd: section" in out and consensus(d).read_bytes() == b0)
# (c3b) same file with the tail pass on: the non-canonical 72 KB section would be archived, but the
# result would lose a REQUIRED marker (primary block = Key Decisions + Next Action) -> fail-closed skip
rc, out = run(d, 2)
check("(c3b) required-marker guard refuses, untouched", "required marker" in out and consensus(d).read_bytes() == b0)
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

# (i) dry-run writes nothing, prints the per-section table
d = newapp(); consensus(d).write_text(doc(BIG), encoding="utf-8")
b0 = consensus(d).read_bytes(); rc, out = run(d, 1, dry=True)
check("(i) dry-run: reports, writes nothing",
      "[dry-run]" in out and consensus(d).read_bytes() == b0
      and not list((d / "docs/operations").glob("*")) and not (d / "logs/consensus-prune.json").exists())
check("(i2) dry-run: before/after table with TOTAL", "before" in out and "after" in out and "TOTAL" in out)

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

# ----------------------------------------------------------------------------- v2 cases
# (p) real prod copy: first run moves (no skip), result <= 80 KB, primary canonical sequence
#     intact, archived blocks byte-exact from the original, non-entry paragraphs preserved,
#     second run no-op.
if PROD and Path(PROD).is_file():
    d = newapp(); shutil.copy(PROD, consensus(d))
    orig = consensus(d).read_text(encoding="utf-8")
    rc, out = run(d, 900, v1=False)
    after = consensus(d).read_text(encoding="utf-8")
    check("(p) prod: moved, no skip reason", "moved" in out and "skipped" not in out)
    check("(p) prod: result <= 80 KB, no 'insufficient'", len(after.encode()) <= 80000 and "insufficient" not in out)
    primary = ["## Current Phase", "## What We Did This Cycle", "## Key Decisions Made", "## Execution Controls",
               "## Active Projects", "## Awaiting Operator", "## WTP Evidence", "## Next Action",
               "## Company State", "## Open Questions"]
    hs = headers(after)
    pi = hs.index("## Current Phase")
    check("(p) prod: primary canonical sequence intact", hs[pi:pi + len(primary)] == primary)
    check("(p) prod: Key Decisions untouched", section(orig, "## Key Decisions Made", 1) == section(after, "## Key Decisions Made", 0))
    pieces = archive_pieces(d)
    check("(p) prod: every archived piece is byte-exact from the original and one copy fewer in the result",
          len(pieces) > 50 and all(p.rstrip("\n") in orig for p in pieces)
          and all(orig.count(p.rstrip("\n")) > after.count(p.rstrip("\n")) for p in pieces))
    ok = True
    for h in ("## Next Action", "## Current Phase", "## Company State"):
        ok = ok and non_cycle_paras(section(orig, h, 1 if h != "## Next Action" else 1)) == non_cycle_paras(section(after, h, 0))
    check("(p) prod: non-entry paragraphs of NA/CP/CS byte-equal and in order", ok)
    st = json.loads((d / "logs/consensus-prune.json").read_text())
    check("(p) prod: state rebased", st.get("post_sha16") and st["post_metrics"]["bytes"] == len(after.encode()))
    a1 = after
    rc, out = run(d, 901, v1=False)
    check("(p) prod: second run no-op, byte-equal", "moved" not in out and consensus(d).read_text(encoding="utf-8") == a1)
else:
    skip("(p) prod fixture", "set CONSENSUS_PRUNE_PROD_FIXTURE=/path/consensus-prod-2.md")

# (q) tail order broken (808,807,812,809) -> the KEEP_TAIL largest NUMBERS stay, the rest go
tail = [(f"## Cycle {n}", f"body of {n}") for n in (808, 807, 812, 809)]
d = newapp(); consensus(d).write_text(doc2(tail=tail), encoding="utf-8")
rc, out = run(d, 1, v1=False)
hs = headers(consensus(d).read_text(encoding="utf-8"))
check("(q) tail: 812 and 809 stay in place, 808/807 archived",
      "## Cycle 812" in hs and "## Cycle 809" in hs and "## Cycle 808" not in hs and "## Cycle 807" not in hs
      and "— section — Cycle 808 —" in (d / "docs/operations").glob("*").__next__().read_text(encoding="utf-8"))
check("(q) tail: file order of survivors unchanged", hs.index("## Cycle 812") < hs.index("## Cycle 809"))

# (r) unnumbered non-canonical section (head and tail) -> archived; numbered keep-tail still applies
d = newapp()
consensus(d).write_text(doc2(head="## Random Notes\nscratch\n\n", tail=[("## Leftovers", "junk"), ("## Cycle 5", "x")]), encoding="utf-8")
rc, out = run(d, 1, v1=False)
hs = headers(consensus(d).read_text(encoding="utf-8"))
check("(r) unnumbered non-canonical sections archived, numbered one kept",
      "## Random Notes" not in hs and "## Leftovers" not in hs and "## Cycle 5" in hs and "tail=2 sections" in out)

# (s) `**CORRECTED Cycle N` paragraph is NOT an entry: stays while real entries are pruned
corr = para(772, 600, prefix="**CORRECTED Cycle")
d = newapp(); consensus(d).write_text(doc2(na=[790, 789, 788, 787, 786, 785, 784, 783], na_extra="queue text here\n\n" + corr), encoding="utf-8")
rc, out = run(d, 1, v1=False)
na = section(consensus(d).read_text(encoding="utf-8"), "## Next Action")
check("(s) CORRECTED paragraph and queue text stay, entries pruned to cap",
      corr in na and na.startswith("queue text here\n\n") and len(na.encode()) <= 8192 + len("## Next Action\n")
      and "**Cycle 790" in na and "**Cycle 783" not in na and "na=" in out)

# (t) code fence inside an entry -> that section skipped, others still pruned
fenced = "**Cycle 700 — with code.**\n```\nx\n```\n\n"
d = newapp(); consensus(d).write_text(doc2(wwd=BIG[:12], na=[790, 789, 788, 787, 786, 785], na_extra=fenced), encoding="utf-8")
b_na = section(consensus(d).read_text(encoding="utf-8"), "## Next Action")
rc, out = run(d, 1, v1=False)
t_after = consensus(d).read_text(encoding="utf-8")
check("(t) fence: NA skipped with reason, NA untouched, WWD still pruned",
      "na: code fence" in out and section(t_after, "## Next Action") == b_na and "wwd=8" in out)

# (u) each kill switch alone leaves its own target untouched; all off -> byte-equal
def full():
    return doc2(wwd=BIG[:12], na=[790, 789, 788, 787, 786, 785, 784], cp=[780, 779, 778, 777, 776, 775],
                cs=[770, 769, 768, 767, 766], tail=[(f"## Cycle {n}", "b" * 400) for n in (801, 802, 803)])
targets = {"TAIL": lambda t: "## Cycle 801" in headers(t), "NA": lambda t: "**Cycle 784" in t,
           "CP": lambda t: "**Cycle 775" in t, "CS": lambda t: "**Cycle 766" in t,
           "WWD": lambda t: f"**Cycle {BIG[11]}" in t}
for sw, still_there in targets.items():
    d = newapp(); consensus(d).write_text(full(), encoding="utf-8")
    rc, out = run(d, 1, v1=False, env={f"CONSENSUS_PRUNE_{sw}": "0"})
    t_after = consensus(d).read_text(encoding="utf-8")
    others = [k for k in targets if k != sw]
    check(f"(u) switch {sw}=0: its target untouched, others pruned",
          still_there(t_after) and "moved" in out and all(not targets[k](t_after) for k in others))
d = newapp(); consensus(d).write_text(full(), encoding="utf-8"); b0 = consensus(d).read_bytes()
rc, out = run(d, 1, v1=False, env={f"CONSENSUS_PRUNE_{k}": "0" for k in targets})
check("(u) all switches off: byte-equal, no alarm", consensus(d).read_bytes() == b0 and "CONSENSUS-PRUNE —" not in out)

# (w) byte cap: 5 KB entries -> section ends under cap; a single 9 KB entry still stays
d = newapp(); consensus(d).write_text(doc2(na=[804, 803, 802, 801]).replace(para(804), para(804, 5000)).replace(para(803), para(803, 5000)).replace(para(802), para(802, 5000)).replace(para(801), para(801, 5000)), encoding="utf-8")
rc, out = run(d, 1, v1=False)
na = section(consensus(d).read_text(encoding="utf-8"), "## Next Action")
check("(w) cap: NA under 8192, newest entry kept", len(na.encode()) < 8192 and "**Cycle 804" in na and "**Cycle 803" not in na)
d = newapp(); consensus(d).write_text(doc2(na=[804]).replace(para(804), para(804, 9000)), encoding="utf-8")
b0 = consensus(d).read_bytes(); rc, out = run(d, 1, v1=False)
check("(w2) cap: a lone 9 KB entry is never removed (nothing to move -> insufficient, untouched)",
      "insufficient" in out and consensus(d).read_bytes() == b0)

# (x) duplicate cycle number in NA -> NA skipped with reason; the rest still runs
d = newapp(); consensus(d).write_text(doc2(wwd=BIG[:12], na=[790, 789, 789, 787, 786, 785]), encoding="utf-8")
b_na = section(consensus(d).read_text(encoding="utf-8"), "## Next Action")
rc, out = run(d, 1, v1=False)
check("(x) duplicate number: NA skipped + reason, WWD pruned",
      "na: duplicate cycle numbers" in out and section(consensus(d).read_text(encoding="utf-8"), "## Next Action") == b_na and "wwd=8" in out)

# (y) skip path never touches the guard-facing state keys
d = newapp(); consensus(d).write_text(doc(BIG), encoding="utf-8"); run(d, 743)
st1 = json.loads((d / "logs/consensus-prune.json").read_text())
consensus(d).write_text(doc(BIG, extra_bullet="- odd\n"), encoding="utf-8")
rc, out = run(d, 744)
st2 = json.loads((d / "logs/consensus-prune.json").read_text())
check("(y) skip: pre/post sha + post_metrics unchanged, streak counted",
      "skipped" in out and all(st1[k] == st2[k] for k in ("pre_sha16", "post_sha16", "post_metrics"))
      and st2["skipped_streak"] == 1)

# (z) bloat warning: a section growing >10 KB across 3 runs prints the alarm-prefixed line
d = newapp()
outs = []
for i in range(3):
    consensus(d).write_text(doc2(na_extra="queue " + "q" * (6000 * i) + "\n\n"), encoding="utf-8")
    outs.append(run(d, 10 + i, v1=False)[1])
check("(z) bloat: no warning on runs 1-2, warning on run 3 names 'na'",
      "şişme" not in outs[0] and "şişme" not in outs[1] and "CONSENSUS-PRUNE — yeni şişme yeri" in outs[2] and "na +" in outs[2])

# (v) guard + prod copy: guard(N) -> prune(N) -> model appends -> guard(N+1) silent; real loss alarms
if PROD and Path(PROD).is_file():
    d = newapp(); shutil.copy(PROD, consensus(d))
    g1 = guard(d, 900); p = run(d, 900, v1=False)[1]
    t = consensus(d).read_text(encoding="utf-8")
    t = t.replace("## What We Did This Cycle\n", "## What We Did This Cycle\n" + entry(901), 1)
    consensus(d).write_text(t, encoding="utf-8")
    g2 = guard(d, 901)
    check("(v) prod: guard silent across prune cycle", "LEDGER-GUARD" not in g1 and "moved" in p and "LEDGER-GUARD" not in g2)
    cut = t.index("## Key Decisions Made"); nxt = t.index("## Execution Controls", cut)
    lossy = t[:cut] + t[nxt:]  # artificial loss: Key Decisions gone (-26 KB, -1 section)
    # The real prod text carries INCIDENT_RE words ("incident", "restored", "lost", ...) in
    # unrelated places, which blinds the guard by its own design (not a prune regression).
    # Prove the post-prune baseline still alarms once that blinding is removed.
    inc_re = re.search(r'INCIDENT_RE = re\.compile\(\s*r"([^"]+)"', (REPO / "scripts/ops/ledger-guard.py").read_text(encoding="utf-8")).group(1)
    if re.search(inc_re, lossy, re.IGNORECASE):
        print("INFO (v) prod text contains INCIDENT_RE words -> guard blind by design; testing with them neutralised")
        lossy = re.sub(inc_re, lambda m: "x" * len(m.group(0)), lossy, flags=re.IGNORECASE)
    consensus(d).write_text(lossy, encoding="utf-8")
    check("(v) prod: artificial deletion after prune alarms", "LEDGER-GUARD" in guard(d, 902))
else:
    skip("(v) prod guard", "set CONSENSUS_PRUNE_PROD_FIXTURE=/path/consensus-prod-2.md")

print()
if _fail:
    print(f"{len(_fail)} FAILURE(S): " + ", ".join(_fail)); sys.exit(1)
print("ALL TESTS PASSED")
