// SnapOG — alert thresholds.
// Numbers sourced from docs/cfo/snapog-cost-model.md §5 (kill-switch table).
// When any metric crosses its threshold, the cron handler posts to
// ALERT_WEBHOOK_URL. Kept in one file so CFO can revise without touching
// the check logic.

export const ALERT_THRESHOLDS = {
  // D1 free tier is a hard 100k writes/day cap. Alert at 60%.
  d1WritesPerDay: 60_000,

  // 50% of the 10 GB R2 free tier (5 GB in bytes).
  r2StorageBytes: 5 * 1024 * 1024 * 1024,

  // If rolling 14-day cache hit rate slips below this, R2 storage growth
  // is 4x expected — see cost model §7 (Munger inversion).
  cacheHitRateMin: 0.70,

  // >5,000 new free signups in rolling 30 days puts R2 storage on a path
  // to exhaust the 10 GB free tier within 2 months.
  newSignupsRolling30d: 5_000,

  // >3,000 cumulative active free users = we lose the option to *not*
  // wire billing.
  activeUsersMonthly: 3_000,
} as const;

export type ThresholdKey = keyof typeof ALERT_THRESHOLDS;
