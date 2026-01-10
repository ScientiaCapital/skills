# OWASP Top 10 (2021)

Quick reference for the most critical web application security risks.

## A01: Broken Access Control

### Risk
Users acting outside their intended permissions.

### Examples
- Accessing other users' data by changing IDs in URLs
- Privilege escalation (user to admin)
- Missing function-level access control
- CORS misconfiguration

### Prevention

```typescript
// Always verify authorization
async function getDocument(documentId: string, userId: string) {
  const doc = await db.document.findUnique({
    where: { id: documentId }
  });

  // Check ownership or permission
  if (doc.ownerId !== userId && !await hasAccess(userId, documentId)) {
    throw new ForbiddenError('Access denied');
  }

  return doc;
}

// Use RLS in Supabase
// See reference/rls-policies.md
```

### Checklist
- [ ] Deny by default
- [ ] Implement access control checks on every request
- [ ] Use RLS for database queries
- [ ] Disable directory listing
- [ ] Log access control failures

---

## A02: Cryptographic Failures

### Risk
Exposure of sensitive data due to weak cryptography.

### Examples
- Transmitting data in clear text (HTTP)
- Using weak algorithms (MD5, SHA1 for passwords)
- Hardcoded or weak encryption keys
- Not encrypting sensitive data at rest

### Prevention

```typescript
// Use bcrypt for passwords (never MD5/SHA1)
import bcrypt from 'bcrypt';
const hash = await bcrypt.hash(password, 12);

// Use HTTPS everywhere
// Use AES-256-GCM for encryption at rest
// Use TLS 1.2+ for data in transit
```

### Checklist
- [ ] HTTPS enforced everywhere
- [ ] bcrypt for password hashing (cost factor 12+)
- [ ] Sensitive data encrypted at rest
- [ ] No deprecated algorithms (MD5, SHA1, DES)
- [ ] Secrets not in code/version control

---

## A03: Injection

### Risk
User-supplied data executed as code/queries.

### Examples
- SQL injection
- NoSQL injection
- Command injection
- LDAP injection

### Prevention

```typescript
// ALWAYS use parameterized queries
// GOOD
await db.query('SELECT * FROM users WHERE email = $1', [email]);

// BAD - vulnerable to injection
await db.query(`SELECT * FROM users WHERE email = '${email}'`);

// Use ORM/query builders
await prisma.user.findUnique({ where: { email } });
```

### Checklist
- [ ] Use parameterized queries
- [ ] Use ORM/query builders
- [ ] Validate and sanitize all input
- [ ] Limit database permissions

---

## A04: Insecure Design

### Risk
Missing or ineffective security controls by design.

### Examples
- No rate limiting on authentication
- No account lockout after failed attempts
- Predictable resource IDs (sequential integers)
- Missing business logic validation

### Prevention

```typescript
// Rate limiting
const ratelimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(5, '15 m'),
});

// Use UUIDs instead of sequential IDs
const id = crypto.randomUUID();

// Business logic validation
if (order.total < 0) {
  throw new ValidationError('Invalid order total');
}
```

### Checklist
- [ ] Threat modeling during design
- [ ] Rate limiting on sensitive endpoints
- [ ] Use UUIDs for resource identifiers
- [ ] Validate business logic constraints

---

## A05: Security Misconfiguration

### Risk
Insecure default configurations, incomplete setup.

### Examples
- Default credentials
- Unnecessary features enabled
- Error messages exposing stack traces
- Missing security headers
- Cloud storage publicly accessible

### Prevention

```typescript
// Security headers (Next.js)
const headers = [
  { key: 'X-Frame-Options', value: 'DENY' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=()' },
];

// Don't expose stack traces in production
if (process.env.NODE_ENV === 'production') {
  return { error: 'Internal server error' };
}
```

### Checklist
- [ ] Remove default credentials
- [ ] Disable unnecessary features/endpoints
- [ ] Security headers configured
- [ ] Error handling doesn't expose details
- [ ] Cloud resources not publicly accessible

---

## A06: Vulnerable Components

### Risk
Using components with known vulnerabilities.

### Examples
- Outdated dependencies with CVEs
- Unsupported frameworks
- Not tracking component versions

### Prevention

```bash
# Regular audits
npm audit
pip-audit
snyk test

# Automated updates
dependabot (GitHub)
renovate bot
```

