# Tailwind CSS v4 — Complete Setup Guide

> Deep-dive reference for Tailwind v4 CSS-first configuration. Load when setting up a
> new project or migrating from v3.

---

## Table of Contents

1. [Installation](#installation)
2. [@theme Directive Deep Dive](#theme-directive-deep-dive)
3. [@theme inline for shadcn/ui](#theme-inline-for-shadcnui)
4. [@source Directive](#source-directive)
5. [Container Queries](#container-queries)
6. [Dark Mode](#dark-mode)
7. [Migration from v3 to v4](#migration-from-v3-to-v4)
8. [Custom Plugins](#custom-plugins-in-v4)
9. [Performance](#performance)

---

## Installation

### Next.js with Vite Plugin (Recommended)

The Vite plugin is **10x faster** than PostCSS for full builds. Use this for new
projects.

```bash
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir
cd my-app
```

```bash
npm install tailwindcss @tailwindcss/vite
```

```ts
// next.config.ts
import tailwindcss from "@tailwindcss/vite"
import type { NextConfig } from "next"

const nextConfig: NextConfig = {
  plugins: [tailwindcss()],
}

export default nextConfig
```

```css
/* app/globals.css */
@import "tailwindcss";
```

### Next.js with PostCSS (Fallback)

Use when Vite plugin is incompatible with your build pipeline.

```bash
npm install tailwindcss @tailwindcss/postcss
```

```js
// postcss.config.mjs
export default {
  plugins: {
    "@tailwindcss/postcss": {},
  },
}
```

```css
/* app/globals.css */
@import "tailwindcss";
```

### Verify Installation

```bash
# Should see Tailwind classes compiled in output
npm run dev
# Check: no tailwind.config.js needed — config lives in CSS
```

---

## @theme Directive Deep Dive

The `@theme` directive replaces `tailwind.config.js`. All design tokens are defined in
CSS, generating corresponding utility classes automatically.

### Colors (OKLCH)

Tailwind v4 uses OKLCH — perceptually uniform, better for generating consistent
palettes and accessible contrast ratios.

```css
@theme {
  /* Brand palette */
  --color-brand-50: oklch(0.97 0.01 250);
  --color-brand-100: oklch(0.93 0.03 250);
  --color-brand-200: oklch(0.86 0.06 250);
  --color-brand-300: oklch(0.76 0.10 250);
  --color-brand-400: oklch(0.66 0.13 250);
  --color-brand-500: oklch(0.55 0.15 250);
  --color-brand-600: oklch(0.47 0.14 250);
  --color-brand-700: oklch(0.39 0.12 250);
  --color-brand-800: oklch(0.32 0.09 250);
  --color-brand-900: oklch(0.26 0.07 250);
  --color-brand-950: oklch(0.18 0.05 250);

  /* Semantic colors */
  --color-success: oklch(0.60 0.15 145);
  --color-warning: oklch(0.75 0.15 75);
  --color-danger: oklch(0.55 0.20 25);
  --color-info: oklch(0.60 0.12 250);
}
```

**Usage:** `bg-brand-500`, `text-danger`, `border-success`.

OKLCH channels: `L` (lightness 0-1), `C` (chroma 0-0.4), `H` (hue 0-360).
Rule of thumb: keep `C` and `H` constant, vary `L` for shade scales.

### Spacing

```css
@theme {
  /* Extend or override the default spacing scale */
  --spacing-4\.5: 1.125rem;   /* 18px */
  --spacing-13: 3.25rem;      /* 52px */
  --spacing-15: 3.75rem;      /* 60px */
  --spacing-128: 32rem;       /* 512px */
}
```

**Usage:** `p-4.5`, `mt-13`, `w-128`.

### Typography

```css
@theme {
  /* Font families */
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;
  --font-display: "Cal Sans", "Inter", sans-serif;

  /* Font sizes: [size, line-height] */
  --text-2xs: 0.625rem;
  --text-2xs--line-height: 0.875rem;

  /* Letter spacing */
  --tracking-tighter: -0.04em;
  --tracking-tight: -0.02em;

  /* Font weight */
  --font-weight-semibold: 600;
}
```

**Usage:** `font-display`, `text-2xs`, `tracking-tight`.

### Breakpoints

```css
@theme {
  --breakpoint-xs: 475px;
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;
  --breakpoint-3xl: 1920px;
}
```

**Usage:** `xs:flex`, `3xl:grid-cols-4`.

### Animations

```css
@theme {
  /* Keyframes */
  --animate-slide-in: slide-in 0.3s ease-out;
  --animate-slide-out: slide-out 0.2s ease-in;
  --animate-fade-in: fade-in 0.2s ease-out;
  --animate-scale-in: scale-in 0.15s ease-out;
}

@keyframes slide-in {
  from { transform: translateX(-100%); }
  to { transform: translateX(0); }
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scale-in {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
```

**Usage:** `animate-slide-in`, `animate-fade-in`.

### Full @theme Example

```css
@theme {
  --color-primary: oklch(0.55 0.15 250);
  --color-primary-foreground: oklch(0.98 0.01 250);
  --color-secondary: oklch(0.90 0.03 250);
  --color-secondary-foreground: oklch(0.20 0.02 250);
  --color-muted: oklch(0.93 0.01 250);
  --color-muted-foreground: oklch(0.50 0.02 250);
  --color-accent: oklch(0.93 0.02 250);
  --color-accent-foreground: oklch(0.20 0.02 250);
  --color-destructive: oklch(0.55 0.20 25);
  --color-destructive-foreground: oklch(0.98 0.01 25);

  --font-sans: "Inter", system-ui, sans-serif;
  --breakpoint-xs: 475px;
  --animate-fade-in: fade-in 0.2s ease-out;
}
```

---

## @theme inline for shadcn/ui

`@theme inline` defines CSS custom properties **without** generating Tailwind utility
classes for them. Use this for tokens that shadcn/ui components reference directly
via `var()` but that do not need standalone utility classes (e.g., `bg-sidebar`).

```css
@import "tailwindcss";

@theme inline {
  --color-background: oklch(1 0 0);
  --color-foreground: oklch(0.145 0 0);
  --color-card: oklch(1 0 0);
  --color-card-foreground: oklch(0.145 0 0);
  --color-popover: oklch(1 0 0);
  --color-popover-foreground: oklch(0.145 0 0);
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
  --color-border: oklch(0.922 0.004 286.375);
  --color-input: oklch(0.922 0.004 286.375);
  --color-ring: oklch(0.205 0.042 264.695);

  --color-sidebar: oklch(0.985 0 0);
  --color-sidebar-foreground: oklch(0.145 0 0);
  --color-sidebar-primary: oklch(0.205 0.042 264.695);
  --color-sidebar-primary-foreground: oklch(0.985 0 0);
  --color-sidebar-accent: oklch(0.97 0.001 286.375);
  --color-sidebar-accent-foreground: oklch(0.205 0.042 264.695);
  --color-sidebar-border: oklch(0.922 0.004 286.375);
  --color-sidebar-ring: oklch(0.205 0.042 264.695);

  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
  --radius: 0.625rem;
}
```

**Key difference:** `@theme` generates utilities (e.g., `bg-brand-500`). `@theme inline`
only sets CSS variables (consumed by `var(--color-sidebar)` in component code). Use
`@theme inline` for shadcn/ui tokens; use `@theme` for your own extended scales.

---

## @source Directive

Replaces the `content` array from `tailwind.config.js`. Tells Tailwind which files to
scan for class names.

```css
@import "tailwindcss";

/* Scan a monorepo package */
@source "../packages/ui/src/**/*.{ts,tsx}";

/* Scan a component library */
@source "./node_modules/@acme/ui/dist/**/*.js";

/* Disable default source detection */
@source none;
@source "./src/**/*.tsx";
```

Default behavior (no `@source`): scans all files in the project root, respecting
`.gitignore`. Add `@source` only when you need to scan outside the default detection
range (e.g., monorepo packages, node_modules libraries).

---

## Container Queries

Built-in to Tailwind v4 — no plugin required.

### Basic Usage

```tsx
// Parent defines the container
<div className="@container">
  {/* Children respond to parent width, not viewport */}
  <div className="grid grid-cols-1 @sm:grid-cols-2 @lg:grid-cols-3 gap-4">
    <KPICard />
    <KPICard />
    <KPICard />
  </div>
</div>
```

### Named Containers

```tsx
<div className="@container/sidebar">
  <nav className="flex flex-col @sm/sidebar:flex-row gap-2">
    <NavItem />
    <NavItem />
  </nav>
</div>
```

### Container Query Breakpoints

| Prefix | Min Width |
|--------|-----------|
| `@xs:` | 320px |
| `@sm:` | 384px |
| `@md:` | 448px |
| `@lg:` | 512px |
| `@xl:` | 576px |
| `@2xl:` | 672px |
| `@3xl:` | 768px |
| `@4xl:` | 896px |
| `@5xl:` | 1024px |

### Min and Max Container Queries

```tsx
{/* Only apply between sm and lg container width */}
<div className="@min-sm:@max-lg:bg-blue-100">
  Highlighted at medium container sizes
</div>
```

### Practical Pattern — Responsive Card

```tsx
function MetricCard({ title, value, trend }: MetricCardProps) {
  return (
    <div className="@container">
      <div className="flex flex-col @sm:flex-row @sm:items-center gap-2 p-4 rounded-lg border">
        <div className="flex-1">
          <p className="text-sm text-muted-foreground">{title}</p>
          <p className="text-2xl @sm:text-3xl font-bold">{value}</p>
        </div>
        <div className="@sm:text-right">
          <TrendBadge trend={trend} />
        </div>
      </div>
    </div>
  )
}
```

---

## Dark Mode

Tailwind v4 dark mode uses CSS custom properties and the `.dark` class strategy by
default.

### Setup with CSS Custom Properties

```css
@import "tailwindcss";

@theme inline {
  --color-background: oklch(1 0 0);
  --color-foreground: oklch(0.145 0 0);
  --color-card: oklch(1 0 0);
  --color-card-foreground: oklch(0.145 0 0);
  --color-border: oklch(0.922 0.004 286.375);
}

.dark {
  --color-background: oklch(0.145 0 0);
  --color-foreground: oklch(0.985 0 0);
  --color-card: oklch(0.205 0.015 286.375);
  --color-card-foreground: oklch(0.985 0 0);
  --color-border: oklch(0.30 0.01 286.375);
}
```

### Theme Toggle Component

```tsx
"use client"

import { useTheme } from "next-themes"
import { Moon, Sun } from "lucide-react"
import { Button } from "@/components/ui/button"

function ThemeToggle() {
  const { theme, setTheme } = useTheme()

  return (
    <Button
      variant="ghost"
      size="sm"
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
      aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
    >
      <Sun className="h-4 w-4 rotate-0 scale-100 transition dark:rotate-90 dark:scale-0" />
      <Moon className="absolute h-4 w-4 rotate-90 scale-0 transition dark:rotate-0 dark:scale-100" />
    </Button>
  )
}
```

### next-themes Setup

```tsx
// app/layout.tsx
import { ThemeProvider } from "next-themes"

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
```

---

## Migration from v3 to v4

### Automated Upgrade Tool

```bash
npx @tailwindcss/upgrade
```

This handles most mechanical changes: config migration, import syntax, utility renames.
Review the diff carefully after running.

### Breaking Changes

| Category | v3 | v4 |
|----------|----|----|
| Config | `tailwind.config.js` | `@theme` in CSS |
| Import | `@tailwind base/components/utilities` | `@import "tailwindcss"` |
| Content | `content: ["./src/**/*.tsx"]` | `@source` directive or auto-detection |
| Colors | HSL / hex | OKLCH |
| Plugins | `require("plugin")` in config | CSS `@plugin` directive |

### Renamed Utilities

These are **scale shifts** — the visual output changes to match the new name:

| v3 Class | v4 Class | Notes |
|----------|----------|-------|
| `shadow-sm` | `shadow-xs` | Old `shadow-sm` is now smaller |
| `shadow` | `shadow-sm` | Default shadow shifted down |
| `shadow-md` | `shadow` | And so on up the scale |
| `blur-sm` | `blur-xs` | Same shift pattern |
| `blur` | `blur-sm` | |
| `rounded-sm` | `rounded-xs` | |
| `rounded` | `rounded-sm` | |
| `ring-offset-*` | `ring-offset:*` | Becomes a variant, not a utility |
| `drop-shadow-sm` | `drop-shadow-xs` | Same shift as shadow |
| `outline-none` | `outline-hidden` | `outline-none` now literally means none |

### Removed Features

- **`@apply` in external CSS** — Still works inside `.css` files imported via
  `@import`, but discouraged. Prefer component-level className composition.
- **`safelist`** — Use `@source "inline"` for dynamic classes, or spell out classes
  in comments for scanning.
- **`darkMode: "class"` config** — Automatic. `.dark` class strategy is the default.
- **`theme.extend`** — Just use `@theme` directly. New tokens merge with defaults.
- **`screens`** — Renamed to `--breakpoint-*` in `@theme`.
- **Color opacity modifier with `/`** — Still works but native `oklch()` with alpha
  channel is preferred: `oklch(0.55 0.15 250 / 0.5)`.

### Step-by-Step Manual Migration

1. **Delete `tailwind.config.js`** (after extracting values)
2. **Replace imports** in CSS entry file:
   ```css
   /* Before */
   @tailwind base;
   @tailwind components;
   @tailwind utilities;

   /* After */
   @import "tailwindcss";
   ```
3. **Move theme values** to `@theme`:
   ```css
   @theme {
     --color-primary: oklch(0.55 0.15 250);
     --font-sans: "Inter", system-ui, sans-serif;
   }
   ```
4. **Update renamed utilities** in components (see table above)
5. **Replace `content` array** with `@source` if needed
6. **Update plugins** to `@plugin` syntax or remove if built-in now (container
   queries, aspect-ratio, etc.)
7. **Test dark mode** — Ensure `.dark` class swaps CSS variables correctly

---

## Custom Plugins in v4

### CSS @plugin Directive

```css
@plugin "@tailwindcss/typography";
@plugin "@tailwindcss/forms";
```

### Custom Plugin (JS)

```js
// plugins/text-shadow.js
export default function textShadowPlugin({ matchUtilities, theme }) {
  matchUtilities(
    {
      "text-shadow": (value) => ({
        textShadow: value,
      }),
    },
    { values: theme("textShadow") }
  )
}
```

```css
@plugin "./plugins/text-shadow.js";

@theme {
  --text-shadow-sm: 0 1px 2px oklch(0 0 0 / 0.1);
  --text-shadow-md: 0 2px 4px oklch(0 0 0 / 0.15);
  --text-shadow-lg: 0 4px 8px oklch(0 0 0 / 0.2);
}
```

**Usage:** `text-shadow-sm`, `text-shadow-lg`.

### Built-In (No Plugin Needed in v4)

These previously required plugins but are now native:
- Container queries (`@container`)
- Aspect ratio (`aspect-video`, `aspect-square`)
- Typography prose (still needs `@tailwindcss/typography` for full feature set)

---

## Performance

### Build Size

Tailwind v4 produces **~70% smaller CSS** than v3 for the same project. The new engine
uses a single-pass compiler with better dead code elimination.

| Metric | v3 | v4 |
|--------|----|----|
| CSS output (typical SaaS) | ~45KB gzipped | ~12KB gzipped |
| Full build time (Vite) | ~800ms | ~80ms |
| Full build time (PostCSS) | ~800ms | ~200ms |
| HMR update | ~150ms | ~8ms |

### Vite Plugin vs PostCSS

| | Vite Plugin | PostCSS |
|---|---|---|
| Full builds | **10x faster** | Baseline |
| HMR | **~8ms** | ~50ms |
| Setup | `@tailwindcss/vite` in next.config | `@tailwindcss/postcss` in postcss.config |
| Compatibility | Next.js 15+, Vite 6+ | Any PostCSS pipeline |

**Recommendation:** Always use Vite plugin for new projects. Fall back to PostCSS only
for legacy build systems.

### Tips

1. **Let auto-detection work** — Do not add `@source` unless needed. The default
   scanner is fast and respects `.gitignore`.
2. **Use `@theme inline`** — For tokens that only need CSS variables (not utility
   classes), `inline` avoids generating unused classes.
3. **Avoid `@apply` in component files** — Prefer className strings. `@apply` can
   prevent tree-shaking.
4. **Minimal `@import`** — Import only `"tailwindcss"`. Do not import layer files
   individually unless you have a specific reason.
