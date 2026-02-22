# Vite + React 19 Setup Guide

Complete guide for setting up a Vite-powered React 19 SPA with Tailwind v4 and shadcn/ui.

> **When to use Vite SPA vs Next.js:**
> - **Vite SPA:** Internal tools, dashboards behind auth, admin panels, Electron apps, any app that doesn't need SSR/SEO
> - **Next.js:** Public-facing marketing, SEO-critical pages, apps needing Server Components for data-heavy rendering

---

## Installation

### Create Project

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
```

This scaffolds:
- `index.html` — Entry point (Vite uses HTML as entry, not JS)
- `src/main.tsx` — React root mount
- `src/App.tsx` — Root component
- `vite.config.ts` — Build configuration
- `tsconfig.json` + `tsconfig.app.json` — TypeScript config

### Install Core Dependencies

```bash
# Tailwind v4 with Vite plugin (NOT postcss — Vite gets the fast native plugin)
npm install -D @tailwindcss/vite

# shadcn/ui prerequisites
npm install tailwind-merge clsx class-variance-authority lucide-react
npm install tw-animate-css

# Data fetching
npm install @tanstack/react-query

# Routing (pick one)
npm install react-router        # React Router v7
# npm install @tanstack/react-router  # TanStack Router alternative

# Forms
npm install react-hook-form @hookform/resolvers zod
```

---

## Vite Config Deep Dive

### Base Configuration

```ts
// vite.config.ts
import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"
import tailwindcss from "@tailwindcss/vite"
import path from "path"

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})
```

### Path Aliases

Vite and TypeScript need aligned alias config:

```ts
// vite.config.ts
resolve: {
  alias: {
    "@": path.resolve(__dirname, "./src"),
    "@/components": path.resolve(__dirname, "./src/components"),
    "@/lib": path.resolve(__dirname, "./src/lib"),
    "@/hooks": path.resolve(__dirname, "./src/hooks"),
  },
},
```

```json
// tsconfig.app.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

