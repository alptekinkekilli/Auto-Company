#!/usr/bin/env python3
"""May this firm be emailed right now? Decided from live evidence, fail-closed.

Operator decision, 2026-08-02: dispatch is no longer operator-triggered. The company sends
autonomously to firms that pass the gates, reads and answers replies itself, and the operator
enters only at payment. That removes the single human check that stood between a bad row and
a real company's inbox — so the gates stop being documentation and become the brake. This is
the brake.

  send-gate.py --record recXXXX          # one firm: ALLOW or REFUSE with the reason
  send-gate.py --report                  # the caps, and who is currently eligible

## What it enforces, in the order that fails cheapest first

1. **Caps** — 3 sends per UTC day, 20 in total. Chosen by the operator as the blast radius of
   a mistake, not as a throughput target: a wrong gate can now reach 3 firms before anyone
   looks, instead of 20 in an afternoon.
2. **Never twice** — a firm that already has a send is out. Duplicate outreach is the most
   visible possible error to the recipient.
3. **Opt-out** — an opted-out firm is permanently out, checked at the firm level, not the
   address level.
4. **G4, verified LIVE** — `g4-check.py` re-derives attribution from the site and the register
   at this moment. A `G4 PASS` written in a field is a claim, not evidence, and with no human
   in the path a self-declaration would be the only thing standing between a guess and a
   stranger's inbox.

Any check that cannot be completed is a REFUSE, never an ALLOW: with the operator out of the
loop, "I could not tell" and "it is fine" must not produce the same outcome.

## What this tool deliberately does NOT do

It does not send. It answers one question and exits; `send-email.js` still owns delivery and
keeps its own suppression, commitment and daily-cap guards. Two independent brakes on the
same action is the point — this one knows about eligibility, that one about volume and
compliance, and neither can be talked out of its half.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import importlib.util
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
API_ROOT = "https://api.airtable.com/v0"
BASE = "appPLc31jSlgulX3D"
OUTREACH = "tbl1fZbNmolrEXAMy"
BRIDGE = "tblREW6MtTMTP5h5N"
DAILY_CAP = 3
GROUND_MAX_CHARS = 300   # healthy sent grounds measured 50-204
GROUND_MAX_EN = 3        # healthy sent grounds measured 0
TOTAL_CAP = 20


PREQUAL = ("ön yeterlik", "on yeterlik", "ön yeterlilik")
BID = ("teklifinin değerlendirme dışı", "tekliflerinin değerlendirme dışı",
       "teklifin değerlendirme dışı", "teklifleri değerlendirme dışı")


def phase_of(decision_text: str) -> str:
    """Which stage did the authority actually eliminate at — from ITS OWN operative sentence.

    Not from our prose. N.K.Y (2025/UD.I-1751) reads "İş Ortaklığının ön yeterlik başvurusunun
    yeterli kabul edilmeyerek ön yeterlik değerlendirmesi dışında bırakılması": nobody had bid
    yet. The approved template says "teklif değerlendirilmeden önce eleyebilir" and "…
    değerlendirme dışı bırakıldığını gördüm", which describes bid evaluation — so that message
    told a real firm the wrong thing about its own file (sent 2026-08-02 15:01Z).

    Returns "PREQUAL", "BID", or "UNKNOWN". UNKNOWN is a refusal upstream, never a pass: a
    stage we cannot read is a claim we cannot make.
    """
    tail = (decision_text or "")[-4000:].lower()
    if not tail:
        return "UNKNOWN"
    pre = any(k in tail for k in PREQUAL)
    bid = any(k in tail for k in BID)
    if pre and not bid:
        return "PREQUAL"
    if bid and not pre:
        return "BID"
    if pre and bid:
        # Both appear: let the operative sentence decide by whichever comes last.
        return "PREQUAL" if max(tail.rfind(k) for k in PREQUAL) > max(
            tail.rfind(k) for k in BID) else "BID"
    return "UNKNOWN"


def body_claims(body: str) -> str:
    """What stage does the message assert? Mirrors the approved template's own wording."""
    b = (body or "").lower()
    if any(k in b for k in PREQUAL):
        return "PREQUAL"
    if "değerlendirme dışı bırakıld" in b or "teklif değerlendirilmeden" in b:
        return "BID"
    return "UNKNOWN"


