// HeadInspect — response-header inspector on Cloudflare Workers.
// Routes:
//   GET  /            → HTML report (or empty form if no ?url=)
//   GET  /health      → JSON health probe
//   GET  /api/inspect → JSON, url via ?url= or Accept: application/json GET on /
//   POST /api/inspect → JSON, url via {"url":"..."} body
// CORS: Access-Control-Allow-Origin: * on /api/*.

import { categorizeHeaders, grade, type InspectReport, type RedirectHop } from "./inspect";
import { renderPage, renderBadge } from "./render";

const FETCH_TIMEOUT_MS = 10_000;
const MAX_REDIRECTS = 5;
const MAX_READ_BYTES = 1_000_000;

const CORS_HEADERS: Record<string, string> = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET, POST, OPTIONS",
  "access-control-allow-headers": "content-type",
  "access-control-max-age": "86400",
};

export default {
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    if (url.pathname === "/health") {
      return json({ ok: true, service: "headinspect", ts: new Date().toISOString() });
    }

    if (url.pathname === "/api/inspect") {
      const target = await extractTarget(request, url);
      if (!target.ok) return json({ error: target.error }, 400);
      const result = await inspect(target.url);
      if (!result.ok) return json({ error: result.error }, result.status ?? 502);
      return json(result.report);
    }

    if (url.pathname === "/badge.svg") {
      const qUrl = url.searchParams.get("url");
      if (!qUrl) return svg(renderBadge({ letter: "error", message: "missing url" }));
      const parsed = validateUrl(qUrl);
      if (!parsed.ok) return svg(renderBadge({ letter: "error", message: "invalid url" }));
      const result = await inspect(parsed.url);
      if (!result.ok) return svg(renderBadge({ letter: "error", message: "fetch failed" }));
      return svg(renderBadge({ letter: result.report.grade.letter, score: result.report.grade.score }));
    }

    if (url.pathname === "/") {
      const qUrl = url.searchParams.get("url");
      const wantsJson = (request.headers.get("accept") ?? "").includes("application/json");

      if (!qUrl) {
        return wantsJson
          ? json({ error: "missing ?url=" }, 400)
          : html(renderPage({ origin: url.origin }));
      }

      const parsed = validateUrl(qUrl);
      if (!parsed.ok) {
        return wantsJson
          ? json({ error: parsed.error }, 400)
          : html(renderPage({ origin: url.origin, url: qUrl, error: parsed.error }), 400);
      }

      const result = await inspect(parsed.url);
      if (!result.ok) {
        return wantsJson
          ? json({ error: result.error }, result.status ?? 502)
          : html(renderPage({ origin: url.origin, url: qUrl, error: result.error }), result.status ?? 502);
      }

      return wantsJson
        ? json(result.report)
        : html(renderPage({ origin: url.origin, url: qUrl, report: result.report }));
    }

    return new Response("not found", { status: 404 });
  },
};

// ---------- request-target extraction ---------------------------------------

type TargetOk = { ok: true; url: string };
type TargetErr = { ok: false; error: string };

async function extractTarget(request: Request, url: URL): Promise<TargetOk | TargetErr> {
  let raw: string | null = url.searchParams.get("url");
  if (!raw && request.method === "POST") {
    try {
      const body = (await request.json()) as { url?: unknown };
      if (typeof body?.url === "string") raw = body.url;
    } catch {
      return { ok: false, error: "invalid JSON body" };
    }
  }
  if (!raw) return { ok: false, error: "missing 'url'" };
  const v = validateUrl(raw);
  return v;
}

// ---------- URL validation + SSRF filter -------------------------------------

function validateUrl(raw: string): TargetOk | TargetErr {
  let u: URL;
  try {
    u = new URL(raw);
  } catch {
    return { ok: false, error: "not a valid URL" };
  }
  if (u.protocol !== "https:") return { ok: false, error: "only https:// URLs are accepted" };
  if (!u.hostname) return { ok: false, error: "missing hostname" };
  if (isBlockedHost(u.hostname)) return { ok: false, error: "hostname resolves to a blocked address range" };
  return { ok: true, url: u.toString() };
}

