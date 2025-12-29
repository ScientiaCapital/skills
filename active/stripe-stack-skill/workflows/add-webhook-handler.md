# Add Webhook Handler to Existing Project

## Prerequisites

- Stripe SDK already installed
- Supabase or database connection available

## Step 1: Create Idempotency Table

If not already created, run this migration:

```sql
CREATE TABLE stripe_webhook_events (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  data JSONB NOT NULL,
  processed_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_stripe_events_type ON stripe_webhook_events(type);
CREATE INDEX idx_stripe_events_processed ON stripe_webhook_events(processed_at DESC);
```

## Step 2: Create Webhook Route

Create `src/app/api/stripe/webhook/route.ts`:

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { getStripe } from '@/lib/stripe/client';
import { createClient } from '@supabase/supabase-js';
import type Stripe from 'stripe';

// Use service role for webhook handlers (bypasses RLS)
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);

export async function POST(request: NextRequest) {
  const body = await request.text();
  const signature = request.headers.get('stripe-signature');

  if (!signature) {
    return NextResponse.json({ error: 'Missing signature' }, { status: 400 });
  }

  const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;
  if (!webhookSecret) {
    console.error('STRIPE_WEBHOOK_SECRET not configured');
    return NextResponse.json({ error: 'Server error' }, { status: 500 });
  }

  let event: Stripe.Event;

  try {
    event = getStripe().webhooks.constructEvent(body, signature, webhookSecret);
  } catch (err) {
    console.error('Webhook signature verification failed:', err);
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 });
  }

  // Idempotency check
  const { data: existing } = await supabase
    .from('stripe_webhook_events')
    .select('id')
    .eq('id', event.id)
    .single();

  if (existing) {
    return NextResponse.json({ received: true, duplicate: true });
  }

  // Log event BEFORE processing
  await supabase.from('stripe_webhook_events').insert({
    id: event.id,
    type: event.type,
    data: event,
  });

  console.log(`Processing: ${event.type} (${event.id})`);

  try {
    switch (event.type) {
      case 'checkout.session.completed':
        await handleCheckoutComplete(event.data.object as Stripe.Checkout.Session);
        break;
      case 'customer.subscription.updated':
        await handleSubscriptionChange(event.data.object as Stripe.Subscription);
        break;
      case 'customer.subscription.deleted':
        await handleSubscriptionDeleted(event.data.object as Stripe.Subscription);
        break;
      case 'invoice.paid':
        await handleInvoicePaid(event.data.object as Stripe.Invoice);
        break;
      case 'invoice.payment_failed':
        await handlePaymentFailed(event.data.object as Stripe.Invoice);
        break;
      default:
        console.log(`Unhandled: ${event.type}`);
    }

    return NextResponse.json({ received: true });
  } catch (error) {
    console.error(`Error processing ${event.type}:`, error);
    return NextResponse.json({ error: 'Handler failed' }, { status: 500 });
  }
}

// Implement these based on your needs
async function handleCheckoutComplete(session: Stripe.Checkout.Session) {
  // Create subscription record, initialize user
}

async function handleSubscriptionChange(subscription: Stripe.Subscription) {
  // Update plan, sync limits
}

async function handleSubscriptionDeleted(subscription: Stripe.Subscription) {
  // Downgrade to free tier
}

async function handleInvoicePaid(invoice: Stripe.Invoice) {
  // Reset usage counters for new period
}

async function handlePaymentFailed(invoice: Stripe.Invoice) {
  // Mark as past_due, send notification
}
```

## Step 3: Add Route Config (Vercel)

Add to the webhook route file:

```typescript
export const runtime = 'nodejs';
export const maxDuration = 30;
export const dynamic = 'force-dynamic';
```

## Step 4: Register Webhook in Stripe

1. Go to Stripe Dashboard → Developers → Webhooks
2. Click "Add endpoint"
3. Enter URL: `https://your-domain.com/api/stripe/webhook`
4. Select events:
   - `checkout.session.completed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.paid`
   - `invoice.payment_failed`
5. Copy signing secret to `STRIPE_WEBHOOK_SECRET`

## Step 5: Test Locally

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward events to local server
stripe listen --forward-to localhost:3000/api/stripe/webhook

# In another terminal, trigger test events
stripe trigger checkout.session.completed
```

## Common Issues

**400 "Invalid signature"**
- Check `STRIPE_WEBHOOK_SECRET` matches the endpoint
- Ensure using `request.text()` not `request.json()`

**Duplicate processing**
- Verify idempotency table exists
- Check if service role client has access

**Handler errors not visible**
- Add detailed console logging
- Check Vercel function logs
