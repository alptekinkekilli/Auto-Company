-- =============================================================================
-- SnapOG North-Star Metric — canonical SQL
-- =============================================================================
-- North-star: Weekly Active Producers (WAP)
--   = distinct api_key_id that generated at least 1 NON-CACHED OG image
--     (cache_hit = 0) inside the reporting window.
--
-- Why "non-cached": a cache_hit=1 event is an edge-served static response
-- with near-zero marginal cost and zero signal of new demand. Only cache
-- misses represent an api_key doing something the system hadn't already
-- pre-computed — i.e. a real, load-bearing generation. WAP therefore
-- tracks unique keys doing real work, not raw request volume.
--
-- Secondary metrics captured alongside so we can act on the same read:
--   - cache_hit_ratio     : cost-efficiency signal. Higher = cheaper to serve.
--   - total_events        : raw traffic (includes cache hits).
--   - active_producers    : the distinct-key count per bucket (the WAP number).
--
-- Target: DB is snapog-db (D1 UUID efd6d504-3a34-49a7-9ff7-0d0d4d57c801,
-- WEUR primary). Schema is migrations/0001_init.sql. All queries below are
-- read-only and safe to run from the dashboard, `wrangler d1 execute`, or
-- the Cloudflare MCP `d1_database_query` tool.
-- =============================================================================


-- -----------------------------------------------------------------------------
-- Q1. Daily breakdown, last 30 days.
-- Primary north-star surface. One row per calendar day, most-recent first.
-- Days with zero traffic will NOT appear (GROUP BY on empty bucket = no row);
-- if you need a zero-filled calendar for charts, do that client-side.
-- -----------------------------------------------------------------------------
WITH daily AS (
  SELECT
    substr(generated_at, 1, 10) AS day,
    api_key_id,
    cache_hit
  FROM usage_events
  WHERE generated_at >= datetime('now', '-30 days')
)
SELECT
  day,
  COUNT(DISTINCT CASE WHEN cache_hit = 0 THEN api_key_id END) AS active_producers,
  COUNT(*)                                                    AS total_events,
  SUM(cache_hit)                                              AS cache_hits,
  ROUND(1.0 * SUM(cache_hit) / NULLIF(COUNT(*), 0), 3)        AS cache_hit_ratio
FROM daily
GROUP BY day
ORDER BY day DESC;


-- -----------------------------------------------------------------------------
-- Q2. Rolling 7-day and 30-day WAP roll-up (one row, for scorecards).
-- Use this for the "front page" number when a single WAP-today value is
-- more useful than a 30-row time-series.
-- -----------------------------------------------------------------------------
SELECT
  COUNT(DISTINCT CASE
    WHEN cache_hit = 0
     AND generated_at >= datetime('now', '-7 days')
    THEN api_key_id
  END) AS wap_7d,
  COUNT(DISTINCT CASE
    WHEN cache_hit = 0
     AND generated_at >= datetime('now', '-30 days')
    THEN api_key_id
  END) AS wap_30d,
  COUNT(*) FILTER (WHERE generated_at >= datetime('now', '-30 days')) AS events_30d,
  ROUND(
    1.0 * SUM(cache_hit) FILTER (WHERE generated_at >= datetime('now', '-30 days'))
        / NULLIF(COUNT(*) FILTER (WHERE generated_at >= datetime('now', '-30 days')), 0),
    3
  ) AS cache_hit_ratio_30d
FROM usage_events;


-- -----------------------------------------------------------------------------
-- Q3. Per-key activity leaderboard, last 30 days.
-- Feeds two decisions:
--   (a) who to email for testimonials / case studies (top of list),
--   (b) which free-tier keys are approaching monthly_limit and should be
--       nudged to upgrade (join to api_keys.monthly_limit / usage_count).
-- Only counts non-cached events, so churn on a cached asset doesn't inflate
-- someone's "activity".
-- -----------------------------------------------------------------------------
SELECT
  ak.id                                             AS api_key_id,
  ak.key_prefix,
  ak.tier,
  ak.monthly_limit,
  ak.usage_count,
  COUNT(ue.id) FILTER (WHERE ue.cache_hit = 0)      AS misses_30d,
  COUNT(ue.id) FILTER (WHERE ue.cache_hit = 1)      AS hits_30d,
  MIN(ue.generated_at) FILTER (WHERE ue.cache_hit = 0) AS first_miss_30d,
  MAX(ue.generated_at) FILTER (WHERE ue.cache_hit = 0) AS last_miss_30d
FROM api_keys ak
LEFT JOIN usage_events ue
  ON ue.api_key_id = ak.id
 AND ue.generated_at >= datetime('now', '-30 days')
GROUP BY ak.id, ak.key_prefix, ak.tier, ak.monthly_limit, ak.usage_count
HAVING misses_30d > 0
ORDER BY misses_30d DESC
LIMIT 50;
