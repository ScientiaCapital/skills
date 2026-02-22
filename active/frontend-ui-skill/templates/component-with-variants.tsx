/**
 * shadcn-style component template — Alert with cva variants
 *
 * Demonstrates:
 * - cva with multiple variant axes (variant, size)
 * - React 19: ref as prop, no forwardRef
 * - data-slot attribute for parent style overrides
 * - cn() class merging
 * - VariantProps type extraction
 * - Default variants
 * - asChild / Slot polymorphic rendering
 *
 * Usage:
 *   <Alert variant="destructive" size="lg">Something went wrong.</Alert>
 *   <Alert variant="success" asChild><a href="/status">All systems go.</a></Alert>
 */

import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import {
  AlertCircle,
  AlertTriangle,
  CheckCircle2,
  Info,
  type LucideIcon,
} from "lucide-react"
import { cn } from "@/lib/utils"

// ── Variant definitions ──────────────────────────────────────

const alertVariants = cva(
  "relative flex w-full items-start gap-3 rounded-lg border p-4 text-sm [&>svg]:shrink-0",
  {
    variants: {
      variant: {
        default:
          "border-border bg-background text-foreground [&>svg]:text-foreground",
        destructive:
          "border-destructive/50 bg-destructive/5 text-destructive [&>svg]:text-destructive",
        warning:
          "border-amber-500/50 bg-amber-500/5 text-amber-700 dark:text-amber-400 [&>svg]:text-amber-600 dark:[&>svg]:text-amber-400",
        success:
          "border-emerald-500/50 bg-emerald-500/5 text-emerald-700 dark:text-emerald-400 [&>svg]:text-emerald-600 dark:[&>svg]:text-emerald-400",
      },
      size: {
        sm: "gap-2 p-3 text-xs [&>svg]:size-4",
        default: "gap-3 p-4 text-sm [&>svg]:size-5",
        lg: "gap-4 p-5 text-base [&>svg]:size-6",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

// ── Icon map ─────────────────────────────────────────────────

const iconMap: Record<string, LucideIcon> = {
  default: Info,
  destructive: AlertCircle,
  warning: AlertTriangle,
  success: CheckCircle2,
}

// ── Types ────────────────────────────────────────────────────

type AlertProps = React.ComponentProps<"div"> &
  VariantProps<typeof alertVariants> & {
    /** Render as a different element via Radix Slot */
    asChild?: boolean
    /** Override the default icon for this variant */
    icon?: LucideIcon
  }

// ── Component ────────────────────────────────────────────────

function Alert({
  className,
  variant,
  size,
  asChild = false,
  icon,
  children,
  ref,
  ...props
}: AlertProps) {
  const Comp = asChild ? Slot : "div"
  const IconComp = icon ?? iconMap[variant ?? "default"]

  return (
    <Comp
      ref={ref}
      data-slot="alert"
      role="alert"
      className={cn(alertVariants({ variant, size, className }))}
      {...props}
    >
      <IconComp aria-hidden="true" />
      <div data-slot="alert-content" className="flex-1">
        {children}
      </div>
    </Comp>
  )
}

// ── Sub-components ───────────────────────────────────────────

function AlertTitle({
  className,
  ref,
  ...props
}: React.ComponentProps<"h5">) {
  return (
    <h5
      ref={ref}
      data-slot="alert-title"
      className={cn("mb-1 font-medium leading-none tracking-tight", className)}
      {...props}
    />
  )
}

function AlertDescription({
  className,
  ref,
  ...props
}: React.ComponentProps<"div">) {
  return (
    <div
      ref={ref}
      data-slot="alert-description"
      className={cn("text-sm [&_p]:leading-relaxed", className)}
      {...props}
    />
  )
}

export { Alert, AlertTitle, AlertDescription, alertVariants }
export type { AlertProps }
