// Header categorization, per-header commentary, and security grading.
// Pure functions — no I/O, no fetch, no Worker globals.

export type Category =
  | "security"
  | "cache"
  | "content"
  | "compat"
  | "cors"
  | "cookie"
  | "other";

export interface HeaderEntry {
  name: string;      // lowercase canonical name
  value: string;     // raw value; for set-cookie this is a summary string
  category: Category;
  note: string;      // one-line commentary
  ok: boolean;       // rough sanity: true if present-and-reasonable
}

export interface RedirectHop {
  status: number;
  from: string;
  to: string;
}

export interface Grade {
  letter: "A" | "B" | "C" | "D" | "F";
  score: number;      // 0..100
  reasons: string[];  // human-readable positives/negatives
}

export interface InspectReport {
  url: string;              // final URL after redirects
  requestedUrl: string;     // original URL user supplied
  status: number;
  redirects: RedirectHop[];
  headers: HeaderEntry[];
  grade: Grade;
  fetchedAt: string;        // ISO
  elapsedMs: number;
}

// ---------- categorization ---------------------------------------------------

const SECURITY = new Set([
  "content-security-policy",
  "content-security-policy-report-only",
  "strict-transport-security",
  "x-frame-options",
  "x-content-type-options",
  "referrer-policy",
  "permissions-policy",
  "cross-origin-opener-policy",
  "cross-origin-embedder-policy",
  "cross-origin-resource-policy",
]);

const CACHE = new Set([
  "cache-control",
  "etag",
  "expires",
  "last-modified",
  "vary",
  "age",
  "pragma",
]);

const CONTENT = new Set([
  "content-type",
  "content-encoding",
  "content-length",
  "content-language",
  "content-disposition",
]);

const COMPAT = new Set([
  "x-powered-by",
  "server",
  "x-aspnet-version",
  "x-aspnetmvc-version",
  "x-generator",
  "x-drupal-cache",
]);

function categorize(name: string): Category {
  const n = name.toLowerCase();
  if (SECURITY.has(n)) return "security";
  if (CACHE.has(n)) return "cache";
  if (CONTENT.has(n)) return "content";
  if (COMPAT.has(n)) return "compat";
  if (n.startsWith("access-control-")) return "cors";
  if (n === "set-cookie" || n === "cookie") return "cookie";
  return "other";
}

// ---------- per-header commentary + sanity -----------------------------------

interface HeaderJudgement {
  note: string;
  ok: boolean;
}

