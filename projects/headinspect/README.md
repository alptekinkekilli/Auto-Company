# HeadInspect

HTTP response-header inspector on Cloudflare Workers. Paste a URL, get its headers grouped into Security / Cache / Content / CORS / Cookies / Compat / Other, with one-line commentary per header and a security grade.

## Run

```sh
npm install
npx wrangler dev
```

## Deploy

Requires `CLOUDFLARE_API_TOKEN` in the environment, or a prior `npx wrangler login`.

```sh
npx wrangler deploy
```

Deploys to `headinspect.<account>.workers.dev`. No custom domain, no R2, no D1 binding (see `migrations/0001_hits.sql` for the optional counter table).

## API

```sh
# HTML report
curl 'https://headinspect.workers.dev/?url=https://example.com'

# JSON
curl 'https://headinspect.workers.dev/api/inspect?url=https://example.com'

curl -X POST https://headinspect.workers.dev/api/inspect \
  -H 'content-type: application/json' \
  -d '{"url":"https://example.com"}'
```

CORS is open (`*`) on `/api/*` so the endpoint is drop-in usable from dev tools and browser scripts.

## Security-grade rubric

| Signal | Weight | Notes |
|---|---:|---|
| HSTS (`Strict-Transport-Security`) | +25 | Full credit only at `max-age >= 15552000` (180d) |
| CSP (`Content-Security-Policy`) | +25 | -15 if it contains `unsafe-inline`/`unsafe-eval`/wildcards |
| CSP report-only only | +5 | Not enforced, so partial credit |
| `X-Content-Type-Options: nosniff` | +10 | |
| `X-Frame-Options` (DENY/SAMEORIGIN) | +10 | |
| `Referrer-Policy` conservative | +10 | `no-referrer`, `same-origin`, or `strict-origin*` |
| `Permissions-Policy` present | +10 | |
| COOP / COEP / CORP any | +5 | |
| `X-Powered-By`, `Server`, `X-AspNet-Version` present | -5 each | Fingerprint leak |

Letters: A ≥ 90, B ≥ 75, C ≥ 55, D ≥ 35, else F. **Grade capped at C if no enforced CSP.**

## Limits

- HTTPS URLs only. RFC 1918 / loopback / link-local / metadata IPs rejected.
- 10s fetch timeout. Max 5 redirects. Response body reading capped at 1MB.
- Cookie values are never surfaced — only a summary of counts and flags.
