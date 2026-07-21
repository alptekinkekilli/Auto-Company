// SnapOG — shared types

export type Tier = 'free' | 'pro' | 'business';

export const TIER_LIMITS: Record<Tier, number> = {
  free: 100,
  pro: 10_000,
  business: 100_000,
};

// Max distinct cacheKey values a single api_key may write to R2 per billing
// month. Beyond this, /og still renders but skips OG_CACHE.put() and returns
// X-Cache: BYPASSED. Bounds R2 storage against unique-URL abuse (audit G8).
export const MONTHLY_CACHE_KEY_CAP = 30;

export interface ApiKey {
  id: string;
  user_id: string;
  name: string;
  key_prefix: string;
  key_hash: string;
  tier: Tier;
  monthly_limit: number;
  usage_count: number;
  usage_reset_at: string;
  created_at: string;
}

export interface OGParams {
  title: string;
  description?: string;
  theme?: 'dark' | 'light';
  template?: 'default' | 'blog' | 'article';
  author?: string;
  domain?: string;
  tag?: string;
}

export interface Env {
  DB: D1Database;
  OG_CACHE: R2Bucket;
  ENVIRONMENT: string;
  AUTH_SECRET?: string;
}