**Both must match** — Vite uses its own resolver (not TypeScript's) at build time.

### API Proxy for Development

Avoid CORS issues by proxying API requests to your backend:

```ts
// vite.config.ts
server: {
  port: 5173,
  proxy: {
    // Single backend
    "/api": {
      target: "http://localhost:3001",
      changeOrigin: true,
    },
    // WebSocket support
    "/ws": {
      target: "ws://localhost:3001",
      ws: true,
    },
    // Rewrite paths
    "/auth": {
      target: "http://localhost:3002",
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/auth/, "/v1/auth"),
    },
  },
},
```

### Manual Chunks for Vendor Splitting

Control bundle splitting for optimal caching:

```ts
// vite.config.ts
build: {
  rollupOptions: {
    output: {
      manualChunks: {
        // Core React — changes rarely, cache aggressively
        vendor: ["react", "react-dom"],
        // UI primitives — changes with shadcn updates
        ui: [
          "@radix-ui/react-dialog",
          "@radix-ui/react-dropdown-menu",
          "@radix-ui/react-popover",
          "@radix-ui/react-select",
          "@radix-ui/react-tabs",
        ],
        // Router — changes rarely
        router: ["react-router"],
        // Data fetching — changes rarely
        query: ["@tanstack/react-query"],
      },
    },
  },
  // Target modern browsers only
  target: "es2022",
  // Generate source maps for error tracking
  sourcemap: true,
},
```

**Chunk strategy:**
- `vendor` (~140KB gzipped) — React core, cache for months
- `ui` (~50KB gzipped) — Radix primitives, cache for weeks
- `router` (~15KB gzipped) — Route library
- `query` (~12KB gzipped) — React Query
- App code — Split per route via `React.lazy()`

---

## Tailwind v4 with Vite

### Why `@tailwindcss/vite` (Not PostCSS)

| Feature | `@tailwindcss/vite` | `@tailwindcss/postcss` |
|---------|--------------------|-----------------------|
| HMR speed | ~5ms (native) | ~50ms (PostCSS pipeline) |
| Build integration | Direct Vite plugin | PostCSS middleware |
| Config needed | Just `plugins: [tailwindcss()]` | `postcss.config.js` |
| Use when | Vite projects | Non-Vite tools, Webpack |

### CSS Setup

```css
/* src/index.css */
@import "tailwindcss";
@import "tw-animate-css";

@theme inline {
  --color-background: oklch(1 0 0);
  --color-foreground: oklch(0.145 0 0);
  --color-card: oklch(1 0 0);
  --color-card-foreground: oklch(0.145 0 0);
  --color-popover: oklch(1 0 0);
  --color-popover-foreground: oklch(0.145 0 0);
  --color-primary: oklch(0.205 0.042 264.695);
  --color-primary-foreground: oklch(0.985 0 0);
  --color-secondary: oklch(0.97 0 0);
  --color-secondary-foreground: oklch(0.205 0.042 264.695);
  --color-muted: oklch(0.97 0 0);
  --color-muted-foreground: oklch(0.556 0 0);
  --color-accent: oklch(0.97 0 0);
  --color-accent-foreground: oklch(0.205 0.042 264.695);
  --color-destructive: oklch(0.577 0.245 27.325);
  --color-border: oklch(0.922 0 0);
  --color-input: oklch(0.922 0 0);
  --color-ring: oklch(0.708 0 0);
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
  --radius: 0.625rem;
}

/* Dark mode overrides */
.dark {
  --color-background: oklch(0.145 0 0);
  --color-foreground: oklch(0.985 0 0);
  --color-card: oklch(0.205 0 0);
  --color-card-foreground: oklch(0.985 0 0);
  --color-primary: oklch(0.922 0 0);
  --color-primary-foreground: oklch(0.205 0.042 264.695);
  --color-secondary: oklch(0.269 0 0);
  --color-secondary-foreground: oklch(0.985 0 0);
  --color-muted: oklch(0.269 0 0);
  --color-muted-foreground: oklch(0.708 0 0);
  --color-accent: oklch(0.269 0 0);
  --color-accent-foreground: oklch(0.985 0 0);
  --color-destructive: oklch(0.704 0.191 22.216);
  --color-border: oklch(1 0 0 / 10%);
  --color-input: oklch(1 0 0 / 15%);
  --color-ring: oklch(0.556 0 0);
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
```

### Source Detection

Tailwind v4 auto-detects files in the project root. If components live outside `src/`, add explicit source paths:

```css
/* Include files from a monorepo package */
@source "../packages/ui/src/**/*.tsx";
```

---

## shadcn/ui with Vite

### Initialization

```bash
npx shadcn@latest init
```

The CLI auto-detects Vite projects. It will:
1. Create `src/lib/utils.ts` with `cn()` helper
2. Create `components.json` pointing to `src/components/ui`
3. Add CSS variables to your stylesheet

### components.json for Vite

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": false,
  "tsx": true,
  "tailwind": {
    "config": "",
    "css": "src/index.css",
    "baseColor": "neutral",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  },
  "iconLibrary": "lucide"
}
```

**Key difference from Next.js:** `"rsc": false` — disables Server Component wrappers.

### Adding Components

```bash
npx shadcn@latest add button card dialog table form input label
npx shadcn@latest add sidebar  # Dashboard sidebar component
```

Components install into `src/components/ui/` and work identically to Next.js.

### tsconfig Paths Requirement

shadcn/ui uses `@/` imports. Ensure both configs are aligned:

```json
// tsconfig.app.json — TypeScript resolution
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": { "@/*": ["./src/*"] }
  }
}
```

```ts
// vite.config.ts — Build-time resolution
resolve: {
  alias: { "@": path.resolve(__dirname, "./src") },
},
```

---

## Environment Variables

### Comparison: Vite vs Next.js

| Feature | Vite | Next.js |
|---------|------|---------|
| Client prefix | `VITE_` | `NEXT_PUBLIC_` |
| Server-only vars | No prefix (not bundled) | No prefix |
| Access pattern | `import.meta.env.VITE_API_URL` | `process.env.NEXT_PUBLIC_API_URL` |
| `.env` files | `.env`, `.env.local`, `.env.[mode]` | `.env`, `.env.local`, `.env.[mode]` |
| Mode-specific | `.env.development`, `.env.production` | `.env.development`, `.env.production` |
| Type safety | `env.d.ts` declaration | `next-env.d.ts` auto-generated |
| Build-time only | Yes (statically replaced) | Client vars are build-time |

### Type-Safe Environment Variables

```ts
// src/env.d.ts
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_APP_TITLE: string
  readonly VITE_STRIPE_PUBLISHABLE_KEY: string
  readonly VITE_POSTHOG_KEY: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
```

### Runtime Validation with Zod

```ts
// src/lib/env.ts
import { z } from "zod"

const envSchema = z.object({
  VITE_API_URL: z.string().url(),
  VITE_APP_TITLE: z.string().default("My App"),
  VITE_STRIPE_PUBLISHABLE_KEY: z.string().startsWith("pk_"),
})

export const env = envSchema.parse(import.meta.env)
```

### .env Files

```bash
# .env — Shared defaults (committed)
VITE_APP_TITLE="My SaaS App"

# .env.local — Local overrides (gitignored)
VITE_API_URL=http://localhost:3001
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_xxx

# .env.production — Production values (committed)
VITE_API_URL=https://api.myapp.com
```

---

## Build Optimization

### Dynamic Imports for Route-Based Splitting

```tsx
import { lazy, Suspense } from "react"

// Each lazy() call creates a separate chunk
const Dashboard = lazy(() => import("@/pages/Dashboard"))
const Settings = lazy(() => import("@/pages/Settings"))
const Analytics = lazy(() => import("@/pages/Analytics"))

// Wrap in Suspense
<Suspense fallback={<PageSkeleton />}>
  <Dashboard />
</Suspense>
```

### Preloading Critical Routes

```tsx
// Preload on hover/focus for instant navigation
const DashboardModule = () => import("@/pages/Dashboard")
const Dashboard = lazy(DashboardModule)

function NavLink({ to, children }: { to: string; children: React.ReactNode }) {
  return (
    <Link
      to={to}
      onMouseEnter={() => DashboardModule()}
      onFocus={() => DashboardModule()}
    >
      {children}
    </Link>
  )
}
```

### Tree Shaking

Vite (via Rollup/esbuild) tree-shakes automatically. Ensure:

```tsx
// GOOD: Named imports — tree-shakeable
import { Button } from "@/components/ui/button"
import { format } from "date-fns"

// BAD: Default/namespace imports — may prevent tree shaking
import * as dateFns from "date-fns"
import _ from "lodash"  // Use lodash-es instead
```

### Analyze Bundle Size

```bash
# Install analyzer
npm install -D rollup-plugin-visualizer

# Add to vite.config.ts
import { visualizer } from "rollup-plugin-visualizer"

plugins: [
  react(),
  tailwindcss(),
  visualizer({ open: true, gzipSize: true }),
],
```

---

## HMR Behavior: Vite vs Next.js

| Behavior | Vite | Next.js |
|----------|------|---------|
| CSS changes | Instant injection (no reload) | Instant injection |
| Component changes | Fast refresh (preserves state) | Fast refresh (preserves state) |
| Config changes | Full page reload | Full server restart |
| New dependencies | Auto-optimized on next request | Requires restart sometimes |
| Error overlay | Native Vite overlay | Next.js error overlay |
| State preservation | React Fast Refresh rules | Same rules |

**Vite advantage:** No server-side compilation step. Changes reflect in ~50ms vs ~200-500ms for Next.js dev server.

**Fast Refresh rules (same for both):**
- Component must be the default export or a named export
- File should only export React components
- Adding hooks can cause state reset — this is expected

---

## Project Structure

```
src/
├── components/
│   ├── ui/              # shadcn/ui components (auto-generated)
│   ├── layout/          # App layout components
│   │   ├── Sidebar.tsx
│   │   ├── Header.tsx
│   │   └── RootLayout.tsx
│   └── shared/          # Reusable app components
│       ├── DataTable.tsx
│       └── PageSkeleton.tsx
├── hooks/               # Custom hooks
│   ├── use-auth.ts
│   └── use-media-query.ts
├── lib/                 # Utilities
│   ├── utils.ts         # cn() helper
│   ├── env.ts           # Env validation
│   ├── api.ts           # API client (fetch wrapper)
│   └── query-client.ts  # React Query setup
├── pages/               # Route components (lazy-loaded)
│   ├── Dashboard.tsx
│   ├── Settings.tsx
│   └── auth/
│       ├── Login.tsx
│       └── Register.tsx
├── providers/           # Context providers
│   ├── AuthProvider.tsx
│   ├── QueryProvider.tsx
│   └── ThemeProvider.tsx
├── routes/              # Route definitions
│   └── index.tsx
├── types/               # Shared types
├── App.tsx              # Root component with providers
├── main.tsx             # Entry point
└── index.css            # Tailwind + theme tokens
```

---

## Deployment

### Static Hosting (No Server Required)

Vite SPAs build to a `dist/` folder — just static HTML, CSS, JS.

```bash
npm run build    # Outputs to dist/
npm run preview  # Local preview of production build
```

### Vercel

```json
// vercel.json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

### Netlify

```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Cloudflare Pages

```bash
# Build command: npm run build
# Build output directory: dist
```

Add `_redirects` file in `public/`:
```
/*    /index.html   200
```

### SPA Routing Catch-All

All static hosts need a catch-all redirect to `index.html` for client-side routing. Without it, direct URL access (e.g., `/dashboard/settings`) returns 404.

### Docker (Nginx)

```dockerfile
FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

```nginx
# nginx.conf
server {
  listen 80;
  root /usr/share/nginx/html;
  index index.html;

  location / {
    try_files $uri $uri/ /index.html;
  }

  # Cache static assets aggressively
  location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
  }
}
```

---

## Quick Reference: Vite CLI Commands

| Command | What It Does |
|---------|-------------|
| `npm run dev` | Start dev server (port 5173) |
| `npm run build` | Production build to `dist/` |
| `npm run preview` | Preview production build locally |
| `npx vite --host` | Expose to network (mobile testing) |
| `npx vite --port 3000` | Custom port |
| `npx vite optimize` | Pre-bundle dependencies |

---

## Common Gotchas

1. **Path aliases not working** — Must configure in BOTH `vite.config.ts` AND `tsconfig.app.json`
2. **Environment variables undefined** — Must use `VITE_` prefix and `import.meta.env` (not `process.env`)
3. **CSS not applying** — Ensure `@import "tailwindcss"` is in your CSS and `tailwindcss()` is in Vite plugins
4. **shadcn components not found** — Run `npx shadcn@latest init` and verify `components.json` has correct aliases
5. **404 on refresh** — Add catch-all redirect for SPA routing on your hosting platform
6. **Large bundle** — Add `manualChunks` and use `React.lazy()` for route components
7. **`process.env` usage** — Vite uses `import.meta.env`, not `process.env`. Libraries that use `process.env` need a define config:
   ```ts
   define: { "process.env.NODE_ENV": JSON.stringify(process.env.NODE_ENV) }
   ```
