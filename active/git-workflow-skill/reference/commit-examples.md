# Commit Message Examples

## By Type

### feat: New Features

```bash
# Simple feature
feat(auth): add password reset flow

# Feature with scope
feat(api): add user search endpoint

# Feature with body
feat(ui): add dark mode toggle

Adds system preference detection and manual toggle.
Persists preference to localStorage.

# Feature with breaking change
feat(api)!: change pagination to cursor-based

BREAKING CHANGE: offset-based pagination removed.
Use `cursor` and `limit` params instead of `page` and `pageSize`.
```

### fix: Bug Fixes

```bash
# Simple fix
fix(auth): prevent session timeout on active users

# Fix with issue reference
fix(checkout): handle zero-quantity items

Items with quantity 0 now removed from cart.
Closes #456

# Fix with root cause
fix(api): handle null response from payment provider

PaymentProvider.charge() can return null on timeout.
Added null check and retry logic.
```

### docs: Documentation

```bash
# README update
docs(readme): add deployment instructions

# API documentation
docs(api): document rate limiting headers

# Code comments
docs: add JSDoc to utility functions
```

### style: Formatting

```bash
# Code formatting
style: apply prettier formatting

# Linting fixes
style(api): fix eslint warnings

# Whitespace/formatting only
style: normalize line endings to LF
```

### refactor: Code Restructuring

```bash
# Extract function
refactor(auth): extract token validation to middleware

# Rename
refactor: rename UserService to UserRepository

# Simplify
refactor(api): simplify error handling with Result type

# Split file
refactor(ui): split Button into separate components
```

### perf: Performance

```bash
# Optimization
perf(db): add index on users.email

# Caching
perf(api): cache user profile for 5 minutes

# Bundle size
perf(ui): lazy load dashboard charts
```

### test: Testing

```bash
# Add tests
test(auth): add unit tests for token refresh

# Fix flaky test
test(e2e): fix race condition in checkout flow

# Improve coverage
test(api): add edge case tests for validation
```

### build: Build System

```bash
# Dependencies
build(deps): upgrade React to v18

# Build config
build: add production optimization flags

# Output
build: configure source maps for debugging
```

### ci: Continuous Integration

```bash
# Pipeline changes
ci: add staging deployment step

# Fix CI
ci: increase test timeout for slow runners

# New workflow
ci: add nightly security scan
```

### chore: Maintenance

```bash
# Dependencies
chore(deps): update dev dependencies

# Cleanup
chore: remove unused imports

# Config
chore: add .nvmrc for Node version
```

## Real-World Examples

### API Development

```bash
feat(api): add user authentication endpoints

- POST /auth/login - email/password login
- POST /auth/register - new user registration
- POST /auth/refresh - token refresh
- DELETE /auth/logout - invalidate session

Closes #101
```

### Bug Fix with Context

```bash
fix(checkout): prevent duplicate order submission

Users clicking "Place Order" multiple times created duplicates.
Added idempotency key and disabled button during submission.

Root cause: No client-side debouncing + no server idempotency.
Solution: Both client and server-side protection.

Closes #202
```

### Breaking Change

```bash
feat(api)!: migrate to JSON:API response format

BREAKING CHANGE: All API responses now follow JSON:API spec.

Before:
{
  "user": { "id": 1, "name": "John" }
}

After:
{
  "data": {
    "type": "user",
    "id": "1",
    "attributes": { "name": "John" }
  }
}

Migration guide: https://docs.example.com/migration/v2
```

### Hotfix

```bash
fix(payment): increase Stripe timeout to 30s

URGENT: Production payments failing during peak hours.

Stripe webhook responses taking >10s under load.
Increased timeout from 10s to 30s.

Monitoring: https://dashboard.example.com/payments
Closes INCIDENT-789
```

## Anti-Patterns (Don't Do This)

```bash
# Too vague
fix: stuff
update code
misc changes
WIP

# No type
added user feature
fixed the bug

# Past tense (should be present/imperative)
feat: added login
fix: fixed null pointer

# Too long subject
feat(authentication): implement comprehensive user authentication system with OAuth2 support including Google, GitHub, and Microsoft providers

# Implementation details in subject
fix: change line 45 in UserService.ts
```

## Subject Line Formula

```
<verb> <what> [<context>]

Examples:
add user authentication → what we're adding
fix null pointer in checkout → what + where
remove deprecated endpoints → what we're removing
update dependencies to latest → what + detail
```

**Good Verbs:** add, remove, update, fix, implement, refactor, optimize, move, rename, extract, simplify, handle, prevent, enable, disable