### Checklist
- [ ] Inventory all dependencies
- [ ] Regular vulnerability scanning
- [ ] Automated dependency updates
- [ ] Remove unused dependencies
- [ ] Monitor security advisories

---

## A07: Authentication Failures

### Risk
Broken authentication mechanisms.

### Examples
- Weak passwords allowed
- Missing MFA
- Session IDs in URL
- Session not invalidated on logout
- Credential stuffing vulnerability

### Prevention

```typescript
// Strong password requirements
const passwordSchema = z.string()
  .min(8)
  .regex(/[a-z]/)
  .regex(/[A-Z]/)
  .regex(/[0-9]/)
  .regex(/[^a-zA-Z0-9]/);

// Check against breached passwords
const isPwned = await checkHaveIBeenPwned(password);

// Secure session configuration
res.cookie('session', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict',
  maxAge: 15 * 60 * 1000, // 15 minutes
});
```

### Checklist
- [ ] Strong password policy enforced
- [ ] MFA available/required
- [ ] Account lockout after failed attempts
- [ ] Session timeout implemented
- [ ] Secure session cookies

---

## A08: Software and Data Integrity

### Risk
Code and infrastructure not protected from integrity violations.

### Examples
- No integrity verification on updates
- Insecure CI/CD pipeline
- Auto-update without verification
- Deserialization of untrusted data

### Prevention

```typescript
// Verify webhook signatures
const signature = req.headers['stripe-signature'];
const event = stripe.webhooks.constructEvent(
  body,
  signature,
  process.env.STRIPE_WEBHOOK_SECRET
);

// Lock dependencies
// package-lock.json, yarn.lock, poetry.lock
npm ci // Uses lockfile exactly
```

### Checklist
- [ ] Verify signatures on external data
- [ ] Use lockfiles for dependencies
- [ ] Secure CI/CD pipeline
- [ ] Code review for all changes
- [ ] Signed commits (optional but recommended)

---

## A09: Security Logging Failures

### Risk
Insufficient logging to detect attacks.

### Examples
- No logging of login attempts
- Logs don't include enough context
- Logs stored insecurely
- No alerting on suspicious activity

### Prevention

```typescript
// Log security events
logger.info('Login attempt', {
  email: maskEmail(email),
  ip: req.ip,
  userAgent: req.headers['user-agent'],
  success: false,
  reason: 'invalid_password',
});

// Alert on anomalies
if (failedAttempts > 10) {
  alertSecurityTeam({
    type: 'brute_force_attempt',
    target: email,
    ip: req.ip,
  });
}
```

### Checklist
- [ ] Log authentication events
- [ ] Log access control failures
- [ ] Log input validation failures
- [ ] Centralized log management
- [ ] Alerting on security events

---

## A10: Server-Side Request Forgery (SSRF)

### Risk
Application fetches remote resources without validation.

### Examples
- Fetching user-provided URLs
- Accessing internal services via application
- Cloud metadata endpoint access

### Prevention

```typescript
// Validate URLs before fetching
function isAllowedUrl(url: string): boolean {
  const parsed = new URL(url);

  // Only HTTPS
  if (parsed.protocol !== 'https:') return false;

  // Block private IPs
  const ip = await dns.resolve(parsed.hostname);
  if (isPrivateIP(ip)) return false;

  // Allowlist domains (if applicable)
  const allowed = ['api.example.com', 'cdn.example.com'];
  if (!allowed.includes(parsed.hostname)) return false;

  return true;
}

// Block metadata endpoints
const blocked = [
  '169.254.169.254', // AWS metadata
  'metadata.google.internal',
];
```

### Checklist
- [ ] Validate/sanitize all URLs
- [ ] Block private IP ranges
- [ ] Use allowlists where possible
- [ ] Segment network access
- [ ] Block cloud metadata endpoints

---

## Quick Reference Card

| Risk | Primary Defense |
|------|-----------------|
| A01 Broken Access Control | RLS, authorization checks |
| A02 Crypto Failures | HTTPS, bcrypt, strong encryption |
| A03 Injection | Parameterized queries, input validation |
| A04 Insecure Design | Threat modeling, rate limiting |
| A05 Misconfiguration | Security headers, secure defaults |
| A06 Vulnerable Components | Dependency scanning, updates |
| A07 Auth Failures | Strong passwords, MFA, secure sessions |
| A08 Integrity | Signature verification, lockfiles |
| A09 Logging Failures | Security event logging, alerting |
| A10 SSRF | URL validation, network segmentation |
