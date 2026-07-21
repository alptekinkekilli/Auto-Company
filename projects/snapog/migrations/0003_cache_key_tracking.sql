-- SnapOG D1 Schema — Migration 0003
-- Per-API-key distinct-cache-key tracking to cap R2 storage abuse.
-- See docs/qa/snapog-launch-audit.md G8, docs/cfo/snapog-cost-model.md §4.

CREATE TABLE IF NOT EXISTS api_key_cache_keys (
  api_key_id     TEXT NOT NULL,
  cache_key      TEXT NOT NULL,
  -- ISO timestamp of the first day of the billing month
  -- (matches api_keys.usage_reset_at semantics).
  billing_month  TEXT NOT NULL,
  first_seen_at  TEXT NOT NULL DEFAULT (datetime('now')),
  PRIMARY KEY (api_key_id, cache_key, billing_month)
);

CREATE INDEX IF NOT EXISTS idx_ckeys_by_key_month
  ON api_key_cache_keys(api_key_id, billing_month);
