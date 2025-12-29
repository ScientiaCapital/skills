-- Stripe Webhook Events Table
--
-- Copy to: supabase/migrations/YYYYMMDDHHMMSS_stripe_webhook_events.sql
--
-- Purpose: Database-backed idempotency for webhook event processing
-- Critical: This prevents duplicate processing when Stripe retries events

-- =============================================================================
-- Table Definition
-- =============================================================================

CREATE TABLE IF NOT EXISTS stripe_webhook_events (
  id TEXT PRIMARY KEY,                    -- Stripe event ID (evt_xxx)
  type TEXT NOT NULL,                     -- Event type (e.g., 'checkout.session.completed')
  data JSONB NOT NULL,                    -- Full event payload
  processed_at TIMESTAMPTZ DEFAULT NOW(), -- When we received/processed it

  -- Optional: Add status tracking for debugging
  processing_status TEXT DEFAULT 'processed',  -- 'processed', 'failed', 'skipped'
  error_message TEXT                      -- If processing failed
);

-- Index for common queries
CREATE INDEX IF NOT EXISTS idx_stripe_webhook_events_type
  ON stripe_webhook_events(type);

CREATE INDEX IF NOT EXISTS idx_stripe_webhook_events_processed_at
  ON stripe_webhook_events(processed_at DESC);

-- =============================================================================
-- Row Level Security
-- =============================================================================

-- Enable RLS
ALTER TABLE stripe_webhook_events ENABLE ROW LEVEL SECURITY;

-- Only service role can access (webhooks use service role key)
-- No user-facing policies needed - this is internal data
CREATE POLICY "Service role full access" ON stripe_webhook_events
  FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

-- =============================================================================
-- User Subscriptions Table (if not exists)
-- =============================================================================

-- This is the table webhooks update - adjust to match your schema
CREATE TABLE IF NOT EXISTS user_subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

  -- Stripe identifiers
  stripe_customer_id TEXT,
  stripe_subscription_id TEXT,

  -- Plan details
  plan_id TEXT DEFAULT 'free',
  status TEXT DEFAULT 'active',  -- 'active', 'cancelled', 'past_due', 'trialing'

  -- Usage tracking (for metered plans)
  usage_count INTEGER DEFAULT 0,
  usage_reset_at TIMESTAMPTZ DEFAULT NOW(),

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  -- Ensure one subscription per user
  UNIQUE(user_id)
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_user_subscriptions_stripe_customer
  ON user_subscriptions(stripe_customer_id);

CREATE INDEX IF NOT EXISTS idx_user_subscriptions_stripe_subscription
  ON user_subscriptions(stripe_subscription_id);

CREATE INDEX IF NOT EXISTS idx_user_subscriptions_status
  ON user_subscriptions(status);

-- =============================================================================
-- RLS for User Subscriptions
-- =============================================================================

ALTER TABLE user_subscriptions ENABLE ROW LEVEL SECURITY;

-- Users can read their own subscription
CREATE POLICY "Users can view own subscription" ON user_subscriptions
  FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

-- Service role can do everything (for webhooks)
CREATE POLICY "Service role full access on subscriptions" ON user_subscriptions
  FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

-- =============================================================================
-- Helper Functions
-- =============================================================================

-- Function to reset monthly usage (call from invoice.paid handler or cron)
CREATE OR REPLACE FUNCTION reset_usage_for_subscription(sub_id TEXT)
RETURNS void AS $$
BEGIN
  UPDATE user_subscriptions
  SET
    usage_count = 0,
    usage_reset_at = NOW(),
    updated_at = NOW()
  WHERE stripe_subscription_id = sub_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to increment usage
CREATE OR REPLACE FUNCTION increment_usage(p_user_id UUID)
RETURNS INTEGER AS $$
DECLARE
  new_count INTEGER;
BEGIN
  UPDATE user_subscriptions
  SET
    usage_count = usage_count + 1,
    updated_at = NOW()
  WHERE user_id = p_user_id
  RETURNING usage_count INTO new_count;

  RETURN COALESCE(new_count, 0);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =============================================================================
-- Cleanup (Optional)
-- =============================================================================

-- Consider adding a cleanup job to remove old webhook events
-- Events older than 30 days are rarely needed for debugging

-- CREATE OR REPLACE FUNCTION cleanup_old_webhook_events()
-- RETURNS void AS $$
-- BEGIN
--   DELETE FROM stripe_webhook_events
--   WHERE processed_at < NOW() - INTERVAL '30 days';
-- END;
-- $$ LANGUAGE plpgsql;

-- Schedule with pg_cron:
-- SELECT cron.schedule('cleanup-webhooks', '0 3 * * *', 'SELECT cleanup_old_webhook_events()');
