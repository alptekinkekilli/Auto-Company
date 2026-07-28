// Branded opt-out URL: https://auto.appricode.tr/listeden-cik?e=<addr>&s=<sig>
//
// This is a PRESENTATION layer only. It proxies to the comms service's /unsubscribe,
// which verifies the HMAC signature and writes the suppression record. There is
// deliberately NO suppression store here: fail-closed only means something when exactly
// one place answers "is this address suppressed?", and a second store that could disagree
// would be a worse guarantee than one store in an unglamorous place.
//
// Why it exists at all: the raw upstream URL is a generic serverless hostname with "dev"
// in it, on a domain unrelated to the rest of the message. For cold B2B mail that reads as
// untrustworthy to both spam filters and people — and an opt-out link nobody dares click
// is not a working opt-out.
//
// Signature scheme and query parameters are unchanged, so links already in the wild keep
// working against the upstream directly.

const DEFAULT_UPSTREAM = 'https://autocompany-comms-2709-dev.twil.io/unsubscribe';

export async function onRequestGet({ request, env }) {
  const incoming = new URL(request.url);
  const upstream = new URL(env.UNSUB_UPSTREAM || DEFAULT_UPSTREAM);
  upstream.search = incoming.search;

  let res;
  try {
    res = await fetch(upstream.toString(), { headers: { accept: 'text/html' } });
  } catch (err) {
    // Never pretend an opt-out succeeded. Say so plainly and give a way through.
    return errorPage(
      'Listeden çıkma işlemi şu anda tamamlanamadı',
      'Teknik bir aksaklık nedeniyle talebiniz işlenemedi. Lütfen birkaç dakika sonra ' +
        'tekrar deneyin veya iletisim@go.appricode.tr adresine yazın — talebinizi elle işleriz.',
      502,
    );
  }

  const body = await res.text();
  return new Response(body, {
    status: res.status,
    headers: {
      'content-type': 'text/html; charset=utf-8',
      'cache-control': 'no-store',
      'referrer-policy': 'no-referrer',
    },
  });
}

function errorPage(title, message, status) {
  const html = `<!doctype html><html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title></head>
<body style="font-family:-apple-system,Segoe UI,Roboto,sans-serif;background:#f6f7f9;margin:0">
<div style="max-width:440px;margin:12vh auto;background:#fff;border-radius:14px;padding:32px;box-shadow:0 1px 4px rgba(0,0,0,.08)">
<h2 style="margin:0 0 12px;color:#1a1a1a">${title}</h2>
<p style="color:#555;line-height:1.6;margin:0">${message}</p></div></body></html>`;
  return new Response(html, {
    status,
    headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store' },
  });
}
