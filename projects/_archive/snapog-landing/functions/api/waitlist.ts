// Cloudflare Pages Function — POST /api/waitlist
// Writes { email, source, ts, ip, ua } to KV.
//
// Founder setup (Cloudflare dashboard, no wrangler CLI needed):
//   1. Pages -> your project -> Settings -> Functions -> KV namespace bindings
//   2. Variable name: WAITLIST
//   3. Create/select a KV namespace (e.g. "snapog-waitlist")
//
// Until WAITLIST is bound the endpoint returns 503 and the client falls back
// to the Formspree endpoint (or the mailto: fallback).

interface Env {
  WAITLIST?: KVNamespace;
}

interface Body {
  email?: unknown;
  source?: unknown;
  ts?: unknown;
}

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export const onRequestPost: PagesFunction<Env> = async (ctx) => {
  const { request, env } = ctx;

  if (!env.WAITLIST) {
    return json({ error: "waitlist_kv_not_bound" }, 503);
  }

  let body: Body;
  try {
    body = await request.json<Body>();
  } catch {
    return json({ error: "bad_json" }, 400);
  }

  const email = typeof body.email === "string" ? body.email.trim().toLowerCase() : "";
  if (!EMAIL_RE.test(email) || email.length > 254) {
    return json({ error: "bad_email" }, 400);
  }

  const source = typeof body.source === "string" ? body.source.slice(0, 40) : "landing";
  const ip = request.headers.get("cf-connecting-ip") ?? "";
  const ua = (request.headers.get("user-agent") ?? "").slice(0, 200);

  const now = new Date().toISOString();
  const key = `email:${email}`;

  const existing = await env.WAITLIST.get(key);
  if (existing) {
    return json({ ok: true, deduped: true });
  }

  await env.WAITLIST.put(
    key,
    JSON.stringify({ email, source, ip, ua, ts: now }),
    { metadata: { source, ts: now } }
  );

  return json({ ok: true });
};

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "content-type": "application/json",
      "cache-control": "no-store",
    },
  });
}