function judge(name: string, value: string): HeaderJudgement {
  const n = name.toLowerCase();
  const v = value.trim();

  switch (n) {
    case "content-security-policy": {
      const bad = /unsafe-inline|unsafe-eval|\*\s*(;|$)/i.test(v);
      return {
        note: bad
          ? "CSP present but permissive (unsafe-inline / unsafe-eval / wildcards)."
          : "CSP present. Restricts sources for scripts, styles, and other resources.",
        ok: !bad,
      };
    }
    case "content-security-policy-report-only":
      return { note: "CSP in report-only mode. Violations logged, not blocked.", ok: false };
    case "strict-transport-security": {
      const m = v.match(/max-age\s*=\s*(\d+)/i);
      const age = m ? parseInt(m[1]!, 10) : 0;
      const includeSub = /includesubdomains/i.test(v);
      const preload = /preload/i.test(v);
      const okAge = age >= 15552000; // 180 days, browser preload minimum
      return {
        note: `HSTS max-age=${age}${includeSub ? ", includeSubDomains" : ""}${preload ? ", preload" : ""}. ${okAge ? "Age acceptable." : "Age below 180d — browsers may not preload."}`,
        ok: okAge,
      };
    }
    case "x-frame-options": {
      const ok = /^(deny|sameorigin)$/i.test(v);
      return {
        note: ok ? `Framing restricted (${v}). Clickjacking mitigated.` : `Unrecognized X-Frame-Options value (${v}).`,
        ok,
      };
    }
    case "x-content-type-options": {
      const ok = /nosniff/i.test(v);
      return {
        note: ok ? "MIME sniffing disabled." : "X-Content-Type-Options present but not 'nosniff'.",
        ok,
      };
    }
    case "referrer-policy": {
      const strict = /(no-referrer|same-origin|strict-origin|strict-origin-when-cross-origin)/i.test(v);
      return {
        note: strict ? `Referrer policy is conservative (${v}).` : `Referrer policy is permissive (${v}). Consider strict-origin-when-cross-origin.`,
        ok: strict,
      };
    }
    case "permissions-policy":
      return { note: "Permissions-Policy present. Restricts browser feature access.", ok: true };
    case "cross-origin-opener-policy":
      return { note: `COOP set (${v}). Isolates browsing context.`, ok: /same-origin/i.test(v) };
    case "cross-origin-embedder-policy":
      return { note: `COEP set (${v}).`, ok: /require-corp|credentialless/i.test(v) };
    case "cross-origin-resource-policy":
      return { note: `CORP set (${v}).`, ok: true };

    case "cache-control":
      return { note: `Cache directives: ${v}.`, ok: true };
    case "etag":
      return { note: "ETag present. Enables conditional requests.", ok: true };
    case "expires":
      return { note: `Expires: ${v}. Prefer Cache-Control max-age in new code.`, ok: true };
    case "last-modified":
      return { note: "Last-Modified present. Enables If-Modified-Since.", ok: true };
    case "vary":
      return { note: `Vary: ${v}. Downstream caches key on these headers.`, ok: true };
    case "age":
      return { note: `Served from a shared cache (age=${v}s).`, ok: true };
    case "pragma":
      return { note: "Pragma is HTTP/1.0 legacy. Cache-Control supersedes it.", ok: false };

    case "content-type":
      return { note: `MIME type ${v}.${/charset=/i.test(v) ? "" : " No charset — assume UTF-8 at your peril."}`, ok: true };
    case "content-encoding": {
      const modern = /(br|zstd|gzip)/i.test(v);
      return { note: `Encoded with ${v}.${modern ? "" : " Consider br or gzip."}`, ok: modern };
    }
    case "content-length":
      return { note: `${v} bytes.`, ok: true };
    case "content-language":
      return { note: `Language declared as ${v}.`, ok: true };
    case "content-disposition":
      return { note: `Disposition: ${v}.`, ok: true };

    case "x-powered-by":
    case "server":
    case "x-aspnet-version":
    case "x-aspnetmvc-version":
    case "x-generator":
    case "x-drupal-cache":
      return {
        note: `Reveals server implementation (${v}). Consider suppressing for reduced fingerprinting.`,
        ok: false,
      };

    case "set-cookie":
      // value here is our summary string, not raw cookie data.
      return { note: value, ok: /Secure/i.test(value) && /HttpOnly/i.test(value) };
  }

  if (n.startsWith("access-control-")) {
    if (n === "access-control-allow-origin" && v === "*") {
      return { note: "Wildcard CORS origin — public read.", ok: true };
    }
    return { note: `CORS directive: ${v}.`, ok: true };
  }

  return { note: "", ok: true };
}

// ---------- Set-Cookie summariser (privacy: never surface raw values) --------

export function summarizeSetCookies(rawJoined: string): string | null {
  if (!rawJoined) return null;
  // Cloudflare's Headers.get("set-cookie") joins multiple cookies with ", "
  // which is ambiguous vs. Expires date commas. Best-effort split on the
  // pattern ", <name>=" to count cookies.
  const parts = rawJoined.split(/,(?=\s*[^=,;\s]+=)/);
  const count = parts.length;
  let secure = 0, httpOnly = 0, sameSite = 0;
  for (const p of parts) {
    if (/;\s*Secure/i.test(p) || /^\s*Secure\b/i.test(p)) secure++;
    if (/;\s*HttpOnly/i.test(p) || /^\s*HttpOnly\b/i.test(p)) httpOnly++;
    if (/;\s*SameSite=/i.test(p)) sameSite++;
  }
  return `${count} cookie(s) set. Secure: ${secure}/${count}. HttpOnly: ${httpOnly}/${count}. SameSite: ${sameSite}/${count}.`;
}

// ---------- headers → HeaderEntry[] ------------------------------------------

