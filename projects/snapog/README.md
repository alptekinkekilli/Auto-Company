# SnapOG

Generate stunning Open Graph images via API — hosted on Cloudflare Workers, cached globally on R2, sub-100ms on cache hit.

## Quick Start

```bash
# Get a free API key at https://snapog.dev/register, then:
curl "https://snapog.dev/og?title=My+Blog+Post&domain=myblog.com&key=sk_YOUR_KEY" \
  --output og.png && open og.png
```

## API

```
GET /og
  ?title=Your Page Title     # required, max 120 chars
  &key=sk_your_key           # required
  &description=Subtitle      # optional, max 200 chars
  &domain=yourdomain.com     # optional
  &author=Jane Doe           # optional
  &tag=Tutorial              # optional, shown as pill badge
  &template=default          # default | blog | article
  &theme=dark                # dark | light
```

Returns `image/png`, 1200×630.

Headers:
- `X-Cache: HIT|MISS` — whether served from R2 cache
- `X-SnapOG-Tier: free|pro|business`

## HTML Integration

```html
<meta property="og:image"
      content="https://snapog.dev/og?title=YOUR_TITLE&key=YOUR_KEY" />
<meta property="og:image:width"  content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card"   content="summary_large_image" />
<meta name="twitter:image"  content="https://snapog.dev/og?title=YOUR_TITLE&key=YOUR_KEY" />
```

## Pricing

| Tier | Price | Images/month |
|------|-------|-------------|
| Free | $0 | 100 |
| Pro | $19/mo | 10,000 |
| Business | $49/mo | 100,000 |

Free tier images include "snapog.dev" watermark.

## Local Development

### Prerequisites
- Node.js 18+, npm
- Wrangler (`npm install -g wrangler`)
- A Cloudflare account with Workers access

### Setup

```bash
cd projects/snapog
npm install

# 1. Create D1 database
wrangler d1 create snapog-db
# Copy the returned database_id into wrangler.toml [d1_databases]

# 2. Apply migrations locally
npm run db:local

# 3. Create R2 bucket (local R2 is simulated)
# No setup needed for local dev — wrangler simulates R2

# 4. Start dev server
npm run dev
```

Open http://127.0.0.1:8787

### Test

```bash
# Register a key via browser at http://127.0.0.1:8787/register
# Then test with:
API_KEY=sk_your_key bash sample/smoke-test.sh

# Or direct curl:
curl "http://127.0.0.1:8787/og?title=Hello+World&key=sk_your_key" --output og.png
```

### Typecheck

```bash
npm run typecheck
```

## Deployment

### One-time bootstrap (local, founder-run)

```bash
# 1. Authenticate wrangler with Cloudflare
wrangler login

# 2. Create remote D1 database, paste UUID into wrangler.toml [d1_databases]
wrangler d1 create snapog-db

# 3. Create R2 bucket
wrangler r2 bucket create snapog-og-cache

# 4. Commit the updated wrangler.toml
git add wrangler.toml && git commit -m "chore(snapog): wire live D1 database_id"
```

### CI/CD (recurring)

After bootstrap, deploys are handled by GitHub Actions —
`.github/workflows/snapog-deploy.yml`. Trigger via the **Actions** tab
(`workflow_dispatch` → pick `staging` or `production`). The job:

1. Verifies `wrangler.toml` no longer has the `REPLACE_WITH_...` placeholder.
2. Verifies required repo secrets are set.
3. Type-checks.
4. Applies D1 migrations (`--remote`).
5. Runs `wrangler deploy`.
6. Smoke-tests `GET /health` on the returned worker URL (5 retries, 3s backoff).

**Required repo secrets** (Settings → Secrets and variables → Actions):

| Secret | Where to get it |
|--------|-----------------|
| `CLOUDFLARE_API_TOKEN` | Cloudflare dashboard → My Profile → API Tokens → Create Token. Needs `Workers Scripts:Edit`, `D1:Edit`, `R2:Edit`, `Account Settings:Read` scopes. |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare dashboard → any Workers page, right sidebar (32-char hex). |

Every PR touching `projects/snapog/**` also runs `snapog-ci` (typecheck +
wrangler config sanity) — no secrets required.

### Manual deploy (fallback)

```bash
npm run db:remote
wrangler deploy
```

## Tech Stack

- [Cloudflare Workers](https://workers.cloudflare.com/) — edge compute
- [Hono](https://hono.dev/) — HTTP framework
- [workers-og](https://github.com/nicholasgasior/workers-og) — OG image generation (Satori-based)
- [Cloudflare D1](https://developers.cloudflare.com/d1/) — SQLite for usage tracking
- [Cloudflare R2](https://developers.cloudflare.com/r2/) — image cache storage
