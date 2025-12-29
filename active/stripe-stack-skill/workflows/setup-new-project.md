# Setup New Project with Stripe

## Prerequisites

- Stripe account (test mode is fine to start)
- Next.js project with App Router
- Supabase project (for idempotency)

## Step 1: Install Dependencies

```bash
npm install stripe
```

## Step 2: Set Environment Variables

Copy from `templates/env-example.txt` or add manually:

```bash
# .env.local
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

**Get these from:**
1. Stripe Dashboard → Developers → API keys
2. Webhook secret: Create webhook endpoint first (Step 5)

## Step 3: Create Stripe Client

Copy `templates/stripe-client.ts` to your project:

```bash
# Suggested location
cp templates/stripe-client.ts src/lib/stripe/client.ts
```

Or create manually with lazy initialization pattern.

## Step 4: Create Idempotency Table

Run the migration in `templates/idempotency-migration.sql`:

```sql
CREATE TABLE stripe_webhook_events (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  data JSONB NOT NULL,
  processed_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Step 5: Create Webhook Endpoint

1. Copy `templates/webhook-handler-nextjs.ts` to:
   ```
   src/app/api/stripe/webhook/route.ts
   ```

2. Customize the event handlers for your use case

3. Register in Stripe Dashboard:
   - Go to Developers → Webhooks → Add endpoint
   - URL: `https://your-domain.com/api/stripe/webhook`
   - Select events to listen for

4. Copy the signing secret to `STRIPE_WEBHOOK_SECRET`

## Step 6: Create Products/Prices

In Stripe Dashboard:
1. Products → Add Product
2. Set name, description
3. Add pricing (one-time or recurring)
4. Copy price IDs to your config

## Step 7: Deploy and Test

1. Deploy to Vercel
2. Use Stripe CLI to test webhooks locally:
   ```bash
   stripe listen --forward-to localhost:3000/api/stripe/webhook
   ```
3. Trigger test events:
   ```bash
   stripe trigger checkout.session.completed
   ```

## Verification Checklist

- [ ] Stripe client initializes without errors
- [ ] Webhook endpoint returns 200 for valid events
- [ ] Idempotency table logs events
- [ ] Duplicate events are detected and skipped
- [ ] Environment variables set in Vercel
