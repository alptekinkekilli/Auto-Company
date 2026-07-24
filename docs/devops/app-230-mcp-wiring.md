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

## One item to verify before trusting Linear (community package)

- Airtable's `airtable-mcp-server` is well-established and API-key native — low risk.
- Linear has **no official API-key stdio MCP** (the official Linear MCP is OAuth-remote — the
  exact fragility we're removing). `@tacticlaunch/mcp-linear` is a **community** package keyed
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