function isBlockedHost(host: string): boolean {
  const h = host.toLowerCase();
  if (h === "localhost" || h.endsWith(".localhost")) return true;
  if (h === "metadata.google.internal") return true;

  // IPv4 literal?
  const m = h.match(/^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/);
  if (m) {
    const [a, b] = [parseInt(m[1]!, 10), parseInt(m[2]!, 10)];
    if (a === 10) return true;                         // 10.0.0.0/8
    if (a === 127) return true;                        // loopback
    if (a === 0) return true;                          // 0.0.0.0/8
    if (a === 169 && b === 254) return true;           // link-local + metadata
    if (a === 172 && b >= 16 && b <= 31) return true;  // 172.16.0.0/12
    if (a === 192 && b === 168) return true;           // 192.168.0.0/16
    if (a >= 224) return true;                         // multicast / reserved
    return false;
  }
  // IPv6 literal? Block loopback + link-local + ULA outright.
  if (h.startsWith("[") && h.endsWith("]")) {
    const v6 = h.slice(1, -1).toLowerCase();
    if (v6 === "::1" || v6 === "::") return true;
    if (v6.startsWith("fe80:") || v6.startsWith("fc") || v6.startsWith("fd")) return true;
    return false;
  }
  return false;
}

// ---------- inspection core --------------------------------------------------

type InspectOk = { ok: true; report: InspectReport };
type InspectErr = { ok: false; error: string; status?: number };

async function inspect(startUrl: string): Promise<InspectOk | InspectErr> {
  const started = Date.now();
  const redirects: RedirectHop[] = [];
  let current = startUrl;
  let finalResp: Response | null = null;

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);

  try {
    for (let hop = 0; hop <= MAX_REDIRECTS; hop++) {
      const resp = await fetch(current, {
        method: "GET",
        redirect: "manual",
        signal: controller.signal,
        headers: { "user-agent": "HeadInspect/0.1 (+https://headinspect.workers.dev)" },
      });

      // 3xx with Location → record + follow (up to cap).
      const loc = resp.headers.get("location");
      if (resp.status >= 300 && resp.status < 400 && loc) {
        let next: string;
        try {
          next = new URL(loc, current).toString();
        } catch {
          finalResp = resp;
          break;
        }
        const nextParsed = validateUrl(next);
        if (!nextParsed.ok) {
          clearTimeout(timer);
          return { ok: false, error: `redirect target rejected: ${nextParsed.error}`, status: 400 };
        }
        redirects.push({ status: resp.status, from: current, to: next });
        current = nextParsed.url;

        // Drain body to release the socket before re-fetching.
        await consume(resp, MAX_READ_BYTES);

        if (hop === MAX_REDIRECTS) {
          clearTimeout(timer);
          return { ok: false, error: `too many redirects (>${MAX_REDIRECTS})`, status: 508 };
        }
        continue;
      }

      finalResp = resp;
      await consume(resp, MAX_READ_BYTES);
      break;
    }
  } catch (err: unknown) {
    clearTimeout(timer);
    if (err instanceof Error && err.name === "AbortError") {
      return { ok: false, error: `fetch timed out after ${FETCH_TIMEOUT_MS}ms`, status: 504 };
    }
    return { ok: false, error: err instanceof Error ? err.message : "fetch failed", status: 502 };
  }

  clearTimeout(timer);
  if (!finalResp) return { ok: false, error: "no response captured", status: 502 };

  const entries = categorizeHeaders(finalResp.headers);
  const g = grade(entries);

  const report: InspectReport = {
    url: current,
    requestedUrl: startUrl,
    status: finalResp.status,
    redirects,
    headers: entries,
    grade: g,
    fetchedAt: new Date().toISOString(),
    elapsedMs: Date.now() - started,
  };
  return { ok: true, report };
}

// Drain up to `cap` bytes from the response body so the fetch can complete.
async function consume(resp: Response, cap: number): Promise<void> {
  if (!resp.body) return;
  const reader = resp.body.getReader();
  let read = 0;
  try {
    while (read < cap) {
      const { done, value } = await reader.read();
      if (done) break;
      read += value.byteLength;
    }
    await reader.cancel();
  } catch {
    // best-effort; we already have the headers
  }
}

// ---------- response helpers -------------------------------------------------

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body, null, 2), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      ...CORS_HEADERS,
    },
  });
}

function html(body: string, status = 200): Response {
  return new Response(body, {
    status,
    headers: {
      "content-type": "text/html; charset=utf-8",
      "cache-control": "no-store",
      "x-content-type-options": "nosniff",
      "referrer-policy": "strict-origin-when-cross-origin",
    },
  });
}

// Always 200 so README embeds never render a broken image. Edge-cached 5min
// (GitHub camo will layer its own cache on top).
function svg(body: string): Response {
  return new Response(body, {
    status: 200,
    headers: {
      "content-type": "image/svg+xml; charset=utf-8",
      "cache-control": "public, max-age=300, s-maxage=300",
      ...CORS_HEADERS,
    },
  });
}
