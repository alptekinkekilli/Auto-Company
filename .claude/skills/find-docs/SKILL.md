---
name: find-docs
description: Current documentation for any EXTERNAL library/framework/API via the ctx7 CLI. Use BEFORE writing code against, or designing an integration with, anything outside the standard library — Airtable/Cloudflare/Stripe/Paddle APIs, npm or pip packages, wrangler config, webhook signatures. Training data is stale; verify the current API surface first. Pure CLI (npx) — works on BOTH engines, adds zero per-turn tool surface.
---

# find-docs — loop adaptation (2026-08-03)

The upstream skill triggers on "user asks about a library"; there is no user here. The
loop trigger is: **you are about to write or modify code that talks to something outside
the Python/Node standard library, or to design against an external API.** That is the
same moment CLAUDE.md's Context7 rule and `context7-check.py` care about.

## Steps — at most 3 commands per question, ONE concept per command

1. Resolve the library (skip if you already know the `/org/project` id):
   `npx ctx7@latest library <name> "<specific question>"`
   Pick by exact-name match, snippet count, source reputation, benchmark score.
2. Fetch, with CONTEXT HYGIENE (Runtime Guardrail 6 — a raw dump re-bills every later turn):
   `npx ctx7@latest docs /org/project "<specific question>" > /tmp/ctx7.txt 2>&1; grep -n -A6 "<term>" /tmp/ctx7.txt | head -40`
   Read back only the excerpt you need, never the whole output. `--json` exists for
   scripted extraction. Version-specific ids: `/org/project/version`.
3. Record the consultation: one line in consensus naming the library id and that the
   path was **ctx7 CLI** (the CLAUDE.md rule requires naming the path).

## Failure handling

- Quota/auth error: `CONTEXT7_API_KEY` is already in the runtime environment; if it is
  missing or rejected, REPORT that in consensus and stop — never silently fall back to
  training-data guesses for API surfaces.
- No good library match after 2 attempts: say so and proceed with explicit uncertainty,
  flagging the integration as unverified-against-current-docs.
