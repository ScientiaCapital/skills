/**
 * 3-Tier SaaS pricing page — monthly/annual toggle
 *
 * Features:
 * - Plan data as typed const array for easy modification
 * - Monthly/annual toggle with Switch
 * - Professional plan highlighted as "Most Popular"
 * - Feature comparison table below cards
 * - Responsive: single column mobile, 3-col grid on lg
 * - Accessible: semantic markup, keyboard-friendly toggle
 *
 * Dependencies:
 *   npx shadcn@latest add card button badge switch table
 *   npm install lucide-react
 */

"use client"

import { useState } from "react"
import { Check, Minus } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Switch } from "@/components/ui/switch"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { cn } from "@/lib/utils"

// ── Plan data ────────────────────────────────────────────────

interface Plan {
  name: string
  description: string
  monthlyPrice: number | null // null = custom pricing
  annualPrice: number | null
  cta: string
  ctaVariant: "default" | "outline"
  highlighted: boolean
  features: string[]
}

const plans: Plan[] = [
  {
    name: "Starter",
    description: "For individuals and small projects getting started.",
    monthlyPrice: 29,
    annualPrice: 24,
    cta: "Start Free Trial",
    ctaVariant: "outline",
    highlighted: false,
    features: [
      "Up to 1,000 customers",
      "Basic analytics",
      "Email support",
      "1 team member",
      "API access",
    ],
  },
  {
    name: "Professional",
    description: "For growing teams that need more power and collaboration.",
    monthlyPrice: 79,
    annualPrice: 64,
    cta: "Start Free Trial",
    ctaVariant: "default",
    highlighted: true,
    features: [
      "Up to 25,000 customers",
      "Advanced analytics & reports",
      "Priority email & chat support",
      "Up to 10 team members",
      "API access + webhooks",
      "Custom integrations",
      "Audit log",
    ],
  },
  {
    name: "Enterprise",
    description: "For large organizations with custom requirements.",
    monthlyPrice: null,
    annualPrice: null,
    cta: "Contact Sales",
    ctaVariant: "outline",
    highlighted: false,
    features: [
      "Unlimited customers",
      "Custom analytics & BI export",
      "Dedicated account manager",
      "Unlimited team members",
      "Full API + webhooks + SSO",
      "Custom integrations",
      "Audit log + SIEM",
      "SLA & uptime guarantee",
      "On-premise deployment option",
    ],
  },
] as const satisfies readonly Plan[]

// ── Feature comparison data ──────────────────────────────────

interface ComparisonRow {
  feature: string
  starter: string | boolean
  professional: string | boolean
  enterprise: string | boolean
}

const comparisonData: ComparisonRow[] = [
  { feature: "Customers", starter: "1,000", professional: "25,000", enterprise: "Unlimited" },
  { feature: "Team members", starter: "1", professional: "10", enterprise: "Unlimited" },
  { feature: "Analytics", starter: "Basic", professional: "Advanced", enterprise: "Custom + BI" },
  { feature: "API access", starter: true, professional: true, enterprise: true },
  { feature: "Webhooks", starter: false, professional: true, enterprise: true },
  { feature: "SSO / SAML", starter: false, professional: false, enterprise: true },
  { feature: "Custom integrations", starter: false, professional: true, enterprise: true },
  { feature: "Audit log", starter: false, professional: true, enterprise: true },
  { feature: "SLA guarantee", starter: false, professional: false, enterprise: true },
  { feature: "Support", starter: "Email", professional: "Email & chat", enterprise: "Dedicated AM" },
]

// ── Pricing Page Component ───────────────────────────────────

