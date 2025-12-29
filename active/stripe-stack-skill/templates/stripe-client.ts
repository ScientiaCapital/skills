/**
 * Stripe Client Factory
 *
 * Copy to: src/lib/stripe/client.ts
 *
 * Features:
 * - Lazy initialization (avoids build-time errors)
 * - Type-safe API version
 * - Validation at runtime
 * - Backwards-compatible export
 */

import Stripe from 'stripe';

// Lazy-initialized Stripe instance
let _stripe: Stripe | null = null;

/**
 * Get the Stripe server-side client
 *
 * Uses lazy initialization to prevent build-time errors when
 * STRIPE_SECRET_KEY isn't available during static generation.
 */
export function getStripe(): Stripe {
  if (!_stripe) {
    const key = process.env.STRIPE_SECRET_KEY;

    if (!key) {
      throw new Error('STRIPE_SECRET_KEY is not configured');
    }

    if (!key.startsWith('sk_')) {
      throw new Error('STRIPE_SECRET_KEY must start with sk_');
    }

    _stripe = new Stripe(key, {
      apiVersion: '2025-12-15.clover', // Update to latest
      typescript: true,
    });
  }

  return _stripe;
}

/**
 * Backwards-compatible export
 *
 * Use getStripe() in new code for explicit initialization.
 * This proxy provides the same API for existing code.
 */
export const stripe = {
  get checkout() {
    return getStripe().checkout;
  },
  get customers() {
    return getStripe().customers;
  },
  get subscriptions() {
    return getStripe().subscriptions;
  },
  get webhooks() {
    return getStripe().webhooks;
  },
  get paymentMethods() {
    return getStripe().paymentMethods;
  },
  get prices() {
    return getStripe().prices;
  },
  get products() {
    return getStripe().products;
  },
  get invoices() {
    return getStripe().invoices;
  },
  get billingPortal() {
    return getStripe().billingPortal;
  },
};

// =============================================================================
// Helper Functions
// =============================================================================

/**
 * Create a Stripe Customer Portal session
 */
export async function createPortalSession(params: {
  customerId: string;
  returnUrl: string;
}): Promise<Stripe.BillingPortal.Session> {
  return getStripe().billingPortal.sessions.create({
    customer: params.customerId,
    return_url: params.returnUrl,
  });
}

/**
 * Create or retrieve a Stripe Customer
 */
export async function getOrCreateCustomer(params: {
  email: string;
  name?: string;
  userId: string;
  existingCustomerId?: string;
}): Promise<Stripe.Customer> {
  const stripe = getStripe();

  // Return existing customer if valid
  if (params.existingCustomerId) {
    try {
      const customer = await stripe.customers.retrieve(params.existingCustomerId);
      if (!customer.deleted) {
        return customer as Stripe.Customer;
      }
    } catch {
      // Customer doesn't exist, create new one
    }
  }

  // Create new customer
  return stripe.customers.create({
    email: params.email,
    name: params.name,
    metadata: {
      user_id: params.userId,
    },
  });
}

/**
 * Cancel a subscription
 */
export async function cancelSubscription(
  subscriptionId: string,
  immediately = false
): Promise<Stripe.Subscription> {
  const stripe = getStripe();

  if (immediately) {
    return stripe.subscriptions.cancel(subscriptionId);
  }

  return stripe.subscriptions.update(subscriptionId, {
    cancel_at_period_end: true,
  });
}

/**
 * Get subscription details
 */
export async function getSubscription(
  subscriptionId: string
): Promise<Stripe.Subscription> {
  return getStripe().subscriptions.retrieve(subscriptionId);
}

/**
 * Verify webhook signature
 */
export function constructWebhookEvent(
  payload: string | Buffer,
  signature: string,
  secret: string
): Stripe.Event {
  return getStripe().webhooks.constructEvent(payload, signature, secret);
}

// =============================================================================
// Types
// =============================================================================

export type { Stripe };
