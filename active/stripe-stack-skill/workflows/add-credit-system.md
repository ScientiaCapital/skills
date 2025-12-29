# Add Credit-Based System

## Overview

Credit systems allow pay-as-you-go pricing where users purchase credits and consume them per operation. This is ideal for:
- Variable usage patterns
- High-value operations (AI analysis, reports)
- Hybrid models (base subscription + credits)

## Step 1: Define Credit Packs

```typescript
// src/lib/stripe/credits.ts

export const CREDIT_PACKS = {
  credit_100: {
    id: 'credit_100',
    name: '$100 Credit Pack',
    amount: 10000, // cents
    credits: 400, // $100 / $0.25 per credit
    priceId: process.env.STRIPE_PRICE_CREDIT_100 || 'price_xxx',
  },
  credit_250: {
    id: 'credit_250',
    name: '$250 Credit Pack',
    amount: 25000,
    credits: 1000,
    priceId: process.env.STRIPE_PRICE_CREDIT_250 || 'price_xxx',
  },
  credit_500: {
    id: 'credit_500',
    name: '$500 Credit Pack',
    amount: 50000,
    credits: 2000,
    priceId: process.env.STRIPE_PRICE_CREDIT_500 || 'price_xxx',
  },
} as const;

export type CreditPackId = keyof typeof CREDIT_PACKS;

// Operation costs
export const OPERATION_CREDITS = {
  photo_analysis: 1,    // $0.25
  blueprint_page: 2,    // $0.50
  full_report: 20,      // $5.00
  premium_feature: 60,  // $15.00
} as const;

export const CENTS_PER_CREDIT = 25;
```

## Step 2: Create User Credits Table

```sql
CREATE TABLE user_credits (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID UNIQUE NOT NULL REFERENCES auth.users(id),
  email TEXT,
  balance_credits INTEGER NOT NULL DEFAULT 0,
  stripe_customer_id TEXT UNIQUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Transaction log for audit
CREATE TABLE credit_transactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id),
  amount INTEGER NOT NULL, -- positive = add, negative = deduct
  balance_after INTEGER NOT NULL,
  transaction_type TEXT NOT NULL, -- 'purchase', 'usage', 'refund', 'bonus'
  description TEXT,
  stripe_payment_id TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS
ALTER TABLE user_credits ENABLE ROW LEVEL SECURITY;
ALTER TABLE credit_transactions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own credits"
  ON user_credits FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can view own transactions"
  ON credit_transactions FOR SELECT USING (auth.uid() = user_id);

-- Helper function to add credits
CREATE OR REPLACE FUNCTION add_credits(
  p_user_id UUID,
  p_amount INTEGER,
  p_type TEXT,
  p_description TEXT DEFAULT NULL,
  p_stripe_id TEXT DEFAULT NULL
) RETURNS INTEGER AS $$
DECLARE
  v_new_balance INTEGER;
BEGIN
  UPDATE user_credits
  SET balance_credits = balance_credits + p_amount,
      updated_at = NOW()
  WHERE user_id = p_user_id
  RETURNING balance_credits INTO v_new_balance;

  INSERT INTO credit_transactions (user_id, amount, balance_after, transaction_type, description, stripe_payment_id)
  VALUES (p_user_id, p_amount, v_new_balance, p_type, p_description, p_stripe_id);

  RETURN v_new_balance;
END;
$$ LANGUAGE plpgsql;
```

## Step 3: Create Credit Purchase Checkout

```typescript
// src/app/api/stripe/buy-credits/route.ts

import { NextRequest, NextResponse } from 'next/server';
import { getStripe } from '@/lib/stripe/client';
import { CREDIT_PACKS, CreditPackId } from '@/lib/stripe/credits';

export async function POST(request: NextRequest) {
  const { packId, userId, userEmail, customerId } = await request.json();

  const pack = CREDIT_PACKS[packId as CreditPackId];
  if (!pack) {
    return NextResponse.json({ error: 'Invalid pack' }, { status: 400 });
  }

  const stripe = getStripe();

  const session = await stripe.checkout.sessions.create({
    mode: 'payment', // One-time, not subscription
    payment_method_types: ['card'],
    line_items: [{
      price_data: {
        currency: 'usd',
        product_data: {
          name: pack.name,
          description: `${pack.credits} credits`,
        },
        unit_amount: pack.amount,
      },
      quantity: 1,
    }],
    success_url: `${process.env.NEXT_PUBLIC_APP_URL}/dashboard?credits=success`,
    cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/credits?canceled=true`,
    customer: customerId || undefined,
    customer_email: customerId ? undefined : userEmail,
    metadata: {
      user_id: userId,
      pack_id: packId,
      credits: pack.credits.toString(),
      type: 'credit_purchase',
    },
  });

  return NextResponse.json({ url: session.url });
}
```

## Step 4: Handle Credit Purchase Webhook

```typescript
// In your webhook handler

