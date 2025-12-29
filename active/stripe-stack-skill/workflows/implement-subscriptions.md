# Implement Subscription Billing

## Overview

This workflow covers recurring subscription billing with plans, tiers, and usage limits.

## Step 1: Define Your Plans

Create a plans configuration file:

```typescript
// src/lib/stripe/plans.ts

export const PLANS = {
  free: {
    id: 'free',
    name: 'Free',
    price: 0,
    priceId: null, // No Stripe price for free
    features: ['3 requests/month', 'Basic support'],
    limits: { requestsMonthly: 3 },
  },
  starter: {
    id: 'starter',
    name: 'Starter',
    price: 2900, // cents ($29)
    priceId: process.env.STRIPE_PRICE_STARTER_MONTHLY || 'price_xxx',
    features: ['50 requests/month', 'Email support'],
    limits: { requestsMonthly: 50 },
  },
  pro: {
    id: 'pro',
    name: 'Pro',
    price: 7900, // cents ($79)
    priceId: process.env.STRIPE_PRICE_PRO_MONTHLY || 'price_xxx',
    features: ['500 requests/month', 'Priority support', 'API access'],
    limits: { requestsMonthly: 500 },
  },
  business: {
    id: 'business',
    name: 'Business',
    price: 19900, // cents ($199)
    priceId: process.env.STRIPE_PRICE_BUSINESS_MONTHLY || 'price_xxx',
    features: ['Unlimited requests', '24/7 support', 'Custom integrations'],
    limits: { requestsMonthly: -1 }, // -1 = unlimited
  },
} as const;

export type PlanId = keyof typeof PLANS;

export function getPlan(id: PlanId) {
  return PLANS[id] || PLANS.free;
}
```

## Step 2: Create Products in Stripe

1. Go to Stripe Dashboard → Products
2. Create a product for each paid plan
3. Add monthly pricing
4. Copy price IDs to environment variables

## Step 3: Create Checkout Session API

```typescript
// src/app/api/stripe/checkout/route.ts

import { NextRequest, NextResponse } from 'next/server';
import { getStripe } from '@/lib/stripe/client';
import { PLANS, PlanId } from '@/lib/stripe/plans';

export async function POST(request: NextRequest) {
  const { planId, userId, userEmail } = await request.json();

  const plan = PLANS[planId as PlanId];
  if (!plan || !plan.priceId) {
    return NextResponse.json({ error: 'Invalid plan' }, { status: 400 });
  }

  const stripe = getStripe();

  const session = await stripe.checkout.sessions.create({
    mode: 'subscription',
    payment_method_types: ['card'],
    line_items: [{ price: plan.priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_APP_URL}/dashboard?success=true`,
    cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/pricing?canceled=true`,
    customer_email: userEmail,
    metadata: {
      user_id: userId,
      plan_id: planId,
    },
    subscription_data: {
      metadata: {
        user_id: userId,
        plan_id: planId,
      },
    },
  });

  return NextResponse.json({ url: session.url });
}
```

## Step 4: Handle Webhook Events

In your webhook handler, process subscription events:

```typescript
async function handleCheckoutComplete(session: Stripe.Checkout.Session) {
  const userId = session.metadata?.user_id;
  const planId = session.metadata?.plan_id as PlanId;
  const customerId = session.customer as string;
  const subscriptionId = session.subscription as string;

  if (!userId) return;

  const plan = getPlan(planId);

  await supabase.from('user_subscriptions').upsert({
    user_id: userId,
    stripe_customer_id: customerId,
    stripe_subscription_id: subscriptionId,
    plan_id: planId,
    status: 'active',
    requests_monthly: plan.limits.requestsMonthly,
    requests_used: 0,
    current_period_start: new Date().toISOString(),
  }, { onConflict: 'user_id' });
}

async function handleSubscriptionChange(subscription: Stripe.Subscription) {
  const planId = subscription.metadata?.plan_id as PlanId;
  const plan = getPlan(planId);

  await supabase
    .from('user_subscriptions')
    .update({
      status: subscription.status,
      plan_id: planId,
      requests_monthly: plan.limits.requestsMonthly,
    })
    .eq('stripe_subscription_id', subscription.id);
}

async function handleSubscriptionDeleted(subscription: Stripe.Subscription) {
  const freePlan = getPlan('free');

  await supabase
    .from('user_subscriptions')
    .update({
      status: 'cancelled',
      plan_id: 'free',
      requests_monthly: freePlan.limits.requestsMonthly,
      stripe_subscription_id: null,
    })
    .eq('stripe_subscription_id', subscription.id);
}

async function handleInvoicePaid(invoice: Stripe.Invoice) {
  // Reset usage for new billing period
  const subscriptionId = invoice.subscription as string;

  await supabase
    .from('user_subscriptions')
    .update({
      requests_used: 0,
      current_period_start: new Date().toISOString(),
    })
    .eq('stripe_subscription_id', subscriptionId);
}
```

## Step 5: Create User Subscription Table

```sql
CREATE TABLE user_subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID UNIQUE NOT NULL REFERENCES auth.users(id),
  stripe_customer_id TEXT,
  stripe_subscription_id TEXT,
  plan_id TEXT NOT NULL DEFAULT 'free',
  status TEXT NOT NULL DEFAULT 'active',
  requests_monthly INTEGER NOT NULL DEFAULT 3,
  requests_used INTEGER NOT NULL DEFAULT 0,
  current_period_start TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS
ALTER TABLE user_subscriptions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own subscription"
  ON user_subscriptions FOR SELECT
  USING (auth.uid() = user_id);
```

## Step 6: Check Usage in API Routes

```typescript
async function checkUsageLimit(userId: string): Promise<boolean> {
  const { data } = await supabase
    .from('user_subscriptions')
    .select('requests_monthly, requests_used')
    .eq('user_id', userId)
    .single();

  if (!data) return false;
  if (data.requests_monthly === -1) return true; // Unlimited

  return data.requests_used < data.requests_monthly;
}

async function incrementUsage(userId: string) {
  await supabase.rpc('increment_requests_used', { user_id: userId });
}
```

## Frontend: Pricing Page

```tsx
// components/PricingCard.tsx
export function PricingCard({ plan, currentPlan }) {
  const handleSubscribe = async () => {
    const response = await fetch('/api/stripe/checkout', {
      method: 'POST',
      body: JSON.stringify({
        planId: plan.id,
        userId: user.id,
        userEmail: user.email,
      }),
    });
    const { url } = await response.json();
    window.location.href = url;
  };

  return (
    <div className="pricing-card">
      <h3>{plan.name}</h3>
      <p>${plan.price / 100}/month</p>
      <ul>
        {plan.features.map(f => <li key={f}>{f}</li>)}
      </ul>
      <button onClick={handleSubscribe}>
        {currentPlan === plan.id ? 'Current' : 'Subscribe'}
      </button>
    </div>
  );
}
```
