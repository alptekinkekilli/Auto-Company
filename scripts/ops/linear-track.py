#!/usr/bin/env python3
"""Append to a workstream's checklist instead of opening another Linear issue.

WHY THIS EXISTS. Operator, 2026-08-02: *"Çok fazla linear açıyorsun bu proje için, sonra
arşivlemek zorunda kalıyoruz."* Three issues were opened in one turn for three facts that all
belonged to the same workstream. Each was individually defensible and collectively they made
the board a chore: 40 open issues, one thread split across four of them, and the operator
doing the cleanup.

The cause is that opening an issue was the CHEAP action and filing under an existing one was
the expensive one. This tool inverts that. `--add` is one flag; `--new` demands a written
justification that matches one of three tests, and refuses otherwise.

## When something deserves its own issue (all other cases are checklist items)

  1. **Independent owner** — someone else could pick it up without reading the parent thread.
  2. **Own lifecycle** — it has a deadline or a review date that must alarm on its own clock.
  3. **Durable capability** — it is a new surface the company will keep, not a task inside a
     thread that already exists.

Everything else — findings, blockers, follow-ups, "we should also…" — is a checklist item on
the workstream issue, where the context already lives.

## Tracks

A track is the one long-lived issue that owns a workstream. Keep the list short; a project
with five tracks is legible, a project with forty issues is not.

  linear-track.py --list
  linear-track.py --add "Deploy reply-watch once SSH returns"        # defaults to --track
  linear-track.py --add "…" --track APP-276
  linear-track.py --done "Deploy reply-watch"                        # ticks the box
  linear-track.py --comment "evidence…" --track APP-276              # evidence, not a task
  linear-track.py --new "title" --why independent-owner --body "…"   # refused without --why
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request

API = "https://api.linear.app/graphql"
TEAM_KEY = "APP"
DEFAULT_TRACK = "APP-269"
CHECKLIST_HEADING = "## Open items (this list is the tracker — do not open separate issues for these)"
# The only accepted reasons for a NEW issue. Anything else belongs on a track.
JUSTIFICATIONS = {
    "independent-owner": "someone else can pick it up without reading the parent thread",
    "own-lifecycle": "has its own deadline or review date that must alarm separately",
    "durable-capability": "a new surface the company keeps, not a task inside an existing thread",
}
TRACKS = {
    "APP-269": "Tender outreach execution — sends, templates, cohort, evidence quality",
    "APP-276": "Loop cost, pricing correctness and turn economy",
    "APP-277": "Assistant operating rules alongside the company",
    "APP-246": "Tender track strategy and pivots",
    "APP-221": "Opportunity Analyst (second brain)",
}


def key() -> str:
    k = os.environ.get("LINEAR_API_KEY", "")
    if k.startswith("lin_api_"):
        return k
    out = subprocess.run(["security", "find-generic-password", "-s", "autocompany-linear-key", "-w"],
                         capture_output=True, text=True).stdout.strip()
    if out.startswith("lin_api_"):
        return out
    # Earlier note here said the ~/.zshrc value was "malformed". Measured 2026-08-02: it is
    # not. ~/.zshrc holds no key at all, only `export LINEAR_API_KEY="$(security …)"`, and the
    # Keychain item reads back fine. What breaks is that ~/.zshrc runs for INTERACTIVE shells
    # only, so a GUI-launched Claude Code never has the variable — and .mcp.json's
    # "${LINEAR_API_KEY}" is then passed through VERBATIM to the server. Hence the Keychain
    # read above, and the same fallback now wired into .mcp.json itself.
    raise SystemExit("no usable Linear key (env LINEAR_API_KEY or Keychain autocompany-linear-key)")


def gql(query: str, variables: dict | None = None) -> dict:
    req = urllib.request.Request(API, data=json.dumps({"query": query, "variables": variables or {}}).encode(),
                                 headers={"Authorization": key(), "Content-Type": "application/json"})
    data = json.load(urllib.request.urlopen(req, timeout=40))
    if "errors" in data:
        raise SystemExit("Linear error: %s" % json.dumps(data["errors"])[:300])
    return data["data"]


def get_issue(ident: str) -> dict:
    num = float(ident.split("-")[1])
    nodes = gql('query($n:Float!){issues(filter:{team:{key:{eq:"%s"}},number:{eq:$n}})'
                '{nodes{id identifier title description}}}' % TEAM_KEY, {"n": num})["issues"]["nodes"]
    if not nodes:
        raise SystemExit("no such issue: %s" % ident)
    return nodes[0]


def set_description(issue_id: str, text: str) -> None:
    gql('mutation($i:String!,$d:String!){issueUpdate(id:$i,input:{description:$d}){success}}',
        {"i": issue_id, "d": text})


def cmd_list() -> int:
    for ident, what in TRACKS.items():
        try:
            iss = get_issue(ident)
        except SystemExit:
            print("%-9s (unreadable)" % ident)
            continue
        desc = iss.get("description") or ""
        # Linear stores a ticked box as "- [X]" (upper case) regardless of what was written,
        # so counting "- [x]" reported done=0 immediately after a successful tick.
        done = len(re.findall(r"^\s*- \[[xX]\]", desc, re.M))
        print("%-9s open=%-3d done=%-3d  %s" % (ident, desc.count("- [ ]"), done, what))
        for line in desc.split("\n"):
            if line.strip().startswith("- [ ] "):
                print("             · %s" % line.strip()[6:120])
    return 0


def cmd_add(track: str, text: str) -> int:
    iss = get_issue(track)
    desc = iss.get("description") or ""
    if CHECKLIST_HEADING not in desc:
        desc = desc.rstrip() + "\n\n---\n\n" + CHECKLIST_HEADING + "\n"
    desc = desc.rstrip() + "\n- [ ] " + text.strip() + "\n"
    set_description(iss["id"], desc)
    print("%s ← %s" % (track, text.strip()[:90]))
    return 0


def cmd_done(track: str, needle: str) -> int:
    iss = get_issue(track)
    desc = iss.get("description") or ""
    hits = [l for l in desc.split("\n") if l.strip().startswith("- [ ] ") and needle.lower() in l.lower()]
    if len(hits) != 1:
        print("refused: %d checklist items match %r — be more specific" % (len(hits), needle), file=sys.stderr)
        for h in hits:
            print("   " + h.strip()[:110], file=sys.stderr)
        return 2
    set_description(iss["id"], desc.replace(hits[0], hits[0].replace("- [ ] ", "- [x] ", 1)))
    print("ticked on %s: %s" % (track, hits[0].strip()[6:90]))
    return 0


def cmd_comment(track: str, body: str) -> int:
    gql('mutation($i:String!,$b:String!){commentCreate(input:{issueId:$i,body:$b}){success}}',
        {"i": get_issue(track)["id"], "b": body})
    print("commented on %s" % track)
    return 0


def cmd_new(title: str, why: str, body: str) -> int:
    if why not in JUSTIFICATIONS:
        print("refused: --why must be one of:", file=sys.stderr)
        for k, v in JUSTIFICATIONS.items():
            print("    %-20s %s" % (k, v), file=sys.stderr)
        print("\nIf none of these fits, it is a checklist item:\n"
              "    linear-track.py --add %r --track <TRACK>" % title, file=sys.stderr)
        return 2
    team = gql('query{teams(filter:{key:{eq:"%s"}}){nodes{id}}}' % TEAM_KEY)["teams"]["nodes"][0]["id"]
    desc = "%s\n\n---\n_Opened as its own issue because: **%s** — %s._" % (
        body.strip(), why, JUSTIFICATIONS[why])
    out = gql('mutation($t:String!,$d:String!,$team:String!)'
              '{issueCreate(input:{title:$t,description:$d,teamId:$team}){issue{identifier}}}',
              {"t": title, "d": desc, "team": team})
    print("created", out["issueCreate"]["issue"]["identifier"])
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--track", default=DEFAULT_TRACK)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--add")
    ap.add_argument("--done")
    ap.add_argument("--comment")
    ap.add_argument("--new")
    ap.add_argument("--why", default="")
    ap.add_argument("--body", default="")
    args = ap.parse_args()

    if args.list:
        return cmd_list()
    if args.add:
        return cmd_add(args.track, args.add)
    if args.done:
        return cmd_done(args.track, args.done)
    if args.comment:
        return cmd_comment(args.track, args.comment)
    if args.new:
        return cmd_new(args.new, args.why, args.body or args.new)
    ap.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