export function PricingPage() {
  const [annual, setAnnual] = useState(false)

  return (
    <section className="mx-auto max-w-6xl px-4 py-16 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mx-auto max-w-2xl text-center">
        <h1 className="text-3xl font-bold tracking-tight sm:text-4xl lg:text-5xl">
          Simple, transparent pricing
        </h1>
        <p className="mt-4 text-lg text-muted-foreground">
          Start free. Scale as you grow. No hidden fees.
        </p>
      </div>

      {/* Billing toggle */}
      <div className="mt-10 flex items-center justify-center gap-3">
        <span
          className={cn(
            "text-sm font-medium",
            !annual ? "text-foreground" : "text-muted-foreground"
          )}
        >
          Monthly
        </span>
        <Switch
          checked={annual}
          onCheckedChange={setAnnual}
          aria-label="Toggle annual billing"
        />
        <span
          className={cn(
            "text-sm font-medium",
            annual ? "text-foreground" : "text-muted-foreground"
          )}
        >
          Annual
        </span>
        {annual && (
          <Badge variant="secondary" className="ml-1">
            Save 20%
          </Badge>
        )}
      </div>

      {/* Plan cards */}
      <div className="mt-12 grid grid-cols-1 gap-6 lg:grid-cols-3 lg:items-start">
        {plans.map((plan) => (
          <PricingCard key={plan.name} plan={plan} annual={annual} />
        ))}
      </div>

      {/* Feature comparison */}
      <div className="mt-20">
        <h2 className="mb-8 text-center text-2xl font-bold tracking-tight">
          Compare plans
        </h2>
        <FeatureComparison />
      </div>
    </section>
  )
}

// ── Pricing Card ─────────────────────────────────────────────

function PricingCard({ plan, annual }: { plan: Plan; annual: boolean }) {
  const price = annual ? plan.annualPrice : plan.monthlyPrice
  const isCustom = price === null

  return (
    <Card
      className={cn(
        "relative flex flex-col",
        plan.highlighted && "ring-2 ring-primary shadow-lg"
      )}
    >
      {plan.highlighted && (
        <Badge className="absolute -top-3 left-1/2 -translate-x-1/2">
          Most Popular
        </Badge>
      )}

      <CardHeader className="pb-4">
        <CardTitle className="text-xl">{plan.name}</CardTitle>
        <CardDescription>{plan.description}</CardDescription>
      </CardHeader>

      <CardContent className="flex-1">
        {/* Price */}
        <div className="mb-6">
          {isCustom ? (
            <p className="text-4xl font-bold tracking-tight">Custom</p>
          ) : (
            <div className="flex items-baseline gap-1">
              <span className="text-4xl font-bold tracking-tight">
                ${price}
              </span>
              <span className="text-sm text-muted-foreground">/month</span>
            </div>
          )}
          {!isCustom && annual && (
            <p className="mt-1 text-sm text-muted-foreground">
              Billed annually (${price! * 12}/yr)
            </p>
          )}
        </div>

        {/* Feature list */}
        <ul className="space-y-3" role="list">
          {plan.features.map((feature) => (
            <li key={feature} className="flex items-start gap-3 text-sm">
              <Check
                className="mt-0.5 size-4 shrink-0 text-primary"
                aria-hidden="true"
              />
              {feature}
            </li>
          ))}
        </ul>
      </CardContent>

      <CardFooter className="pt-4">
        <Button
          variant={plan.ctaVariant}
          className="w-full"
          size="lg"
        >
          {plan.cta}
        </Button>
      </CardFooter>
    </Card>
  )
}

// ── Feature Comparison Table ─────────────────────────────────

function FeatureComparison() {
  return (
    <div className="overflow-x-auto rounded-lg border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[200px]">Feature</TableHead>
            <TableHead className="text-center">Starter</TableHead>
            <TableHead className="text-center font-semibold text-primary">
              Professional
            </TableHead>
            <TableHead className="text-center">Enterprise</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {comparisonData.map((row) => (
            <TableRow key={row.feature}>
              <TableCell className="font-medium">{row.feature}</TableCell>
              <TableCell className="text-center">
                <ComparisonCell value={row.starter} />
              </TableCell>
              <TableCell className="text-center">
                <ComparisonCell value={row.professional} />
              </TableCell>
              <TableCell className="text-center">
                <ComparisonCell value={row.enterprise} />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}

function ComparisonCell({ value }: { value: string | boolean }) {
  if (typeof value === "string") {
    return <span className="text-sm">{value}</span>
  }

  if (value) {
    return (
      <Check
        className="mx-auto size-4 text-primary"
        aria-label="Included"
      />
    )
  }

  return (
    <Minus
      className="mx-auto size-4 text-muted-foreground/40"
      aria-label="Not included"
    />
  )
}