async function handleCheckoutComplete(session: Stripe.Checkout.Session) {
  const type = session.metadata?.type;

  if (type === 'credit_purchase') {
    await handleCreditPurchase(session);
  } else {
    await handleSubscriptionCheckout(session);
  }
}

async function handleCreditPurchase(session: Stripe.Checkout.Session) {
  const userId = session.metadata?.user_id;
  const credits = parseInt(session.metadata?.credits || '0');
  const packId = session.metadata?.pack_id;

  if (!userId || !credits) return;

  // Add credits using RPC function
  await supabase.rpc('add_credits', {
    p_user_id: userId,
    p_amount: credits,
    p_type: 'purchase',
    p_description: `Purchased ${packId}`,
    p_stripe_id: session.payment_intent as string,
  });

  console.log(`Added ${credits} credits to user ${userId}`);
}
```

## Step 5: Deduct Credits on Usage

```typescript
// src/lib/credits.ts

export async function deductCredits(
  userId: string,
  amount: number,
  description: string
): Promise<{ success: boolean; balance: number }> {
  // Check balance first
  const { data: user } = await supabase
    .from('user_credits')
    .select('balance_credits')
    .eq('user_id', userId)
    .single();

  if (!user || user.balance_credits < amount) {
    return { success: false, balance: user?.balance_credits || 0 };
  }

  // Deduct credits
  const { data: newBalance } = await supabase.rpc('add_credits', {
    p_user_id: userId,
    p_amount: -amount, // Negative to deduct
    p_type: 'usage',
    p_description: description,
  });

  return { success: true, balance: newBalance };
}

export async function checkCredits(
  userId: string,
  required: number
): Promise<boolean> {
  const { data } = await supabase
    .from('user_credits')
    .select('balance_credits')
    .eq('user_id', userId)
    .single();

  return (data?.balance_credits || 0) >= required;
}
```

## Step 6: Use in API Routes

```typescript
// src/app/api/analyze/route.ts

import { deductCredits, OPERATION_CREDITS } from '@/lib/credits';

export async function POST(request: NextRequest) {
  const { userId, imageUrl } = await request.json();

  // Check and deduct credits
  const cost = OPERATION_CREDITS.photo_analysis;
  const { success, balance } = await deductCredits(
    userId,
    cost,
    'Photo analysis'
  );

  if (!success) {
    return NextResponse.json(
      { error: 'Insufficient credits', balance, required: cost },
      { status: 402 }
    );
  }

  // Perform the operation
  const result = await analyzeImage(imageUrl);

  return NextResponse.json({ result, creditsRemaining: balance });
}
```

## Hybrid Model: Subscription + Credits

Combine subscriptions with credits:

```typescript
// Monthly subscription includes base credits
async function handleInvoicePaid(invoice: Stripe.Invoice) {
  const subscriptionId = invoice.subscription as string;

  // Get plan details
  const { data: sub } = await supabase
    .from('user_subscriptions')
    .select('user_id, plan_id')
    .eq('stripe_subscription_id', subscriptionId)
    .single();

  if (!sub) return;

  // Add monthly credits based on plan
  const monthlyCredits = {
    starter: 50,
    pro: 200,
    business: 1000,
  }[sub.plan_id] || 0;

  await supabase.rpc('add_credits', {
    p_user_id: sub.user_id,
    p_amount: monthlyCredits,
    p_type: 'subscription',
    p_description: `Monthly ${sub.plan_id} credits`,
  });
}
```
