---
name: cloudflare-pages-deploy
description: "Deploy a static page (fake-door / offer landing / MVP) to Cloudflare Pages with wrangler and VERIFY it is live. Use for the cheapest willingness-to-pay test on any opportunity — a hosted offer page with a single payment/waitlist CTA — and for any company PRODUCT landing. Company products deploy to Cloudflare, never Vercel, never this host."
---

# Cloudflare Pages deploy (+ verify live)

The company's cheapest WTP test (per `PROJECT_EVALUATION_FRAMEWORK.md`) is a **fake-door
landing page** on Cloudflare Pages: one clear offer, one price, one CTA (pay / join
waitlist / book a call). This skill authors that page and ships it to a free, instant
`*.pages.dev` URL — then proves it actually works before anyone calls it live.

Grounded in current wrangler docs (Context7 `/cloudflare/workers-sdk`).

## Prerequisites

- `CLOUDFLARE_API_TOKEN` in the env (deploy-scoped). If it's missing, deployment is **not
  provisioned** — surface that in `consensus.md` and stop; do NOT fall back to another host.
- `wrangler` via `npx` (no global install needed).
- Optional: `CLOUDFLARE_ACCOUNT_ID` (only if the token maps to more than one account).

## Steps

1. **Build the page.** Create a project dir under `projects/<name>/` with a `public/`
   folder holding a self-contained `index.html` (inline CSS; embed assets as data URIs —
   no external CDNs). The frontend-design skill applies here. It must state the offer,
   the price, and exactly ONE primary CTA. A fake-door CTA records intent (email capture
   or a payment link) — never charge without the paid-validation gate the directive sets.

2. **Deploy the static directory to Pages:**
   ```bash
   cd projects/<name>
   npx wrangler pages deploy public \
     --project-name=<project> \
     --branch=main \
     --commit-dirty=true
   ```
   - `--branch=main` makes it a **production** deployment (the stable `<project>.pages.dev`
     URL). Any other branch name produces a preview-hash URL — do not report those as live.
   - First run creates the project; later runs redeploy it.
   - On success wrangler prints: `✨ Deployment complete! Take a peek over at
     https://<hash>.<project>.pages.dev`.

3. **VERIFY live before claiming anything.** A created project or a deployment record is
   NOT proof. Fetch the **production** URL (not the preview hash):
   ```bash
   curl -sS -o /dev/null -w "%{http_code}" https://<project>.pages.dev
   ```
   Expect **HTTP 200** and then confirm the expected offer text is in the body
   (`curl -s https://<project>.pages.dev | grep -F "<your headline>"`).
   - New `*.pages.dev` TLS certs can take a few minutes — if it 5xx/handshake-fails right
     after deploy, wait and re-check. Report the true status ("deployed, cert still
     provisioning"), never overstate.

4. **Record it.** Put the live production URL in `consensus.md` / the relevant docs and
   the Airtable/Linear record for the validation. Inspect recent deployments with
   `npx wrangler pages deployment list --project-name=<project>` if you need history.

## Guardrails

- Products/landing pages → **Cloudflare Pages only**. Not Vercel. Not this company's own
  runtime host (it runs the company and is resource-constrained).
- Never `wrangler delete` / destroy a Pages project (safety guardrail).
- Use the production `<project>.pages.dev` URL in any report, never a preview hash URL.
- Don't claim live until the curl check returns 200 with the expected content.
