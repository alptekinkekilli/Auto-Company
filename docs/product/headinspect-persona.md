# HeadInspect — who's pasting the URL, what they need

## The person pasting a URL

Not one persona. Three real moments, all mid-task, all annoyed:

1. A backend engineer fifteen minutes into onboarding a new microservice behind a fresh Nginx reverse proxy. Someone said "CSP is set" but a browser is still logging inline-script violations. They want to know which hop stripped or rewrote the header, and they want it before their standup in twenty minutes.

2. A solo indie dev deploying a static site to a new CDN. Lighthouse just gave them a 62 on Best Practices and flagged missing security headers. They don't know what "Permissions-Policy" is supposed to look like, they just want a checklist that says "add these five, here's a sane starting value."

3. A security-adjacent developer answering a Slack thread — "does example.com actually have HSTS or is the browser just remembering it?" — and they want a screenshot they can paste back in under a minute.

Common shape: someone is already debugging or verifying something specific. They didn't wake up wanting to learn about HTTP. They googled "response header check" because curl -I is fine but the output is unlabeled and their brain is already full.

## What they need to see in the first 5 seconds

The URL they submitted, the final URL after redirects, HTTP status. Then the security grade — a single letter, and next to it the two or three headers that dragged it down, each with the one-line reason. Below that, the full header table grouped by category, headers copyable as plain text, values wrapping instead of truncating. The redirect chain is collapsed by default unless there was more than one hop.

What does not belong on that screen: a score history graph. Nobody visits twice in a row to watch a number move. Also no "share this report" button above the results and no comparison-to-industry-average badge. All noise before the user has read the actual headers.

## What would make them close the tab

Ranked by fatality, most-fatal first:

1. A signup wall or "enter your email to see the full report." Instant back button, and they never return.
2. Response over three seconds with no indication anything is happening. They assume it's broken and try the next Google result.
3. A vague grade — "C, could be better" — with no per-header explanation. Useless as a debugging tool, useless as a checklist.
4. Header names or values that can't be selected and copied. This is a developer tool; copy-paste is the point.
5. Ads, especially interstitials or "recommended tools" sidebars.
6. A JSON pretty-printer dressed up as analysis — echoing the response headers with syntax highlighting and no interpretation. That's what curl already does.

## r/webdev post copy

Title: I got tired of curl -I so I built a response-header inspector

Body:

Paste a URL, get every response header categorized (security, cache, cors, cookie, content), a security grade A–F based on CSP/HSTS/X-Frame-Options/X-Content-Type-Options/Referrer-Policy/Permissions-Policy, one line of commentary per header explaining what it does and whether the value is sane, and the full redirect chain.

Two entry points: paste into the box for the HTML view, or POST to /api/inspect for JSON if you're scripting it. No signup, no cookies, no rate limit beyond the obvious.

Honest limitation: it only inspects the response to a plain GET. It does not follow client-side redirects, does not execute JavaScript, and does not evaluate whether your CSP actually blocks the scripts on your page — only whether the header exists and parses. If you need a real CSP evaluator, use Google's.

URL: [worker-url].workers.dev

Built it because I kept doing `curl -sI | grep -i` and wanted the output grouped and graded.

## What signal to watch in the first 48 hours

Raw hits are the crudest floor: under twenty in the first twenty-four hours means the r/webdev post did not land and no amount of iteration on the tool fixes that — go re-post or move on. The signal that says "useful, not novelty" is repeat inspects on the same hostname within ten minutes of each other; if that happens for more than five percent of sessions, users are debugging a live change and the natural next feature is side-by-side compare of two URLs (or two timestamps of the same URL). API hits to `/api/inspect` above roughly fifteen percent of total traffic means people are scripting against it, which points to a CLI wrapper before a browser extension. Anything below those thresholds, do not build the next feature — sit with what shipped.