def load_key(app_dir: str) -> None:
    if os.environ.get("AIRTABLE_API_KEY"):
        return
    try:
        with open(os.path.join(app_dir, "logs", "runtime.env"), encoding="utf-8",
                  errors="replace") as fh:
            for line in fh:
                k, _, v = line.strip().partition("=")
                if k.strip() == "AIRTABLE_API_KEY":
                    os.environ["AIRTABLE_API_KEY"] = v.strip().strip('"').strip("'")
                    return
    except OSError:
        pass
    if sys.platform == "darwin":
        out = subprocess.run(["security", "find-generic-password", "-w",
                              "-s", "autocompany-airtable-pat"],
                             capture_output=True, text=True, timeout=10).stdout.strip()
        if out:
            os.environ["AIRTABLE_API_KEY"] = out


def air(path: str, params: dict | None = None) -> dict:
    # Quote the path component: Airtable accepts a table NAME as well as an ID, and a name
    # with a space ("Ihale Outreach") produced a malformed URL. Found by the company itself
    # in cycle #7, 2026-08-02 — its fix lived only in the container and the next deploy wiped
    # it, so it is ported here where it survives.
    url = "%s/%s/%s" % (API_ROOT, BASE, "/".join(urllib.parse.quote(p, safe="") for p in path.split("/")))
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "Authorization": "Bearer " + os.environ["AIRTABLE_API_KEY"]})
    return json.load(urllib.request.urlopen(req, timeout=45))


def sent_rows() -> list[dict]:
    """Every row that has actually been emailed. TEST rows are excluded by status, not by
    name-matching: a real firm could contain the word 'test'."""
    out = []
    for r in air(OUTREACH, {"filterByFormula": "NOT({Last contact date}='')",
                            "maxRecords": 200}).get("records", []):
        f = r.get("fields", {})
        if "TEST" in (f.get("Status") or "").upper():
            continue
        out.append(f)
    return out


def counts() -> tuple[int, int]:
    rows = sent_rows()
    today = _dt.datetime.now(_dt.timezone.utc).date().isoformat()
    return sum(1 for f in rows if (f.get("Last contact date") or "").startswith(today)), len(rows)


def opted_out(fields: dict) -> bool:
    blob = " ".join(str(fields.get(k) or "") for k in
                    ("Status", "Notes", "Email log", "Last channel used")).lower()
    return "opt-out" in blob or "opt out" in blob or "listeden çık" in blob


# BODY LEAK SCANNER (directive 2026-08-02 revision 3). Four marker classes, each named in the
# directive verbatim. Word-boundaried where the marker is an ordinary word that could otherwise
# appear inside an unrelated one (e.g. "ross" inside "across"); left as plain substrings where
# the marker is already distinctive enough that a boundary would only weaken it (e.g. "OPREQ").
# Every entry is (compiled pattern, human label) so a refusal can name exactly what it hit.
_NAME_MARKERS = ["munger", "bezos", "vogels", "norman", "duarte", "cooper", "dhh", "bach",
                 "hightower", "godin", "pg", "graham", "ross", "campbell", "thompson"]
BODY_LEAK_MARKERS = (
    [(re.compile(r"\b%s\b" % re.escape(n), re.IGNORECASE), n) for n in _NAME_MARKERS]
    + [(re.compile(re.escape(m), re.IGNORECASE), m) for m in (
        "PASS WITH CONDITIONS", "NO-GO", "OPREQ", "WTP", "HOLD —", "HOLD -",
        "grep-confirmed", "sha256:", "content_hash",
        "Category 1", "Category 2", "Category 3",
        "Deliberately NOT", "not a usable pitch", "do not create a row",
    )]
)


def body_leak_scan(body: str) -> str:
    """Refuse a send whose body carries internal-only vocabulary. Returns the empty string
    when clean, or a message naming the exact marker hit (never a bare "leak found" — a
    refusal that does not say what tripped it gets worked around, per the directive)."""
    for pattern, label in BODY_LEAK_MARKERS:
        m = pattern.search(body)
        if m:
            return "marker %r matched %r" % (label, m.group(0))
    return ""


