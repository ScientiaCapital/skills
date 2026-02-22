# shadcn/ui Setup with Tailwind v4

> Deep-dive reference for shadcn/ui configuration, theming, and component customization
> with Tailwind CSS v4 and Next.js App Router. Load when setting up a component library
> or customizing shadcn/ui components.

---

## Table of Contents

1. [Installation](#installation)
2. [@theme inline Configuration](#theme-inline-configuration)
3. [CLI Usage](#cli-usage)
4. [Component Styling](#component-styling)
5. [tw-animate-css Setup](#tw-animate-css-setup)
6. [Dark Mode](#dark-mode)
7. [Customizing Components](#customizing-components)
8. [Radix vs Base UI](#radix-vs-base-ui)
9. [cn() Utility](#cn-utility)
10. [Theming System](#theming-system)
11. [Component Styles System](#component-styles-system)

---

## Installation

### Next.js App Router + Tailwind v4

```bash
# 1. Create Next.js project with Tailwind
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir
cd my-app

# 2. Initialize shadcn/ui
npx shadcn@latest init
```

The init command will:
- Detect Tailwind v4 and configure `@theme inline` tokens
- Create `components.json` with path aliases
- Set up `src/lib/utils.ts` with the `cn()` helper
- Create `src/components/ui/` directory
- Install `tw-animate-css` (not `tailwindcss-animate`)

### components.json

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "",
    "css": "src/app/globals.css",
    "baseColor": "neutral",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  }
}
```

### Add Components

```bash
# Add individual components
npx shadcn@latest add button
npx shadcn@latest add card dialog table form input label

# Add multiple at once
npx shadcn@latest add button card dialog table form input label select textarea

# Add all components (not recommended — keep it lean)
npx shadcn@latest add --all
```

---

## @theme inline Configuration

shadcn/ui uses `@theme inline` to define design tokens as CSS variables without
generating Tailwind utility classes. Components reference these via `var()`.

```css
/* app/globals.css */
@import "tailwindcss";
@import "tw-animate-css";

@theme inline {
  /* Core surface colors */
  --color-background: oklch(1 0 0);
  --color-foreground: oklch(0.145 0 0);
  --color-card: oklch(1 0 0);
  --color-card-foreground: oklch(0.145 0 0);
  --color-popover: oklch(1 0 0);
  --color-popover-foreground: oklch(0.145 0 0);

  /* Interactive colors */
  --color-primary: oklch(0.205 0.042 264.695);
  --color-primary-foreground: oklch(0.985 0 0);
  --color-secondary: oklch(0.97 0.001 286.375);
  --color-secondary-foreground: oklch(0.205 0.042 264.695);
  --color-muted: oklch(0.97 0.001 286.375);
  --color-muted-foreground: oklch(0.556 0.017 285.938);
  --color-accent: oklch(0.97 0.001 286.375);
  --color-accent-foreground: oklch(0.205 0.042 264.695);
  --color-destructive: oklch(0.577 0.245 27.325);
  --color-destructive-foreground: oklch(0.985 0 0);

  /* Borders, inputs, focus rings */
  --color-border: oklch(0.922 0.004 286.375);
  --color-input: oklch(0.922 0.004 286.375);
  --color-ring: oklch(0.205 0.042 264.695);

  /* Charts */
  --color-chart-1: oklch(0.646 0.222 41.116);
  --color-chart-2: oklch(0.6 0.118 184.704);
  --color-chart-3: oklch(0.398 0.07 227.392);
  --color-chart-4: oklch(0.828 0.189 84.429);
  --color-chart-5: oklch(0.769 0.188 70.08);

  /* Sidebar */
  --color-sidebar: oklch(0.985 0 0);
  --color-sidebar-foreground: oklch(0.145 0 0);
  --color-sidebar-primary: oklch(0.205 0.042 264.695);
  --color-sidebar-primary-foreground: oklch(0.985 0 0);
  --color-sidebar-accent: oklch(0.97 0.001 286.375);
  --color-sidebar-accent-foreground: oklch(0.205 0.042 264.695);
  --color-sidebar-border: oklch(0.922 0.004 286.375);
  --color-sidebar-ring: oklch(0.205 0.042 264.695);

  /* Border radius system */
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
  --radius: 0.625rem;
}
```

---

## CLI Usage

### init — Initialize Project

```bash
npx shadcn@latest init
# Interactive prompts: style, base color, CSS path, aliases
```

### add — Add Components

```bash
npx shadcn@latest add [component...]

# Examples
npx shadcn@latest add button           # Single component
npx shadcn@latest add dialog sheet     # Multiple components
npx shadcn@latest add --all            # Everything (heavy)
npx shadcn@latest add --overwrite button  # Overwrite existing
```

### diff — Check for Updates

```bash
npx shadcn@latest diff
# Shows what changed since you added each component

npx shadcn@latest diff button
# Diff for a specific component
```

Use `diff` periodically to pull in bug fixes and improvements from upstream without
losing your customizations.

---

## Component Styling

### data-slot Attributes

Every shadcn/ui component exposes `data-slot` attributes — stable styling hooks that
parents can target without fragile className overrides.

```tsx
// Internal component definition
function Card({ className, ref, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      ref={ref}
      data-slot="card"
      className={cn("rounded-xl border bg-card text-card-foreground shadow-xs", className)}
      {...props}
    />
  )
}

function CardHeader({ className, ref, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      ref={ref}
      data-slot="card-header"
      className={cn("flex flex-col gap-1.5 p-6", className)}
      {...props}
    />
  )
}
```

**Styling from parent:**

```tsx
{/* Target all cards within this container */}
<div className="[&_[data-slot=card]]:shadow-lg [&_[data-slot=card-header]]:pb-2">
  <Card>
    <CardHeader>
      <CardTitle>Revenue</CardTitle>
    </CardHeader>
    <CardContent>$12,345</CardContent>
  </Card>
</div>
```

### No forwardRef (React 19)

All shadcn/ui components accept `ref` as a regular prop:

```tsx
function Input({ className, type, ref, ...props }: React.ComponentProps<"input">) {
  return (
    <input
      type={type}
      ref={ref}
      data-slot="input"
      className={cn(
        "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm",
        "file:border-0 file:bg-transparent file:text-sm file:font-medium",
        "placeholder:text-muted-foreground",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
        "disabled:cursor-not-allowed disabled:opacity-50",
        className
      )}
      {...props}
    />
  )
}
```

---

## tw-animate-css Setup

`tw-animate-css` replaces `tailwindcss-animate` for Tailwind v4 compatibility. It
provides pure CSS animations without a Tailwind plugin.

```bash
npm install tw-animate-css
```

```css
/* app/globals.css */
@import "tailwindcss";
@import "tw-animate-css";
```

### Available Animation Classes

```tsx
// Entrance animations
<div className="animate-in fade-in">Fade in</div>
<div className="animate-in fade-in slide-in-from-bottom-4">Fade + slide up</div>
<div className="animate-in zoom-in-95">Scale in</div>

// Exit animations
<div className="animate-out fade-out">Fade out</div>
<div className="animate-out fade-out slide-out-to-top-4">Fade + slide up exit</div>

// Duration and delay
<div className="animate-in fade-in duration-500 delay-200">Slow fade</div>
```

These classes are used internally by Dialog, Sheet, Dropdown, Popover, and other
animated components.

---

## Dark Mode

### CSS Variable Swap

Dark mode swaps `@theme inline` variables under the `.dark` class:

```css
.dark {
  --color-background: oklch(0.145 0 0);
  --color-foreground: oklch(0.985 0 0);
  --color-card: oklch(0.205 0.015 286.375);
  --color-card-foreground: oklch(0.985 0 0);
  --color-popover: oklch(0.205 0.015 286.375);
  --color-popover-foreground: oklch(0.985 0 0);
  --color-primary: oklch(0.922 0.004 286.375);
  --color-primary-foreground: oklch(0.205 0.042 264.695);
  --color-secondary: oklch(0.269 0.015 286.375);
  --color-secondary-foreground: oklch(0.985 0 0);
  --color-muted: oklch(0.269 0.015 286.375);
  --color-muted-foreground: oklch(0.708 0.012 285.938);
  --color-accent: oklch(0.269 0.015 286.375);
  --color-accent-foreground: oklch(0.985 0 0);
  --color-destructive: oklch(0.704 0.191 22.216);
  --color-destructive-foreground: oklch(0.985 0 0);
  --color-border: oklch(0.30 0.01 286.375);
  --color-input: oklch(0.30 0.01 286.375);
  --color-ring: oklch(0.556 0.017 285.938);

  --color-chart-1: oklch(0.488 0.243 264.376);
  --color-chart-2: oklch(0.696 0.17 162.48);
  --color-chart-3: oklch(0.769 0.188 70.08);
  --color-chart-4: oklch(0.627 0.265 303.9);
  --color-chart-5: oklch(0.645 0.246 16.439);

  --color-sidebar: oklch(0.205 0.015 286.375);
  --color-sidebar-foreground: oklch(0.985 0 0);
  --color-sidebar-primary: oklch(0.488 0.243 264.376);
  --color-sidebar-primary-foreground: oklch(0.985 0 0);
  --color-sidebar-accent: oklch(0.269 0.015 286.375);
  --color-sidebar-accent-foreground: oklch(0.985 0 0);
  --color-sidebar-border: oklch(0.30 0.01 286.375);
  --color-sidebar-ring: oklch(0.556 0.017 285.938);
}
```

### next-themes Integration

```bash
npm install next-themes
```

```tsx
// app/layout.tsx
import { ThemeProvider } from "next-themes"

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
```

---

## Customizing Components

### Extending (Preferred)

Wrap the shadcn component, adding your defaults. Preserves upstream updates.

```tsx
// components/app/submit-button.tsx
import { Button, type ButtonProps } from "@/components/ui/button"
import { Loader2 } from "lucide-react"

interface SubmitButtonProps extends ButtonProps {
  loading?: boolean
}

function SubmitButton({ loading, children, disabled, ...props }: SubmitButtonProps) {
  return (
    <Button disabled={disabled || loading} {...props}>
      {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
      {children}
    </Button>
  )
}

export { SubmitButton }
```

### Overriding (When Necessary)

Edit the component file in `components/ui/` directly. You own this code.

```tsx
// components/ui/button.tsx — add a new variant
const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
        // Custom variant
        success: "bg-green-600 text-white hover:bg-green-700",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  }
)
```

Use `npx shadcn@latest diff button` to see upstream changes and merge manually.

---

## Radix vs Base UI

shadcn/ui supports both Radix Primitives and Base UI (MUI) as underlying headless
component libraries.

| Feature | Radix Primitives | Base UI |
|---------|-----------------|---------|
| Maintainer | WorkOS | MUI |
| Philosophy | Accessible, unstyled | Headless hooks |
| API | Compound components | Hooks + render props |
| Bundle | Per-component packages | Single package |
| Use when | Default choice, stable API | Already in MUI ecosystem |

**Recommendation:** Stick with Radix (default) unless your project already uses MUI.
shadcn's Radix integration is more mature and tested.

---

## cn() Utility

Combines `clsx` (conditional classes) with `tailwind-merge` (deduplication).

```ts
// lib/utils.ts
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### Why Both?

- **clsx** handles conditionals: `clsx("base", isActive && "bg-blue-500", { "opacity-50": disabled })`
- **twMerge** resolves conflicts: `twMerge("px-4 py-2", "px-6")` returns `"px-6 py-2"`

Together: safe, conflict-free className composition.

```tsx
// Example: conditional + override-safe
<div className={cn(
  "flex items-center gap-2 rounded-md p-3",
  variant === "danger" && "bg-destructive text-destructive-foreground",
  variant === "success" && "bg-green-50 text-green-900",
  className  // caller can override any of the above
)} />
```

---

## Theming System

### OKLCH Color Tokens

All colors use OKLCH for perceptual uniformity. When creating custom themes, maintain
the same token names — components reference them by variable name.

```css
/* Blue theme */
@theme inline {
  --color-primary: oklch(0.55 0.15 250);
  --color-primary-foreground: oklch(0.98 0.01 250);
}

/* Green theme */
@theme inline {
  --color-primary: oklch(0.55 0.15 145);
  --color-primary-foreground: oklch(0.98 0.01 145);
}
```

### Border Radius System

```css
@theme inline {
  --radius: 0.625rem;           /* Base value — change this to scale everything */
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
}
```

Set `--radius` to `0` for sharp corners, `1rem` for very rounded, `9999px` for pill
shapes. All components scale proportionally.

### Font System

```css
@theme inline {
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;
}
```

Pair with `next/font` for optimal loading:

```tsx
// app/layout.tsx
import { Inter, JetBrains_Mono } from "next/font/google"

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" })
const jetbrains = JetBrains_Mono({ subsets: ["latin"], variable: "--font-mono" })

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrains.variable}`}>
      <body className="font-sans">{children}</body>
    </html>
  )
}
```

---

## Component Styles System

### File Organization

```
src/
  components/
    ui/             # shadcn/ui primitives (owned by you, updated via CLI)
      button.tsx
      card.tsx
      dialog.tsx
      table.tsx
    app/            # Application-specific compositions
      submit-button.tsx
      kpi-card.tsx
      user-nav.tsx
      data-table.tsx
```

### Rules

1. **`ui/`** — Pure shadcn components. Customize directly but track diffs.
2. **`app/`** — Your compositions that import from `ui/`. Business logic lives here.
3. **Never modify `ui/` components for a single use case** — wrap in `app/` instead.
4. **Shared variants** belong in `ui/`. Page-specific styling belongs in the page.

### Adding a New Themed Component

```tsx
// components/ui/status-badge.tsx
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const statusBadgeVariants = cva(
  "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
  {
    variants: {
      status: {
        active: "bg-green-50 text-green-700 dark:bg-green-950 dark:text-green-300",
        inactive: "bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300",
        pending: "bg-yellow-50 text-yellow-700 dark:bg-yellow-950 dark:text-yellow-300",
        error: "bg-red-50 text-red-700 dark:bg-red-950 dark:text-red-300",
      },
    },
    defaultVariants: { status: "active" },
  }
)

function StatusBadge({
  className,
  status,
  ...props
}: React.ComponentProps<"span"> & VariantProps<typeof statusBadgeVariants>) {
  return (
    <span
      data-slot="status-badge"
      className={cn(statusBadgeVariants({ status, className }))}
      {...props}
    />
  )
}

export { StatusBadge, statusBadgeVariants }
```
