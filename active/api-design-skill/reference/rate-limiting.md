# Rate Limiting

## Headers

```
X-RateLimit-Limit: 100        # Max requests per window
X-RateLimit-Remaining: 95     # Requests remaining
X-RateLimit-Reset: 1640000000 # Unix timestamp when limit resets
Retry-After: 60               # Seconds until can retry (on 429)
```

## Tiers

| Tier | Limit | Window |
|------|-------|--------|
| Anonymous | 60 req | 1 hour |
| Free | 100 req | 1 minute |
| Pro | 1000 req | 1 minute |
| Enterprise | 10000 req | 1 minute |

## Implementation

```typescript
import { Ratelimit } from '@upstash/ratelimit';

const ratelimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(100, '1 m'),
});

async function rateLimitMiddleware(req: Request) {
  const identifier = req.headers.get('authorization') || req.ip;
  const { success, limit, remaining, reset } = await ratelimit.limit(identifier);

  const headers = {
    'X-RateLimit-Limit': limit.toString(),
    'X-RateLimit-Remaining': remaining.toString(),
    'X-RateLimit-Reset': reset.toString(),
  };

  if (!success) {
    return new Response(
      JSON.stringify({
        error: {
          code: 'rate_limited',
          message: 'Too many requests',
        },
      }),
      {
        status: 429,
        headers: {
          ...headers,
          'Retry-After': Math.ceil((reset - Date.now()) / 1000).toString(),
        },
      }
    );
  }

  return { headers };
}
```
