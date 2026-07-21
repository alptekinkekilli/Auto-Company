---
sender: founder@snapog.dev
list: KV `snapog-waitlist` (Cloudflare Workers KV, snapog Worker binding)
send_window: Tuesday 09:00 US-Eastern of launch week
expected_recipients: N (KV read at send-time)
related_files:
  - docs/marketing/launch-content/01-teardown-shipping-og-without-nodejs.md
  - docs/marketing/launch-content/02-howto-nextjs-app-router.md
  - docs/marketing/launch-content/03-howto-astro.md
  - docs/operations/snapog-launch-distribution.md
---

# SnapOG — Waitlist Launch Email

## Subject lines

- **Primary:** `SnapOG is up. Your key is one click away.`
  - Rationale: states the fact, names the product, sets the CTA. No hype verbs. Reads like an ops note, which is on-brand.
- **A/B alt 1:** `An OG image is a <meta> tag. So is SnapOG.`
  - Rationale: leads with the quotable line from the teardown. High curiosity, low corporate. Rewards readers who forgot they signed up.
- **A/B alt 2:** `You signed up for SnapOG. It's live.`
  - Rationale: pure recall trigger for the "who is this?" bucket. Zero cleverness, maximum open rate on a cold-ish list.

## Preheader

`One HTTP GET. One <meta> tag. Free tier covers 100 images a month.`

## Body (HTML-safe plain prose)

Months ago you dropped your email on snapog.dev because I said I was building a Cloudflare-Worker OG image API and asked if that sounded useful. It's live today. If you don't remember signing up, that's fair — the honest version is that it took longer than I told you it would. But it's here now, and you're on this list because you asked to be first.

Here's the whole thing in sixty seconds. Grab a key at `<REPLACE_WITH_LIVE_URL>/register` — no card, free tier is 100 images a month, Pro is $19/month for 10k. Then paste one tag into your `<head>`:

```html
<meta property="og:image"
      content="<REPLACE_WITH_LIVE_URL>/og?title=Your+post+title&domain=yourblog.com&key=sk_YOUR_KEY" />
```

That's it. No Dockerfile. No Satori JSX. No build step. First request renders in under a second, every request after that is a sub-100ms cache hit off R2.

If you have a designer who wants pixel-perfect brand templates, use Bannerbear — I'm not trying to compete with them and I'll say so on Twitter if you ask. SnapOG is for the case where you want an OG image, you have a title, and you're done thinking about it. If that's not you, ignore this email with my blessing. If it is you: reply and tell me what breaks. I read every reply, and the fastest way to shape v1.1 is to be the person whose bug I fixed on day two.

— Alptekin

## Plain-text fallback

```
SnapOG is up. Your key is one click away.

Months ago you dropped your email on snapog.dev because I said I
was building a Cloudflare-Worker OG image API and asked if that
sounded useful. It's live today. If you don't remember signing
up, that's fair -- the honest version is that it took longer
than I told you it would. But it's here now, and you're on this
list because you asked to be first.

Here's the whole thing in sixty seconds. Grab a key at
<REPLACE_WITH_LIVE_URL>/register -- no card, free tier is 100
images a month, Pro is $19/month for 10k. Then paste one tag
into your <head>:

  <meta property="og:image"
        content="<REPLACE_WITH_LIVE_URL>/og?title=Your+post+title&domain=yourblog.com&key=sk_YOUR_KEY" />

That's it. No Dockerfile. No Satori JSX. No build step. First
request renders in under a second, every request after that is
a sub-100ms cache hit off R2.

If you have a designer who wants pixel-perfect brand templates,
use Bannerbear -- I'm not trying to compete with them and I'll
say so on Twitter if you ask. SnapOG is for the case where you
want an OG image, you have a title, and you're done thinking
about it. If that's not you, ignore this email with my blessing.
If it is you: reply and tell me what breaks. I read every reply,
and the fastest way to shape v1.1 is to be the person whose bug
I fixed on day two.

-- Alptekin

Grab a key: <REPLACE_WITH_LIVE_URL>/register
```

## Sender notes

- **Sed before sending:** `sed -i '' 's|<REPLACE_WITH_LIVE_URL>|https://snapog.dev|g' docs/operations/waitlist-launch-email.md` — one replace, four hits (two in the HTML body, two in plain-text). Verify with `grep -c REPLACE` returning 0.
- **Sender-of-choice:** **Buttondown**. Reasoning: list is small (0–100), the email is prose-heavy with one code block, Buttondown's markdown-native editor renders the `<meta>` snippet without escaping gymnastics, and its default `text/plain` MIME part comes out clean. If you don't already have a Buttondown account, don't create one for this — paste the HTML body into whatever transactional sender is already wired to `founder@snapog.dev` (Resend works fine as a fallback; Postmark is overkill for one send).
- **Bounces:** export bounces from the sender after 24h, remove them from the KV waitlist with `wrangler kv:key delete --binding=WAITLIST <email>`. Don't re-send.
- **One blast, not a drip.** List is small and cold — a drip on 60 addresses is theater. Send once, Tuesday 09:00 ET, and move on to distribution (r/webdev "Show and tell" per `docs/operations/snapog-launch-distribution.md`).
- **Reply handling:** the paragraph 3 ask ("reply and tell me what breaks") is load-bearing. Make sure the From address is a real inbox you'll check that day, not `noreply@`.
