-- HeadInspect anonymous hit counter.
-- Kept as a migration file but the DB binding is intentionally NOT wired in
-- wrangler.toml — enabling it is a one-line uncomment on both sides.
-- Privacy: store host only, never the full URL (query strings can leak PII).

CREATE TABLE IF NOT EXISTS headinspect_hits (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  checked_at TEXT    NOT NULL,   -- ISO-8601
  host       TEXT    NOT NULL    -- hostname only, e.g. "example.com"
);

CREATE INDEX IF NOT EXISTS idx_headinspect_hits_checked_at
  ON headinspect_hits(checked_at);

CREATE INDEX IF NOT EXISTS idx_headinspect_hits_host
  ON headinspect_hits(host);
