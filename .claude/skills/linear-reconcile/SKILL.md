---
name: linear-reconcile
description: "Keep Linear (team APP) issues truthful. Use when finishing work tied to an APP issue, when the user asks to review/check in-progress issues, or before winding down a session that touched Auto-Company work. Sweeps in-progress issues, verifies each against ground-truth systems (git/container/Airtable/env/wrangler), and updates state + an evidence comment. Prevents stale 'In Progress' issues whose descriptions no longer match reality."
argument-hint: "[optional: project name or issue id to focus on]"
---

# Linear Reconcile — sweep + system-verification

Keep the Linear board honest. An issue that says "In Progress / not yet built" while the work is already shipped is worse than no issue: it makes the operator re-investigate finished work and hides the real blocker. This skill is the antidote — a repeatable **sweep → verify-against-systems → update** loop.

> Operator's standing rule (2026-07-23): *"in-progress olanları güncellemiyorsun… bunu kalıcı hale getir."* All substantive work is tracked in **Linear team Appricode/APP**; GitHub for code, Asana for non-software. Read the issue before developing; verify before closing.

## When to use

- You just finished a chunk of work tied to an APP issue → close the loop **now**, same session.
- The user asks to "review / check where we are on the in-progress issues."
- You're winding down a session that touched Auto-Company work → reconcile before ending.

## Core principle — verify against systems, NOT memory or the issue text

The issue description is a **claim to check**, not a fact. It is usually the stale thing. Before reporting or changing state, pull ground truth from the actual system. Never mark Done off recollection.

## Workflow

### 1. Scope the sweep
`list_issues(team: "APP", state: "In Progress")`, then filter to the relevant `project` (default focus: **"Auto-Company Self-Hosting"**). If `$ARGUMENTS` names a project or issue id, scope to that.
- **Exclude APP-205** (appricode-panel) unless explicitly asked — it is intentionally HOLD/gated.

### 2. Get ground truth per issue
For each issue, `get_issue(id)` to read the full description + its checklist/Status block, then verify each claim against its real source:

| Claim is about… | Verify with |
|-----------------|-------------|
| Code shipped / feature built | `git log --oneline` in `~/projects/autocompany` (grep the APP-id / feature); read the file |
| Company-loop output (docs, consensus, directive) | `ssh powerupp-ts` → `docker exec <z12a992…> sh -lc "…"` on `/app/docs`, `/app/memories/consensus.md`, `/app/memories/human-directive.md` |
| Airtable CRM (records, drafts, emails, queue) | Airtable MCP `list_records_for_table` on base `appPLc31jSlgulX3D` |
| Config / secret wired (COMPANY_ADDRESS, tokens) | read the project `.env` (chmod 600) or Keychain via `security find-generic-password`; **never print secret values** |
| Worker / deploy live | `wrangler` deploys, or fetch the public URL and confirm HTTP 200 + expected content |
| Dashboard endpoint | curl the container's internal port (dashboard listens on **8787**, not published) |

**Container gotcha:** `docker exec … sh -lc 'echo $VAR'` shows a *fresh* shell, not the entrypoint-sourced env the loop/dashboard actually run with — don't diagnose runtime env that way. (See memory `redeploy-auto-company`.)

### 3. Decide the state transition
Linear state categories are fixed-order: **Backlog → Todo → In Progress → Done → Canceled** (`statusType`: backlog / unstarted / started / completed / canceled).
- **→ Done** only when ground truth confirms the issue's *committed scope* is delivered. Verify, don't assume.
- **Stay In Progress** when genuinely open — but the comment must state the **real remaining item + whose court it's in** (operator decision / human outreach / operator registration), not a stale build-status.
- **Scope split:** if part is done and part is blocked on something separate, close the done part and **spin off** the remainder into its own issue (Backlog) so nothing is lost — e.g. APP-211 email→Done, SMS/WhatsApp/Voice→APP-219. Set `parentId` to keep the tree.
- **Don't over-close.** WTP-validation issues stay open until a real paid signal (WTP hard-STOP); $0 verified revenue ≠ done.

### 4. Update — state + evidence comment
Always pair a state change with a `save_comment` carrying the **verified evidence** (commit hash, deployed URL, record count, file path, `git`/Airtable proof). Then `save_issue(id, state: …)`.

Evidence-comment template:
```
## Doğrulama: <BUILT ✅ | blocker ÇÖZÜLDÜ ✅ | durum güncellemesi>
<what the description claimed> → <what's actually true>.
- <evidence 1: commit / URL / record count / file path>
- <evidence 2>
Kalan (varsa): <real remaining item> — <kimde: operator / human outreach / registration>. → <Done | In Progress>
```

### 5. Reconcile before ending
Before winding down, re-run the sweep and confirm every remaining In-Progress issue has a dated comment reflecting reality. Report a short ledger (issue → action → evidence) to the operator.

## Reference IDs (this project)
- Team **APP** (Appricode) · project **"Auto-Company Self-Hosting"** (`b3fe27ee-d4ad-4bf0-9738-09d51199412d`).
- Airtable base `appPLc31jSlgulX3D`: Pilot Outreach `tblkWiB8xKnfX1G0E`, Spend-Audit Outreach `tblV8XWdHKop7FQ2F`, Templates `tblEbWWGgD8rjYZgW`.
- Container host `powerupp-ts`; Coolify app UUID `z12a992i3ty202zezspij2fn`.

## Linear MCP tools
`list_issues` (sweep) · `get_issue` (full description + checklist) · `save_comment` (evidence, `issueId`+`body`) · `save_issue` (`id`+`state`, or create with `team`+`title`+`project`+`parentId`) · `search_documentation` (Linear feature/state semantics).

## Grounding — Linear GraphQL/SDK (verified via Context7, `/websites/linear_app_developers` + `/linear/linear`)
The MCP tools wrap these primitives; knowing them explains the tools' behavior:
- **State has a `type`, not just a name.** Filter category-wide with `filter: { state: { type: { eq: "started" } } }` — enum: `backlog | unstarted | started | completed | canceled | triage`. `list_issues(state: "In Progress")` maps to `type: started`. Combine criteria with `and: [ { state: {…} }, { project: {…} } ]`.
- **State changes go through `stateId` (a workflow-state UUID), not the name.** `issueUpdate(id, input: { stateId })`. Fetch valid states via `workflowStates { nodes { id name type } }`. The MCP `save_issue(state: "Done")` resolves the name → id for you; if a name is ambiguous/renamed, resolve the id first.
- **⚠️ Edits within the first ~3 minutes of issue creation are NOT logged in the activity feed.** So when you create-then-immediately-update an issue, add an explicit `save_comment` — don't rely on the activity log to show the change.
- Create = `issueCreate(input: { title, teamId, … })`; comment = `commentCreate(input: { issueId, body })`. No `stateId` on create ⇒ defaults to the team's first state (or Triage).

## Guardrails
- Never print secret values while verifying config.
- Don't touch APP-205 / the original `appricode-panel` repo.
- Verify a deploy is actually live (HTTP 200 + content) before writing "live" in a comment.
