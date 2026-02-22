# Feature Contract: frontend-ui-skill (#39)

**Date:** 2026-02-22
**Status:** APPROVED

## IN SCOPE

- Tailwind CSS v4 setup (@theme directive, OKLCH colors, container queries, CSS-first config)
- shadcn/ui 2026 patterns (@theme inline, data-slot, no forwardRef, tw-animate-css)
- React 19 / Next.js 15+ App Router component architecture
- Server Components / Client Components boundary patterns
- Enterprise SaaS UI patterns (dashboards, pricing pages, data tables, onboarding)
- Accessibility (WCAG 2.1 AA) — semantic HTML, keyboard, focus management, ARIA
- State management decision tree (URL → server → local → Zustand)
- Forms (React Hook Form + Zod + shadcn Form + Server Actions)
- Performance optimization (Core Web Vitals, code splitting, image optimization)
- Responsive design (mobile-first, container queries)
- Dark mode (CSS-based with Tailwind v4)
- Component patterns (cva variants, compound components, polymorphic)

## OUT OF SCOPE

- Vue, Svelte, Angular frameworks
- CSS-in-JS solutions (styled-components, Emotion)
- Backend API design (covered by api-design-skill)
- Testing framework setup (covered by testing-skill)
- React + Vite (non-Next.js) — planned for next sprint
- Authentication flows (covered by security-skill)
- Payment UI details (covered by stripe-stack-skill)

## SUCCESS CRITERIA

- [ ] SKILL.md under 500 lines with all XML sections
- [ ] 8 reference files for deep-dive content
- [ ] 5 template files with production-ready code
- [ ] All activation triggers tested
- [ ] config.json follows library schema
- [ ] Integrates cleanly with existing skills (testing, api-design, security, stripe-stack)

## OBSERVER CHECKPOINTS

1. Contract approved before coding (this document)
2. SKILL.md structure review after draft
3. Final quality check before commit
