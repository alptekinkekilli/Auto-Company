-- SnapOG D1 Schema — Migration 0002
-- Waitlist for paid tiers until Stripe checkout is wired.

CREATE TABLE IF NOT EXISTS waitlist (
  id             TEXT PRIMARY KEY,
  email          TEXT NOT NULL,
  requested_tier TEXT NOT NULL,
  created_at     TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_waitlist_email ON waitlist(email);
