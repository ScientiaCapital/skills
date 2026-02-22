# Secrets Management

## The Golden Rule

**NEVER commit secrets to version control**

```bash
# .gitignore - Always include
.env
.env.local
.env.*.local
*.pem
*.key
credentials.json
secrets.yaml
```

## Environment Variables

```bash
# .env (local development)
DATABASE_URL=postgresql://localhost:5432/myapp
JWT_SECRET=dev-secret-change-in-production
STRIPE_SECRET_KEY=sk_test_...

# .env.example (commit this!)
DATABASE_URL=postgresql://localhost:5432/myapp
JWT_SECRET=generate-secure-secret
STRIPE_SECRET_KEY=sk_test_your_key_here
```

## Loading Secrets

```typescript
// DO: Validate at startup
import { z } from 'zod';

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
});

const env = envSchema.parse(process.env);

// DON'T: Use undefined secrets
// Always validate that required env vars exist
```

## Secret Rotation

```typescript
// Support multiple secrets during rotation
const JWT_SECRETS = [
  process.env.JWT_SECRET_NEW,    // Current
  process.env.JWT_SECRET_OLD,    // Previous (for validation)
].filter(Boolean);

function verifyToken(token: string): JWTPayload {
  for (const secret of JWT_SECRETS) {
    try {
      return jwt.verify(token, secret);
    } catch {
      continue;
    }
  }
  throw new Error('Invalid token');
}
```

## Never Log Secrets

```typescript
// DO: Mask sensitive data in logs
logger.info('User login', {
  userId: user.id,
  email: maskEmail(user.email), // t***@example.com
});

// DON'T: Log tokens or credentials
// Never log: authorization headers, request bodies with passwords, API keys
```
