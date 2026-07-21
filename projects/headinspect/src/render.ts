// Single-template HTML renderer. No client-side framework, inline CSS.
// Total budget: under ~150 lines including CSS.

import type { InspectReport, HeaderEntry, Category } from "./inspect";

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

export function renderPage(opts: { url?: string; report?: InspectReport; error?: string }): string {
  const body = opts.report
    ? renderReport(opts.report)
    : opts.error
      ? `<p class="error">${escapeHtml(opts.error)}</p>`
      : `<p class="hint">Paste a URL. Get its response headers, grouped and graded.</p>`;

  return `<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<title>HeadInspect${opts.report ? ` — ${escapeHtml(opts.report.url)}` : ""}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
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
</style></head><body><main>
<h1>HeadInspect <small>— response-header inspector</small></h1>
<form method="get" action="/">
  <input type="url" name="url" value="${escapeHtml(opts.url ?? "")}" placeholder="https://example.com" required autofocus>
  <button type="submit">Inspect</button>
</form>
${body}
<footer>
  Also usable as JSON: <code>POST /api/inspect {"url":"..."}</code> or <code>GET /?url=...</code> with <code>Accept: application/json</code>.
  10s timeout, 5 redirects, 1MB cap. HTTPS only. No logging of URLs.
</footer>
</main></body></html>`;
}
