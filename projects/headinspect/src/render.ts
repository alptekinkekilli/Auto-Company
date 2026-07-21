// Single-template HTML renderer. No client-side framework, inline CSS.
// Total budget: under ~150 lines including CSS.

import type { InspectReport, HeaderEntry, Category, Grade } from "./inspect";

const CATEGORY_LABEL: Record<Category, string> = {
  security: "Security",
  cache: "Cache",
  content: "Content",
  cors: "CORS",
  cookie: "Cookies",
  compat: "Compat / Legacy",
  other: "Other",
};

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

// ---------- badge ------------------------------------------------------------

function badgeColor(letter: Grade["letter"] | "error"): string {
  switch (letter) {
    case "A": return "#4c1";
    case "B": return "#97ca00";
    case "C": return "#dfb317";
    case "D": return "#fe7d37";
    case "F": return "#e05d44";
    default:  return "#9f9f9f";
  }
}

// Rough 11px Verdana metrics — good enough for our fixed slugs.
function textWidth(s: string): number {
  return s.length * 6.5;
}

// shields.io-flavoured flat SVG. Uses textLength to stretch text to the
// pre-computed slug width so the render is stable across clients that
// substitute the font.
export function renderBadge(opts: { letter: Grade["letter"] | "error"; score?: number; label?: string; message?: string }): string {
  const label = opts.label ?? "headinspect";
  const message = opts.message ?? (opts.letter === "error" ? "error" : `${opts.letter} ${opts.score ?? 0}/100`);
  const color = badgeColor(opts.letter);

  const padL = 12; // 6px each side
  const padR = 12;
  const labelW = Math.round(textWidth(label) + padL);
  const messageW = Math.round(textWidth(message) + padR);
  const total = labelW + messageW;

  // Center-x for each label, scaled 10x for textLength.
  const labelCX10 = labelW * 5;
  const messageCX10 = (labelW * 2 + messageW) * 5;
  const labelTL10 = (labelW - padL) * 10;
  const messageTL10 = (messageW - padR) * 10;

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${total}" height="20" role="img" aria-label="${escapeHtml(label)}: ${escapeHtml(message)}">
<title>${escapeHtml(label)}: ${escapeHtml(message)}</title>
<linearGradient id="s" x2="0" y2="100%"><stop offset="0" stop-color="#bbb" stop-opacity=".1"/><stop offset="1" stop-opacity=".1"/></linearGradient>
<clipPath id="r"><rect width="${total}" height="20" rx="3" fill="#fff"/></clipPath>
<g clip-path="url(#r)">
<rect width="${labelW}" height="20" fill="#555"/>
<rect x="${labelW}" width="${messageW}" height="20" fill="${color}"/>
<rect width="${total}" height="20" fill="url(#s)"/>
</g>
<g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="110">
<text aria-hidden="true" x="${labelCX10}" y="150" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="${labelTL10}">${escapeHtml(label)}</text>
<text x="${labelCX10}" y="140" transform="scale(.1)" textLength="${labelTL10}">${escapeHtml(label)}</text>
<text aria-hidden="true" x="${messageCX10}" y="150" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="${messageTL10}">${escapeHtml(message)}</text>
<text x="${messageCX10}" y="140" transform="scale(.1)" textLength="${messageTL10}">${escapeHtml(message)}</text>
</g>
</svg>`;
}

function renderEmbedBlock(origin: string, requestedUrl: string): string {
  const badgeUrl = `${origin}/badge.svg?url=${encodeURIComponent(requestedUrl)}`;
  const reportUrl = `${origin}/?url=${encodeURIComponent(requestedUrl)}`;
  const md = `[![HeadInspect](${badgeUrl})](${reportUrl})`;
  const htmlSnippet = `<a href="${reportUrl}"><img src="${badgeUrl}" alt="HeadInspect grade"></a>`;
  return `<section class="embed"><h3>Embed a live badge</h3>
<img src="${escapeHtml(badgeUrl)}" alt="live grade badge" class="live-badge" width="140" height="20">
<label>Markdown</label>
<textarea readonly onclick="this.select()" rows="1">${escapeHtml(md)}</textarea>
<label>HTML</label>
<textarea readonly onclick="this.select()" rows="1">${escapeHtml(htmlSnippet)}</textarea>
<p class="hint small">Regrades on each render (edge-cached 5min). Drop it in a README to show your headers score.</p>
</section>`;
}

function renderReport(report: InspectReport): string {
  const groups = new Map<Category, HeaderEntry[]>();
  for (const h of report.headers) {
    const arr = groups.get(h.category) ?? [];
    arr.push(h);
    groups.set(h.category, arr);
  }
  const order: Category[] = ["security", "cache", "content", "cors", "cookie", "compat", "other"];

  const groupHtml = order
    .filter((c) => groups.has(c))
    .map((c) => {
      const rows = groups.get(c)!.map((h) => `
        <tr>
          <td class="hname">${escapeHtml(h.name)}</td>
          <td class="hval">${escapeHtml(h.value).slice(0, 400)}</td>
          <td class="hnote ${h.ok ? "ok" : "warn"}">${escapeHtml(h.note)}</td>
        </tr>`).join("");
      return `<section><h3>${CATEGORY_LABEL[c]}</h3><table>${rows}</table></section>`;
    }).join("");

  const redirects = report.redirects.length
    ? `<section><h3>Redirects</h3><ol>${report.redirects.map(r =>
        `<li>${r.status} — ${escapeHtml(r.from)} → ${escapeHtml(r.to)}</li>`).join("")}</ol></section>`
    : "";

  const reasons = report.grade.reasons.map(r => `<li>${escapeHtml(r)}</li>`).join("");

  return `
  <div class="report">
    <div class="summary">
      <div class="grade grade-${report.grade.letter}">${report.grade.letter}<small>${report.grade.score}/100</small></div>
      <div class="meta">
        <div><strong>URL</strong> <code>${escapeHtml(report.url)}</code></div>
        <div><strong>Status</strong> ${report.status} · <strong>Fetched in</strong> ${report.elapsedMs}ms</div>
      </div>
    </div>
    <ul class="reasons">${reasons}</ul>
    ${redirects}
    ${groupHtml}
  </div>`;
}

function hostOf(u: string): string {
  try { return new URL(u).hostname; } catch { return u; }
}

function socialMeta(opts: { origin: string; url?: string; report?: InspectReport; error?: string }): string {
  const site = "HeadInspect";
  const defaultDesc = "Paste a URL. Get its response headers, grouped and graded.";
  const canonical = opts.origin + (opts.url ? `/?url=${encodeURIComponent(opts.url)}` : "/");

  let title = `${site} — response-header inspector`;
  let desc = defaultDesc;

  if (opts.report) {
    const host = hostOf(opts.report.url);
    title = `${host} scored ${opts.report.grade.letter} (${opts.report.grade.score}/100) — ${site}`;
    const top = opts.report.grade.reasons.slice(0, 2)
      .map((r) => r.replace(/[.。]+$/, ""))
      .join(". ");
    desc = top
      ? `${host}: ${opts.report.grade.letter} ${opts.report.grade.score}/100. ${top}.`
      : `${host}: ${opts.report.grade.letter} ${opts.report.grade.score}/100. ${defaultDesc}`;
  } else if (opts.error) {
    desc = `Error: ${opts.error}`;
  }

  return [
    `<link rel="canonical" href="${escapeHtml(canonical)}">`,
    `<meta name="description" content="${escapeHtml(desc)}">`,
    `<meta property="og:type" content="website">`,
    `<meta property="og:site_name" content="${site}">`,
    `<meta property="og:title" content="${escapeHtml(title)}">`,
    `<meta property="og:description" content="${escapeHtml(desc)}">`,
    `<meta property="og:url" content="${escapeHtml(canonical)}">`,
    `<meta name="twitter:card" content="summary">`,
    `<meta name="twitter:title" content="${escapeHtml(title)}">`,
    `<meta name="twitter:description" content="${escapeHtml(desc)}">`,
  ].join("\n");
}

export function renderPage(opts: { origin: string; url?: string; report?: InspectReport; error?: string }): string {
  const embed = opts.report ? renderEmbedBlock(opts.origin, opts.report.requestedUrl) : "";
  const body = opts.report
    ? renderReport(opts.report) + embed
    : opts.error
      ? `<p class="error">${escapeHtml(opts.error)}</p>`
      : `<p class="hint">Paste a URL. Get its response headers, grouped and graded.</p>`;

  const titleTag = opts.report
    ? `${hostOf(opts.report.url)} scored ${opts.report.grade.letter} (${opts.report.grade.score}/100) — HeadInspect`
    : "HeadInspect — response-header inspector";

  return `<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<title>${escapeHtml(titleTag)}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
${socialMeta(opts)}
<style>
:root { color-scheme: light dark; --bg:#fafafa; --fg:#111; --mut:#666; --line:#ddd; --ok:#1a7f37; --warn:#b35c00; --err:#a01313; }
@media (prefers-color-scheme: dark){:root{--bg:#0e0e10;--fg:#e6e6e6;--mut:#999;--line:#2a2a2e;--ok:#3fb950;--warn:#d29922;--err:#f85149;}}
html,body{background:var(--bg);color:var(--fg);margin:0;font:14px/1.5 -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;}
main{max-width:920px;margin:0 auto;padding:32px 20px 80px;}
h1{font-size:22px;margin:0 0 4px;letter-spacing:-0.01em;}
h1 small{color:var(--mut);font-weight:400;font-size:14px;}
h3{font-size:13px;text-transform:uppercase;letter-spacing:0.05em;color:var(--mut);border-bottom:1px solid var(--line);padding-bottom:4px;margin:24px 0 8px;}
form{display:flex;gap:8px;margin:16px 0 8px;}
input[type=url]{flex:1;padding:8px 10px;font:14px ui-monospace,SFMono-Regular,Consolas,monospace;background:transparent;color:var(--fg);border:1px solid var(--line);border-radius:4px;}
button{padding:8px 16px;font:14px sans-serif;background:var(--fg);color:var(--bg);border:0;border-radius:4px;cursor:pointer;}
.hint,.error{color:var(--mut);}
.error{color:var(--err);}
.summary{display:flex;gap:16px;align-items:center;margin:16px 0 8px;padding:12px 16px;border:1px solid var(--line);border-radius:6px;}
.grade{font:600 40px/1 ui-monospace,monospace;padding:8px 14px;border-radius:4px;background:var(--fg);color:var(--bg);display:flex;flex-direction:column;align-items:center;}
.grade small{font-size:10px;font-weight:400;letter-spacing:0.05em;margin-top:2px;}
.grade-A{background:var(--ok);color:#fff;} .grade-B{background:#2f6b3a;color:#fff;} .grade-C{background:var(--warn);color:#fff;} .grade-D,.grade-F{background:var(--err);color:#fff;}
.meta code{font:12px ui-monospace,monospace;color:var(--mut);word-break:break-all;}
.reasons{margin:8px 0 0;padding-left:20px;color:var(--mut);font-size:13px;}
table{width:100%;border-collapse:collapse;font-size:13px;}
td{padding:6px 8px;vertical-align:top;border-bottom:1px solid var(--line);}
.hname{font:12px ui-monospace,SFMono-Regular,monospace;color:var(--fg);white-space:nowrap;width:220px;}
.hval{font:12px ui-monospace,monospace;color:var(--mut);word-break:break-all;max-width:340px;}
.hnote{color:var(--mut);}
.hnote.warn{color:var(--warn);}
footer{margin-top:48px;color:var(--mut);font-size:12px;}
footer a{color:inherit;}
ol li{font:12px ui-monospace,monospace;}
.embed{margin-top:24px;}
.embed .live-badge{display:block;margin:8px 0 12px;}
.embed label{display:block;font-size:11px;text-transform:uppercase;letter-spacing:0.05em;color:var(--mut);margin:8px 0 2px;}
.embed textarea{width:100%;padding:6px 8px;font:12px ui-monospace,SFMono-Regular,Consolas,monospace;background:transparent;color:var(--fg);border:1px solid var(--line);border-radius:4px;resize:none;box-sizing:border-box;}
.small{font-size:11px;margin-top:6px;}
</style></head><body><main>
<h1>HeadInspect <small>— response-header inspector</small></h1>
<form method="get" action="/">
  <input type="url" name="url" value="${escapeHtml(opts.url ?? "")}" placeholder="https://example.com" required autofocus>
  <button type="submit">Inspect</button>
</form>
${body}
<footer>
  Also usable as JSON: <code>POST /api/inspect {"url":"..."}</code> or <code>GET /?url=...</code> with <code>Accept: application/json</code>.<br>
  README badge: <code>GET /badge.svg?url=...</code> (SVG, edge-cached 5min).<br>
  10s timeout, 5 redirects, 1MB cap. HTTPS only. No logging of URLs.
</footer>
</main></body></html>`;
}
