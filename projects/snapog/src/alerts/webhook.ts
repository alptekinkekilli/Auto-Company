// Post fired alerts to ALERT_WEBHOOK_URL as generic JSON.
// Compatible with Slack/Discord incoming webhooks (they accept arbitrary
// JSON; formatted rendering is out of scope for the stub).

import type { Env } from '../types';
import type { Alert } from './check';

export interface AlertPayload {
  project: 'snapog';
  environment: string;
  timestamp: string;
  alerts: Alert[];
}

export async function postAlerts(env: Env, alerts: Alert[]): Promise<void> {
  if (alerts.length === 0) return;
  const url = env.ALERT_WEBHOOK_URL;
  if (!url) {
    // Log-only mode: the checks ran, alerts fired, but the founder hasn't
    // wired a webhook yet. Surface in Workers logs so `wrangler tail` shows it.
    console.warn('[alerts] ALERT_WEBHOOK_URL unset; alerts would have fired:', JSON.stringify(alerts));
    return;
  }
  const payload: AlertPayload = {
    project: 'snapog',
    environment: env.ENVIRONMENT,
    timestamp: new Date().toISOString(),
    alerts,
  };
  try {
    const resp = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!resp.ok) {
      console.error(`[alerts] webhook POST HTTP ${resp.status}: ${await resp.text().catch(() => '')}`);
    }
  } catch (err) {
    console.error('[alerts] webhook POST failed:', err);
  }
}
