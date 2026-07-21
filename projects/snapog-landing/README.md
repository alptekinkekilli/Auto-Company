# SnapOG Landing

Static waitlist page for **snapog.dev**. Ships independently of the SnapOG Worker.

- Single-file HTML/CSS/JS (no build step)
- Inherits the "Carbon Terminal" brand system used by the Worker dashboard
- Waitlist form talks to `/api/waitlist` (Cloudflare Pages Function → KV), with
  a Formspree fallback, with a `mailto:` last-resort so no signup is ever lost

## Why this exists

The SnapOG Worker deploy has been blocked on `wrangler login` for four
consecutive cycles. This page lets us start collecting real intent signal
(the north-star metric requires it) without waiting on Worker auth. When the
Worker ships on the same domain later, its `/og?...` route co-exists cleanly
with this page's `/`.

## Deploy — Cloudflare Pages (no wrangler CLI needed)

1. Push this directory to the GitHub repo (already the case).
2. In the Cloudflare dashboard: **Workers & Pages → Create → Pages → Connect to Git**.
3. Pick the repo. Set:
   - **Production branch:** `main`
   - **Build command:** *(leave blank)*
   - **Build output directory:** `projects/snapog-landing`
4. Save → first deploy runs.
5. Point the custom domain `snapog.dev` at the Pages project (Custom domains → Set up a custom domain).

That's the whole path. It requires **no local `wrangler login`** — everything
happens in the browser. The founder-side blockers (domain registration,
Cloudflare account) still apply, but they were already required for the
Worker deploy.

## Waitlist backend — pick ONE

The submission code tries backends in order and falls through gracefully. You
only need to configure ONE for the form to work.

### Option A — Cloudflare Pages Function + KV (recommended)

The KV namespace already exists — it was created via Cloudflare MCP in
Cycle 11 (2026-07-21). You only need to bind it to the Pages project.

- **Namespace title:** `snapog-waitlist`
- **Namespace ID:** `5a27f50e21424d24b4341aef886c9ce1`

1. Pages project → **Settings → Functions → KV namespace bindings → Add binding**.
2. **Variable name:** `WAITLIST`. **KV namespace:** pick `snapog-waitlist` from
   the dropdown (or paste the ID above).
3. Redeploy (or trigger a rebuild). The `/api/waitlist` endpoint starts
   accepting POSTs immediately.
4. Verify: `curl -X POST https://snapog.dev/api/waitlist -H 'content-type: application/json' -d '{"email":"you@you.com"}'` → `{"ok":true}`.
5. Read the list any time via the Cloudflare KV UI, or:
   ```bash
   npx wrangler kv:key list --namespace-id=5a27f50e21424d24b4341aef886c9ce1 | grep '^email:'
   ```
   (reading requires wrangler login later — the writes work without it)

### Option B — Formspree (zero infra, ~2 min setup)

1. Sign up at https://formspree.io (free tier: 50/month is fine for a waitlist).
2. Create a form → copy the endpoint URL (looks like
   `https://formspree.io/f/xxxxxxxx`).
3. Open `index.html`, search for `<REPLACE_WITH_FORMSPREE_URL>`, replace with
   the endpoint.
4. Redeploy.

### Option C — Do nothing

The form falls back to `mailto:hello@snapog.dev` with the email pre-filled in
the subject and body. Uglier UX; no signups lost.

## Post-launch: wire the pull-quote links

After the three launch essays go live, edit `index.html`:

```bash
sed -i '' 's|<REPLACE_WITH_TEARDOWN_URL>|https://your.blog/teardown-url|' index.html
sed -i '' 's|<REPLACE_WITH_NEXTJS_URL>|https://your.blog/nextjs-url|'   index.html
sed -i '' 's|<REPLACE_WITH_ASTRO_URL>|https://your.blog/astro-url|'    index.html
```

Then push. The three "Read the ..." links auto-unlock and start opening in a
new tab. Until then they render as dim, non-clickable text — the section
still reads correctly, no broken links.

## Local preview

```bash
cd projects/snapog-landing
python3 -m http.server 8000
# open http://localhost:8000
```

The waitlist form falls straight through to the `mailto:` fallback locally
(no `/api/waitlist` endpoint), which is the right behavior for a preview.

## Files

- `index.html` — the page
- `functions/api/waitlist.ts` — Pages Function that writes to KV
- `_headers` — security headers (CSP, HSTS, framing, etc.)
- `robots.txt` — allow everything except `/api/`

## What this page is not

- Not a signup page. There is no `/register`. That comes with the Worker.
- Not a dashboard. That comes with the Worker.
- Not a pricing page. Pricing was intentionally scoped out of the waitlist
  intent — the goal is qualified email addresses, not price shopping.
