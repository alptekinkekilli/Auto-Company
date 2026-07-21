// SnapOG — cost-alerting check logic.
// Each check is independent so one failure never suppresses the rest.
// D1-derived metrics use `usage_events.generated_at` (indexed) and
// `api_keys.created_at`.

import type { Env } from '../types';
import { ALERT_THRESHOLDS } from './thresholds';
import { fetchR2BucketStorage } from './graphql';

export type AlertSeverity = 'info' | 'warn' | 'critical';

export interface Alert {
  name: string;
  severity: AlertSeverity;
  current: number | string;
  threshold: number | string;
  message: string;
}

const DAY_MS = 86_400_000;
const R2_BUCKET_NAME = 'snapog-og-cache';

// Approx: each /og call issues 2 D1 writes (recordUsage batches an UPDATE
// on api_keys + an INSERT into usage_events). See cost model §1 A4.
const D1_WRITES_PER_REQUEST = 2;

async function checkD1WritesPerDay(env: Env): Promise<Alert | null> {
  const since = new Date(Date.now() - DAY_MS).toISOString();
  const row = await env.DB
    .prepare('SELECT COUNT(*) as cnt FROM usage_events WHERE generated_at > ?')
    .bind(since)
    .first<{ cnt: number }>();
  const events = row?.cnt ?? 0;
  const estimatedWrites = events * D1_WRITES_PER_REQUEST;
  const threshold = ALERT_THRESHOLDS.d1WritesPerDay;
  if (estimatedWrites <= threshold) return null;
  return {
    name: 'd1_writes_per_day',
    severity: estimatedWrites > threshold * 1.5 ? 'critical' : 'warn',
    current: estimatedWrites,
    threshold,
    message: `Estimated ${estimatedWrites.toLocaleString()} D1 writes in the last 24h (>${threshold.toLocaleString()} threshold; free-tier hard cap is 100,000/day).`,
  };
}

async function checkCacheHitRate(env: Env): Promise<Alert | null> {
  const since = new Date(Date.now() - 14 * DAY_MS).toISOString();
  const row = await env.DB
    .prepare(
      `SELECT
         COUNT(*) as total,
         SUM(CASE WHEN cache_hit = 1 THEN 1 ELSE 0 END) as hits
       FROM usage_events WHERE generated_at > ?`
    )
    .bind(since)
    .first<{ total: number; hits: number }>();
  const total = row?.total ?? 0;
  const hits = row?.hits ?? 0;
  // Need a minimum sample before this metric is meaningful.
  if (total < 500) return null;
  const rate = hits / total;
  const threshold = ALERT_THRESHOLDS.cacheHitRateMin;
  if (rate >= threshold) return null;
  return {
    name: 'cache_hit_rate',
    severity: rate < threshold * 0.7 ? 'critical' : 'warn',
    current: rate.toFixed(3),
    threshold: threshold.toFixed(3),
    message: `14-day cache hit rate ${(rate * 100).toFixed(1)}% (${hits}/${total}) below ${(threshold * 100).toFixed(0)}% target — R2 storage will grow ~4x expected. See cost model §7.`,
  };
}

async function checkNewSignups(env: Env): Promise<Alert | null> {
  const since = new Date(Date.now() - 30 * DAY_MS).toISOString();
  const row = await env.DB
    .prepare('SELECT COUNT(*) as cnt FROM api_keys WHERE created_at > ?')
    .bind(since)
    .first<{ cnt: number }>();
  const signups = row?.cnt ?? 0;
  const threshold = ALERT_THRESHOLDS.newSignupsRolling30d;
  if (signups <= threshold) return null;
  return {
    name: 'new_signups_rolling_30d',
    severity: 'warn',
    current: signups,
    threshold,
    message: `${signups.toLocaleString()} new signups in the last 30 days (>${threshold.toLocaleString()}). At 100 img/mo per user this generates ~2.6 GB/mo of R2 storage.`,
  };
}

async function checkActiveUsers(env: Env): Promise<Alert | null> {
  const row = await env.DB
    .prepare('SELECT COUNT(*) as cnt FROM api_keys WHERE usage_count > 0')
    .first<{ cnt: number }>();
  const active = row?.cnt ?? 0;
  const threshold = ALERT_THRESHOLDS.activeUsersMonthly;
  if (active <= threshold) return null;
  return {
    name: 'active_users_monthly',
    severity: 'warn',
    current: active,
    threshold,
    message: `${active.toLocaleString()} active free users this billing month (>${threshold.toLocaleString()}) — trajectory suggests paid tier within 24 months even at flat growth.`,
  };
}

async function checkR2Storage(env: Env): Promise<Alert | null> {
  const token = env.CLOUDFLARE_ANALYTICS_API_TOKEN;
  const accountId = env.CLOUDFLARE_ACCOUNT_ID;
  if (!token || !accountId) {
    return null;
  }
  const sample = await fetchR2BucketStorage(accountId, R2_BUCKET_NAME, token);
  if (!sample) return null;
  const totalBytes = sample.payloadSizeBytes + sample.metadataSizeBytes;
  const threshold = ALERT_THRESHOLDS.r2StorageBytes;
  if (totalBytes <= threshold) return null;
  const gb = (totalBytes / (1024 * 1024 * 1024)).toFixed(2);
  return {
    name: 'r2_storage_bytes',
    severity: totalBytes > threshold * 1.5 ? 'critical' : 'warn',
    current: totalBytes,
    threshold,
    message: `R2 bucket "${sample.bucketName}" holds ${gb} GB (>50% of 10 GB free tier). Ship the R2 lifecycle rule (G8 fix #1) if not yet done.`,
  };
}

// Run every check; collect alerts. A check that throws is logged and
// treated as no-alert-fired so a broken check never triggers false
// positives, but the failure is visible in Workers logs.
export async function runAllChecks(env: Env): Promise<Alert[]> {
  const checks: Array<() => Promise<Alert | null>> = [
    () => checkD1WritesPerDay(env),
    () => checkCacheHitRate(env),
    () => checkNewSignups(env),
    () => checkActiveUsers(env),
    () => checkR2Storage(env),
  ];
  const results = await Promise.all(
    checks.map(async fn => {
      try {
        return await fn();
      } catch (err) {
        console.error('[alerts] check failed:', err);
        return null;
      }
    })
  );
  return results.filter((a): a is Alert => a !== null);
}
