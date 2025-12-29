/**
 * Stripe Webhook Handler Template
 *
 * Copy to: src/app/api/stripe/webhook/route.ts
 *
 * Features:
 * - Database-backed idempotency
 * - All common subscription events
 * - Error handling that doesn't trigger retries
 * - TypeScript with proper types
 */

import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';
import Stripe from 'stripe';

// Vercel config
export const runtime = 'nodejs';
export const maxDuration = 30;
export const dynamic = 'force-dynamic';

// Lazy-loaded Stripe client
let _stripe: Stripe | null = null;

function getStripe(): Stripe {
  if (!_stripe) {
    const key = process.env.STRIPE_SECRET_KEY;
    if (!key) throw new Error('STRIPE_SECRET_KEY not configured');
    _stripe = new Stripe(key, {
      apiVersion: '2025-12-15.clover',
      typescript: true,
    });
  }
  return _stripe;
}

// Service role client for webhook handlers (bypasses RLS)
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);

export async function POST(request: NextRequest) {
  const body = await request.text();
  const signature = request.headers.get('stripe-signature');

  if (!signature) {
    return NextResponse.json(
      { error: 'Missing stripe-signature header' },
      { status: 400 }
    );
  }

  const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;
  if (!webhookSecret) {
    console.error('[Stripe] STRIPE_WEBHOOK_SECRET not configured');
    return NextResponse.json(
      { error: 'Webhook secret not configured' },
      { status: 500 }
    );
  }

  let event: Stripe.Event;

  try {
    event = getStripe().webhooks.constructEvent(body, signature, webhookSecret);
  } catch (err) {
    console.error('[Stripe] Signature verification failed:', err);
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 });
  }

  // Idempotency check - has this event been processed?
  const { data: existing } = await supabase
    .from('stripe_webhook_events')
    .select('id')
    .eq('id', event.id)
    .single();

  if (existing) {
    console.log(`[Stripe] Duplicate event: ${event.id}`);
    return NextResponse.json({ received: true, duplicate: true });
  }

  // Log event BEFORE processing (critical for idempotency)
  await supabase.from('stripe_webhook_events').insert({
    id: event.id,
    type: event.type,
    data: event,
  });

  console.log(`[Stripe] Processing: ${event.type} (${event.id})`);

  try {
    switch (event.type) {
      case 'checkout.session.completed':
        await handleCheckoutComplete(event.data.object as Stripe.Checkout.Session);
        break;

      case 'customer.subscription.created':
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
        console.log(`[Stripe] Unhandled event: ${event.type}`);
    }

    return NextResponse.json({ received: true });
  } catch (error) {
    console.error(`[Stripe] Error processing ${event.type}:`, error);
    // Return 500 to trigger Stripe retry (consider 200 if you want to skip retries)
    return NextResponse.json({ error: 'Handler failed' }, { status: 500 });
  }
}

// =============================================================================
// Event Handlers - Customize these for your use case
// =============================================================================

async function handleCheckoutComplete(session: Stripe.Checkout.Session) {
  const userId = session.metadata?.user_id;
  const planId = session.metadata?.plan_id;
  const customerId = session.customer as string;
  const subscriptionId = session.subscription as string;

  if (!userId) {
    console.error('[Stripe] No user_id in checkout metadata');
    return;
  }

  console.log(`[Stripe] Checkout complete: user=${userId}, plan=${planId}`);

  // TODO: Customize this for your schema
  const { error } = await supabase.from('user_subscriptions').upsert(
    {
      user_id: userId,
      stripe_customer_id: customerId,
      stripe_subscription_id: subscriptionId,
      plan_id: planId || 'starter',
      status: 'active',
      updated_at: new Date().toISOString(),
    },
    { onConflict: 'user_id' }
  );

  if (error) {
    console.error('[Stripe] Error creating subscription:', error);
    throw error;
  }
}

async function handleSubscriptionChange(subscription: Stripe.Subscription) {
  const subscriptionId = subscription.id;
  const status = subscription.status;
  const planId = subscription.metadata?.plan_id;

  console.log(`[Stripe] Subscription updated: ${subscriptionId} → ${status}`);

  const { error } = await supabase
    .from('user_subscriptions')
    .update({
      status: status,
      plan_id: planId,
      updated_at: new Date().toISOString(),
    })
    .eq('stripe_subscription_id', subscriptionId);

  if (error) {
    console.error('[Stripe] Error updating subscription:', error);
    throw error;
  }
}

async function handleSubscriptionDeleted(subscription: Stripe.Subscription) {
  const subscriptionId = subscription.id;

  console.log(`[Stripe] Subscription cancelled: ${subscriptionId}`);

  const { error } = await supabase
    .from('user_subscriptions')
    .update({
      status: 'cancelled',
      plan_id: 'free',
      stripe_subscription_id: null,
      updated_at: new Date().toISOString(),
    })
    .eq('stripe_subscription_id', subscriptionId);

  if (error) {
    console.error('[Stripe] Error cancelling subscription:', error);
    throw error;
  }
}

async function handleInvoicePaid(invoice: Stripe.Invoice) {
  // Extract subscription ID (handles both old and new Stripe structures)
  const subscriptionId = getSubscriptionIdFromInvoice(invoice);

  if (!subscriptionId) {
    console.log('[Stripe] Non-subscription invoice, skipping');
    return;
  }

  console.log(`[Stripe] Invoice paid for: ${subscriptionId}`);

  // Reset usage for new billing period
  const { error } = await supabase
    .from('user_subscriptions')
    .update({
      usage_count: 0,
      status: 'active',
      updated_at: new Date().toISOString(),
    })
    .eq('stripe_subscription_id', subscriptionId);

  if (error) {
    console.error('[Stripe] Error resetting usage:', error);
    throw error;
  }
}

async function handlePaymentFailed(invoice: Stripe.Invoice) {
  const subscriptionId = getSubscriptionIdFromInvoice(invoice);

  if (!subscriptionId) return;

  console.log(`[Stripe] Payment failed for: ${subscriptionId}`);

  const { error } = await supabase
    .from('user_subscriptions')
    .update({
      status: 'past_due',
      updated_at: new Date().toISOString(),
    })
    .eq('stripe_subscription_id', subscriptionId);

  if (error) {
    console.error('[Stripe] Error marking past_due:', error);
    throw error;
  }

  // TODO: Send email notification to user
}

// =============================================================================
// Helpers
// =============================================================================

function getSubscriptionIdFromInvoice(invoice: Stripe.Invoice): string | undefined {
  // Handle modern Stripe invoice structure
  const invoiceAny = invoice as Record<string, unknown>;
  const parent = invoiceAny.parent as Record<string, unknown> | null;
  const subDetails = parent?.subscription_details as Record<string, unknown> | null;

  if (subDetails?.subscription) {
    const sub = subDetails.subscription;
    return typeof sub === 'string' ? sub : (sub as { id: string })?.id;
  }

  // Fallback: Check line items
  const lineSub = invoice.lines?.data?.[0]?.subscription;
  return typeof lineSub === 'string' ? lineSub : undefined;
}