def g4_live(firm: str, app_dir: str) -> tuple[bool, str]:
    """Re-derive G4 now. The bridge row is found by firm name because that is the only link
    the two tables share; an ambiguous match is a REFUSE, not a guess."""
    spec = importlib.util.spec_from_file_location("g4", os.path.join(HERE, "g4-check.py"))
    g4 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g4)
    key = re.sub(r"[^A-Za-zÇĞİÖŞÜçğıöşü ]", " ", firm).split()
    if not key:
        return False, "firm name unusable for bridge lookup"
    token = max(key, key=len)
    recs = air(BRIDGE, {"filterByFormula": "SEARCH(UPPER('%s'),UPPER({firm}))" % token,
                        "maxRecords": 5}).get("records", [])
    if len(recs) != 1:
        return False, ("registry bridge match is ambiguous for %r: %d rows — cannot verify G4"
                       % (token, len(recs)))
    v = g4.judge(recs[0].get("fields", {}), "", os.environ.get(
        "BROWSEROS_MCP", "http://172.17.0.1:9245/mcp"))
    return v.get("verdict") == "PASS", "%s — %s" % (v.get("verdict"), v.get("reason", ""))


def decide(rec: str, app_dir: str) -> dict:
    fields = air("%s/%s" % (OUTREACH, rec)).get("fields", {})
    firm = fields.get("Business", "") or ""
    d = {"record": rec, "firm": firm[:70]}
    day, total = counts()
    d["sent_today"], d["sent_total"] = day, total

    if day >= DAILY_CAP:
        return {**d, "verdict": "REFUSE", "reason": "daily cap reached (%d/%d)" % (day, DAILY_CAP)}
    if total >= TOTAL_CAP:
        return {**d, "verdict": "REFUSE", "reason": "total cap reached (%d/%d)" % (total, TOTAL_CAP)}
    if fields.get("Last contact date"):
        return {**d, "verdict": "REFUSE",
                "reason": "already contacted on %s — never send twice" % fields["Last contact date"]}
    if opted_out(fields):
        return {**d, "verdict": "REFUSE", "reason": "firm has opted out"}
    if (fields.get("Status") or "") != "Qualified":
        return {**d, "verdict": "REFUSE", "reason": "Status is %r, not 'Qualified'"
                % fields.get("Status")}
    # Status vs Notes. Arkenom (2026-08-02) carried Status='Qualified' while its Notes said
    # "G4 RE-VERIFICATION FAILED ... MOVED TO HELD" — and the firm had already been emailed.
    # The gate keyed on Status alone, so a row can disagree with itself and still pass. Rows
    # are append-only, so ORDER stands in for time: an unresolved HOLD marker is one with no
    # resolution stamp after it. Write "G4 RESOLVED <date>" (or SUPERSEDED / ÇÖZÜLDÜ) below
    # the old marker when it is genuinely settled — never delete the marker.
    notes = fields.get("Notes") or ""
    hold_at = max([notes.upper().rfind(m) for m in
                   ("MOVED TO HELD", "G4 RE-VERIFICATION FAILED", "HELD - EVIDENCE")] )
    res_at = max([notes.upper().rfind(m) for m in
                  ("G4 RESOLVED", "SUPERSEDED", "ÇÖZÜLDÜ", "G4 ÇÖZÜLDÜ")])
    if hold_at >= 0 and res_at < hold_at:
        return {**d, "verdict": "REFUSE",
                "reason": "row disagrees with itself: Status='Qualified' but Notes carry an "
                          "unresolved HOLD marker. Settle it and stamp 'G4 RESOLVED <date>' "
                          "below the marker, or set the Status that is actually true."}
    addr = (fields.get("Email") or "").strip()
    if "@" not in addr:
        return {**d, "verdict": "REFUSE", "reason": "no usable email address on the row"}
    d["email"] = addr
    # READINESS, not just eligibility. The first autonomous send attempt (2026-08-02, Rayelsis)
    # was ALLOWed against a row with no subject or body: the send path refused it and wrote
    # "Failed: Missing Email / Email subject / Email body" into the compliance log, which then
    # surfaced to the operator as a delivery problem. Eligible and ready are different
    # questions and the gate owes an answer to both.
    missing = [k for k in ("Email subject", "Email body") if not (fields.get(k) or "").strip()]
    if missing:
        return {**d, "verdict": "REFUSE",
                "reason": "row is not ready to send: %s empty — render the template into the "
                          "row first" % ", ".join(missing)}

    # BODY LEAK SCAN (directive 2026-08-02 revision 3, root-caused by the N.K.Y incident of
    # 2026-08-02T15:01Z). A message went out whose facts were correct but which carried the
    # company's own internal reasoning into a stranger's inbox — which agent ruled what, which
    # rows were deliberately not created, method notes, process vocabulary. Nobody forgot a
    # rule; there was no check. This is that check, and it runs before every other body-
    # dependent gate below, exactly like every other check here: any failure is a REFUSE, never
    # an ALLOW, because a scanner that cannot be completed is exactly the kind of "I could not
    # tell" this whole gate exists to turn into a refusal rather than a pass.
    try:
        leak = body_leak_scan(fields.get("Email body") or "")
    except Exception as e:                       # noqa: BLE001 - a scanner error is a refusal
        return {**d, "verdict": "REFUSE",
                "reason": "body leak scan failed to run: %s" % e}
    if leak:
        return {**d, "verdict": "REFUSE",
                "reason": "Email body carries internal vocabulary and must not be sent: %s" % leak}

    # UNSPLIT MIGRATION GUARD. A row whose own `Exclusion ground` field still carries internal
    # vocabulary has not been through the split yet — the template that renders `Email body`
    # from `Exclusion ground` would carry the leak forward even though the body scan above
    # only sees what was rendered so far. Catch the source field too, so a half-finished
    # migration cannot send just because nobody re-rendered the body yet.
    eg_leak = body_leak_scan(fields.get("Exclusion ground") or "")
    if eg_leak:
        return {**d, "verdict": "REFUSE",
                "reason": "row's 'Exclusion ground' is not split yet — internal vocabulary "
                          "still present: %s" % eg_leak}

    # The ground sentence is INTERPOLATED verbatim into the customer-facing template, and that
    # field doubles as an internal research note. N.K.Y (2026-08-02) shipped 1,234 characters of
    # English analysis into a Turkish sentence — including a parenthetical inference about a
    # DIFFERENT company — because nothing checked that the field was fit to send. Every other
    # sent firm's ground is 50-204 characters of plain Turkish with zero English markers, so
    # both bars below are far from the healthy range and would have caught only this one.
    ground = (fields.get("Exclusion ground") or "").strip()
    if ground:
        en = len(re.findall(r"\b(the|and|of|was|were|not|by name|per|independently|"
                            r"attributed|submitted|defect\w*)\b", ground, re.I))
        if len(ground) > GROUND_MAX_CHARS or en >= GROUND_MAX_EN:
            return {**d, "verdict": "REFUSE",
                    "reason": "'Exclusion ground' is not fit to send verbatim (%d chars, %d "
                              "English markers). It goes into the customer's sentence as-is; "
                              "rewrite it as one short Turkish clause naming only THIS firm."
                              % (len(ground), en)}

    # PHASE. Read the stage from the authority's own decision and require the message to say
    # the same thing. Fetching costs a round trip, so it runs only once the row is otherwise
    # ready to send.
    src = (fields.get("Exclusion ground source") or "") + " " + (fields.get("Notes") or "")
    kid = re.search(r"KararId=([0-9a-f]{64})", src)
    if kid:
        try:
            spec = importlib.util.spec_from_file_location(
                "kdr", os.path.join(HERE, "kik-decision-read.py"))
            kdr = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(kdr)
            dec = kdr.text_of(kdr.fetch(
                "https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=" + kid.group(1)))
        except Exception as e:                    # noqa: BLE001 — unreadable is a refusal
            return {**d, "verdict": "REFUSE",
                    "reason": "could not read the decision to check the procurement phase: %s" % e}
        dphase = phase_of(dec)
        bphase = body_claims(fields.get("Email body") or "")
        d["phase"] = "decision=%s body=%s" % (dphase, bphase)
        if dphase == "UNKNOWN":
            return {**d, "verdict": "REFUSE",
                    "reason": "cannot tell from the decision whether this was ön yeterlik or "
                              "teklif evaluation — a stage we cannot read is a claim we cannot make"}
        if bphase != dphase:
            return {**d, "verdict": "REFUSE",
                    "reason": "phase mismatch: the decision is %s but the message says %s. "
                              "Saying 'teklif değerlendirme dışı' about an ön yeterlik "
                              "elimination tells the firm the wrong thing about its own file."
                              % (dphase, bphase)}

    # GROUP-ROUTED outreach (operator decision, 2026-08-02). Some bidders are members of a
    # multi-company group whose public contact is a GROUP mailbox: no page ties that mailbox
    # to one member, so strict G4 can never pass, and the firm becomes unreachable forever.
    # The operator's resolution is better than the rule it replaces: write to the group, and
    # NAME the bidding legal person and the decision inside the message. The identity risk G4
    # guards against is accusing the wrong company — naming the firm and the karar no makes a
    # misroute self-correcting instead of defamatory.
    #
    # This is a narrower permission than it looks, and the gate enforces all of it:
    #   * the recipient domain must be the group domain recorded on the row, and the address
    #     must be first-party on it (a group mailbox, not a third-party form);
    #   * the BODY must contain the FULL registered title, so the reader knows exactly which
    #     member company is meant;
    #   * the BODY must contain the KİK karar no, so the claim is checkable at source.
    # Miss any of those and it is a REFUSE, exactly like a failed G4.
    group_note = (fields.get("Notes") or "") + " " + (fields.get("Email body") or "")
    if (fields.get("Outreach mode") or "").strip().upper() == "GROUP_ROUTED":
        body = fields.get("Email body") or ""
        title = (fields.get("Registered title") or "").strip()
        karar = (fields.get("KIK exclusion ref") or "").strip()
        kno = re.search(r"\d{4}/[A-ZÇĞİÖŞÜ]{2}\.[IVX]+-\d+", karar or "")
        gaps = []
        if not title:
            gaps.append("row has no 'Registered title' to name in the body")
        elif title.upper() not in body.upper():
            gaps.append("body does not contain the FULL registered title")
        if not kno:
            gaps.append("row has no parsable KİK karar no")
        elif kno.group(0) not in body:
            gaps.append("body does not cite the KİK karar no (%s)" % kno.group(0))
        gdom = (fields.get("Group domain") or "").strip().lower()
        if not gdom:
            gaps.append("row records no verified 'Group domain'")
        elif not addr.lower().endswith("@" + gdom):
            gaps.append("recipient %s is not first-party on the group domain %s" % (addr, gdom))
        if gaps:
            return {**d, "verdict": "REFUSE",
                    "reason": "group-routed send is not evidenced: " + "; ".join(gaps)}
        return {**d, "verdict": "ALLOW",
                "reason": "GROUP_ROUTED: %s on %s; body names %s and cites %s (caps %d/%d today, "
                          "%d/%d total)" % (addr, gdom, title[:40], kno.group(0),
                                            day, DAILY_CAP, total, TOTAL_CAP)}

    try:
        ok, why = g4_live(firm, app_dir)
    except Exception as e:                       # noqa: BLE001 - any failure is a refusal
        return {**d, "verdict": "REFUSE", "reason": "G4 re-verification failed to run: %s" % e}
    d["g4"] = why
    if not ok:
        return {**d, "verdict": "REFUSE", "reason": "G4 not verifiable right now: %s" % why}
    return {**d, "verdict": "ALLOW",
            "reason": "caps %d/%d today, %d/%d total; G4 %s" % (day, DAILY_CAP, total, TOTAL_CAP, why)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--app", default=os.environ.get("APP_DIR", "/app"))
    ap.add_argument("--record", help="outreach row to decide")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    load_key(args.app)
    if not os.environ.get("AIRTABLE_API_KEY"):
        print("AIRTABLE_API_KEY not found", file=sys.stderr)
        return 2

    if args.report:
        day, total = counts()
        print("sends: %d/%d today (UTC), %d/%d total" % (day, DAILY_CAP, total, TOTAL_CAP))
        print("remaining: %d today, %d overall" % (max(0, DAILY_CAP - day), max(0, TOTAL_CAP - total)))
        return 0
    if not args.record:
        print("give --record recXXXX, or --report", file=sys.stderr)
        return 2

    d = decide(args.record, args.app)
    if args.json:
        print(json.dumps(d, ensure_ascii=False, indent=1))
    else:
        print("[SEND %s] %s" % (d["verdict"], d["firm"]))
        print("    %s" % d["reason"])
    return 0 if d["verdict"] == "ALLOW" else 1


if __name__ == "__main__":
    raise SystemExit(main())
