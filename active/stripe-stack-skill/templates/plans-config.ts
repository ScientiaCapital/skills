/**
 * Subscription Plans Configuration
 *
 * Copy to: src/lib/stripe/plans.ts
 *
 * Features:
 * - Type-safe plan definitions
 * - Environment variable price IDs (test→live switching)
 * - Feature lists for UI
 * - Usage limits per plan
 */

// =============================================================================
// Plan Definitions
// =============================================================================

export const PLANS = {
  free: {
    id: 'free',
    name: 'Free',
    description: 'Get started with basic features',
    priceMonthly: 0,
    priceAnnual: 0,
    priceIdMonthly: null,
    priceIdAnnual: null,
    features: [
      '3 requests per month',
      'Basic support',
      'Community access',
    ],
    limits: {
      requestsMonthly: 3,
      apiAccess: false,
      prioritySupport: false,
    },
  },

  starter: {
    id: 'starter',
    name: 'Starter',
    description: 'For individuals getting started',
    priceMonthly: 2900, // $29
    priceAnnual: 29000, // $290 (2 months free)
    priceIdMonthly: process.env.STRIPE_PRICE_STARTER_MONTHLY || 'price_starter_monthly',
    priceIdAnnual: process.env.STRIPE_PRICE_STARTER_ANNUAL || 'price_starter_annual',
    features: [
      '50 requests per month',
      'Email support',
      'Basic analytics',
    ],
    limits: {
      requestsMonthly: 50,
      apiAccess: false,
      prioritySupport: false,
    },
  },

  pro: {
    id: 'pro',
    name: 'Pro',
    description: 'For professionals and small teams',
    priceMonthly: 7900, // $79
    priceAnnual: 79000, // $790 (2 months free)
    priceIdMonthly: process.env.STRIPE_PRICE_PRO_MONTHLY || 'price_pro_monthly',
    priceIdAnnual: process.env.STRIPE_PRICE_PRO_ANNUAL || 'price_pro_annual',
    features: [
      '500 requests per month',
      'Priority support',
      'Advanced analytics',
      'API access',
    ],
    limits: {
      requestsMonthly: 500,
      apiAccess: true,
      prioritySupport: true,
    },
    popular: true, // Show "Most Popular" badge
  },

  business: {
    id: 'business',
    name: 'Business',
    description: 'For growing companies',
    priceMonthly: 19900, // $199
    priceAnnual: 199000, // $1990 (2 months free)
    priceIdMonthly: process.env.STRIPE_PRICE_BUSINESS_MONTHLY || 'price_business_monthly',
    priceIdAnnual: process.env.STRIPE_PRICE_BUSINESS_ANNUAL || 'price_business_annual',
    features: [
      'Unlimited requests',
      '24/7 phone support',
      'Custom integrations',
      'Dedicated account manager',
      'SLA guarantee',
    ],
    limits: {
      requestsMonthly: -1, // -1 = unlimited
      apiAccess: true,
      prioritySupport: true,
    },
  },

  enterprise: {
    id: 'enterprise',
    name: 'Enterprise',
    description: 'Custom solutions for large organizations',
    priceMonthly: 0, // Custom pricing
    priceAnnual: 0,
    priceIdMonthly: null, // Contact sales
    priceIdAnnual: null,
    features: [
      'Everything in Business',
      'Custom contracts',
      'On-premise deployment',
      'Custom SLAs',
      'Dedicated support team',
    ],
    limits: {
      requestsMonthly: -1,
      apiAccess: true,
      prioritySupport: true,
    },
    contactSales: true,
  },
} as const;

// =============================================================================
// Types
// =============================================================================

export type PlanId = keyof typeof PLANS;
export type Plan = (typeof PLANS)[PlanId];

// =============================================================================
// Helper Functions
// =============================================================================

/**
 * Get plan by ID
 */
export function getPlan(id: PlanId | string): Plan {
  return PLANS[id as PlanId] || PLANS.free;
}

/**
 * Get all plans as array (for pricing page)
 */
export function getAllPlans(): Plan[] {
  return Object.values(PLANS);
}

/**
 * Get paid plans only
 */
export function getPaidPlans(): Plan[] {
  return Object.values(PLANS).filter((p) => p.priceMonthly > 0);
}

/**
 * Check if user has reached usage limit
 */
export function hasReachedLimit(
  planId: PlanId,
  currentUsage: number
): boolean {
  const plan = getPlan(planId);
  const limit = plan.limits.requestsMonthly;

  if (limit === -1) return false; // Unlimited
  return currentUsage >= limit;
}

/**
 * Get remaining usage
 */
export function getRemainingUsage(
  planId: PlanId,
  currentUsage: number
): number | 'unlimited' {
  const plan = getPlan(planId);
  const limit = plan.limits.requestsMonthly;

  if (limit === -1) return 'unlimited';
  return Math.max(0, limit - currentUsage);
}

/**
 * Format price for display
 */
export function formatPrice(cents: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(cents / 100);
}

/**
 * Get price ID for billing period
 */
export function getPriceId(
  planId: PlanId,
  period: 'monthly' | 'annual'
): string | null {
  const plan = getPlan(planId);
  return period === 'monthly' ? plan.priceIdMonthly : plan.priceIdAnnual;
}

/**
 * Calculate savings for annual billing
 */
export function getAnnualSavings(planId: PlanId): number {
  const plan = getPlan(planId);
  const monthlyTotal = plan.priceMonthly * 12;
  return monthlyTotal - plan.priceAnnual;
}
