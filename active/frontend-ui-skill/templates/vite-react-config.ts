// Vite + React 19 + Tailwind v4 + shadcn/ui configuration template
// Usage: Copy to vite.config.ts in your project root

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

  server: {
    port: 5173,
    proxy: {
      // Proxy API requests to backend in development
      "/api": {
        target: "http://localhost:3001",
        changeOrigin: true,
      },
    },
  },

  build: {
    target: "es2022",
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          // Core React — changes rarely, cache aggressively
          vendor: ["react", "react-dom"],
          // UI primitives — changes with shadcn/ui updates
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
  },
})
