// Branded booking front door: https://auto.appricode.tr/randevu
//
// Redirects to the operator's Google Calendar appointment page, which shows the open slots
// and mints a Google Meet link on booking. There is deliberately NO booking logic here —
// slot generation, timezone handling, double-booking races and cancellation are solved
// problems inside Google Calendar, and reimplementing them would add a failure surface
// without adding anything a recipient can see.
//
// What this buys: the link printed in outreach mail is on our own domain. Same reasoning as
// /listeden-cik — a cold B2B message asking someone to click through to an unfamiliar
// third-party hostname reads as untrustworthy, whatever the destination turns out to be.
//
// Set RANDEVU_URL as a Pages environment variable (Settings > Environment variables) to the
// appointment page URL. If it is unset we show a page that says so and gives the recipient a
// way through — never a redirect to a guessed destination, and never a bare error.

export async function onRequestGet({ env }) {
  const target = (env.RANDEVU_URL || '').trim();

  if (!/^https:\/\//i.test(target)) {
    return page(
      'Randevu sayfası henüz hazır değil',
      'Görüşme takvimi şu anda ayarlanıyor. Bu arada ' +
        '<a href="mailto:iletisim@go.appricode.tr" style="color:#12556B">iletisim@go.appricode.tr</a> ' +
        'adresine yazarak uygun bir saat belirleyebiliriz — aynı gün dönüş yapılır.',
      503,
    );
  }

  return new Response(null, {
    status: 302,
    headers: { location: target, 'cache-control': 'no-store', 'referrer-policy': 'no-referrer' },
  });
}

function page(title, message, status) {
  const html = `<!doctype html><html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title></head>
<body style="font-family:-apple-system,Segoe UI,Roboto,sans-serif;background:#F4F6F8;margin:0">
<div style="max-width:460px;margin:12vh auto;background:#fff;border-radius:14px;padding:32px;box-shadow:0 1px 4px rgba(0,0,0,.08)">
<h2 style="margin:0 0 12px;color:#1A1F26;font-weight:400">${title}</h2>
<p style="color:#414B57;line-height:1.6;margin:0">${message}</p></div></body></html>`;
  return new Response(html, {
    status,
    headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store' },
  });
}
