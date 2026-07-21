// SnapOG — cost-alerting cron entry point.
// Wired to wrangler.toml [triggers] crons. Runs every 6 hours.

import type { Env } from '../types';
import { runAllChecks } from './check';
import { postAlerts } from './webhook';

export async function runCostAlertCheck(env: Env): Promise<{ alertCount: number }> {
  const alerts = await runAllChecks(env);
  if (alerts.length > 0) {
    await postAlerts(env, alerts);
  }
  return { alertCount: alerts.length };
}
