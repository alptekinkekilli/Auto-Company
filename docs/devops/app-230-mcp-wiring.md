# APP-230 — Deterministic Airtable + Linear MCP wiring (headless-safe)

**Goal:** give the autonomous loop first-party, API-key-based access to Airtable and Linear
so it can `verify-against-systems` on **every** cycle, independent of the intermittent
claude.ai OAuth connectors (which vanished in Cycle 82; see APP-230).

## What changed (staged, ships on next deploy)

`/.mcp.json` now declares three servers (was: only `context7`):

| Server | Transport | Package / URL | Auth env var |
|--------|-----------|---------------|--------------|
| `context7` | http | `https://mcp.context7.com/mcp` | `CONTEXT7_API_KEY` (already set) |
| `airtable` | stdio (`npx -y airtable-mcp-server`) | `airtable-mcp-server` | `AIRTABLE_API_KEY` |
| `linear` | stdio (`npx -y @tacticlaunch/mcp-linear`) | `@tacticlaunch/mcp-linear` | `LINEAR_API_KEY` |

`.claude/settings.json` has `enableAllProjectMcpServers: true`, so the two new servers are
auto-enabled — no allow-list edit needed. Env values use the `${VAR}` placeholder pattern
(same as the existing `${CONTEXT7_API_KEY}`); **no secret is committed.**

## Operator action required (before / with the deploy)

Create two credentials and store them as **container env vars** via the secrets/Coolify flow:

1. **`AIRTABLE_API_KEY`** — an Airtable **Personal Access Token**.
   Minimum scopes: `data.records:read`, `schema.bases:read` (add `data.records:write` only if
   the loop should also write). Restrict its **base access** to
   `<your Airtable base>` (`<YOUR_AIRTABLE_BASE_ID>`) — do not grant all bases.

2. **`LINEAR_API_KEY`** — a Linear **Personal API key**
   (Linear → Settings → Security & access → Personal API keys). Team: `<your Linear team>`.

## Update (2026-07-25) — this doc's Linear claim above is now stale

**Both Linear and Airtable now ship official remote HTTP MCP servers that accept the
existing API-key credentials** (`https://mcp.linear.app/mcp`, `https://mcp.airtable.com/mcp`)
— the "no official API-key stdio MCP" claim below was true when this doc was written and no
longer is. This was independently verified live (real `initialize` + `tools/list` calls, no
writes) on 2026-07-25: Linear's official endpoint advertises 52 tools, Airtable's 41,
against the *same* shared `LINEAR_API_KEY` / `AIRTABLE_API_KEY` already in
`/app/logs/runtime.env`.

**What actually changed on 2026-07-25:** the Codex engine (previously stuck on
`https://developers.openai.com/mcp` only, no Linear/Airtable/Context7 at all) was wired to
Context7 + the two OFFICIAL Linear/Airtable HTTP endpoints, with a curated
create/update/comment allowlist — delete, merge/review, admin, automation, interface, and
base-create tools deliberately excluded. See
`docs/research/codex-context7-linear-airtable-wiring-answer-2026-07-25.md` (gitignored) for
the full audit trail, exact TOML, and verification gates.

**Claude's `.mcp.json` (below) was deliberately NOT touched by that change** — it still runs
the community `npx` servers described in this doc, which are working. Migrating Claude to
the same official endpoints is a separate, not-yet-scheduled decision; don't assume it
happened just because Codex moved.

## One item to verify before trusting Linear (community package) — Claude engine only

- Airtable's `airtable-mcp-server` is well-established and API-key native — low risk.
- The official Linear MCP now DOES accept an API key over its remote HTTP endpoint (see the
  update above) — this specific risk (Linear only had OAuth-remote) is resolved for any
  engine that migrates to it. Claude has not migrated yet, so this section still describes
  Claude's actual risk profile: `@tacticlaunch/mcp-linear` is a **community** package keyed
  by `LINEAR_API_KEY`. Before/at first deploy, confirm the package name + that it reads
  `LINEAR_API_KEY`, and consider pinning a version (`@tacticlaunch/mcp-linear@<x.y.z>`) instead
  of floating `-y`. If it proves unreliable, fall back to a thin Linear GraphQL REST helper
  (option B) for the Linear half only — Airtable stays as wired here.

## Failure mode is safe

If a server can't start (npm hiccup, bad key), it simply exposes no tools — the loop already
handles missing connectors gracefully (records an access gap, does not fabricate). No cycle
breaks because of this wiring.

## Acceptance (post-deploy)

- Loop's next state-audit shows Airtable + Linear reachable **via env-credentialed servers**,
  and correctly reports your Airtable tables/records and Linear issues (not "connector unavailable").
- A later cycle with the claude.ai connectors absent still has working Airtable/Linear access.