export function categorizeHeaders(headers: Headers): HeaderEntry[] {
  const seen = new Set<string>();
  const out: HeaderEntry[] = [];

  headers.forEach((value, name) => {
    const lower = name.toLowerCase();
    if (seen.has(lower)) return;
    seen.add(lower);

    if (lower === "set-cookie") {
      const summary = summarizeSetCookies(value) ?? "";
      const j = judge(lower, summary);
      out.push({ name: lower, value: summary, category: "cookie", note: j.note, ok: j.ok });
      return;
    }

    const j = judge(lower, value);
    out.push({
      name: lower,
      value,
      category: categorize(lower),
      note: j.note,
      ok: j.ok,
    });
  });

  // Deterministic order: security → cache → content → cors → cookie → compat → other,
  // alphabetical inside each bucket.
  const order: Category[] = ["security", "cache", "content", "cors", "cookie", "compat", "other"];
  out.sort((a, b) => {
    const ca = order.indexOf(a.category);
    const cb = order.indexOf(b.category);
    if (ca !== cb) return ca - cb;
    return a.name.localeCompare(b.name);
  });
  return out;
}

// ---------- grading ----------------------------------------------------------

export function grade(entries: HeaderEntry[]): Grade {
  const byName = new Map(entries.map((e) => [e.name, e]));
  const has = (n: string) => byName.has(n);
  const good = (n: string) => byName.get(n)?.ok === true;

  const reasons: string[] = [];
  let score = 0;

  // Presence + soundness weights (total 100).
  // HSTS 25, CSP 25, X-Content-Type-Options 10, X-Frame-Options 10,
  // Referrer-Policy 10, Permissions-Policy 10, COOP/CORP/COEP 5,
  // Penalties: X-Powered-By/Server -5 each (min 0), CSP present-but-permissive -10.

  if (has("strict-transport-security")) {
    if (good("strict-transport-security")) {
      score += 25;
      reasons.push("HSTS present with adequate max-age.");
    } else {
      score += 15;
      reasons.push("HSTS present but max-age below preload threshold.");
    }
  } else {
    reasons.push("HSTS missing.");
  }

  if (has("content-security-policy")) {
    if (good("content-security-policy")) {
      score += 25;
      reasons.push("CSP present and reasonably strict.");
    } else {
      score += 10;
      reasons.push("CSP present but permissive (unsafe-inline / wildcards).");
    }
  } else if (has("content-security-policy-report-only")) {
    score += 5;
    reasons.push("CSP is report-only — not enforced.");
  } else {
    reasons.push("CSP missing.");
  }

  if (good("x-content-type-options")) { score += 10; reasons.push("MIME sniffing disabled."); }
  else reasons.push("X-Content-Type-Options: nosniff missing.");

  if (good("x-frame-options")) { score += 10; reasons.push("Framing restricted."); }
  else reasons.push("X-Frame-Options missing or invalid.");

  if (good("referrer-policy")) { score += 10; reasons.push("Referrer-Policy is conservative."); }
  else reasons.push("Referrer-Policy missing or permissive.");

  if (has("permissions-policy")) { score += 10; reasons.push("Permissions-Policy present."); }
  else reasons.push("Permissions-Policy missing.");

  if (has("cross-origin-opener-policy") || has("cross-origin-resource-policy") || has("cross-origin-embedder-policy")) {
    score += 5;
    reasons.push("Cross-origin isolation headers present.");
  }

  for (const leak of ["x-powered-by", "server", "x-aspnet-version"]) {
    if (has(leak)) {
      score = Math.max(0, score - 5);
      reasons.push(`Fingerprint leak: ${leak}.`);
    }
  }

  score = Math.max(0, Math.min(100, score));

  // Letter with a hard floor from CSP soundness: missing CSP caps at C.
  let letter: Grade["letter"];
  if (score >= 90) letter = "A";
  else if (score >= 75) letter = "B";
  else if (score >= 55) letter = "C";
  else if (score >= 35) letter = "D";
  else letter = "F";

  // Hard cap: missing enforced CSP cannot earn better than C, no matter the score.
  if (!has("content-security-policy") && (letter === "A" || letter === "B")) {
    letter = "C";
    reasons.push("Grade capped at C — no enforced CSP.");
  }

  return { letter, score, reasons };
}
