# Authentication Patterns

## JWT Implementation

### Token Structure

```
Header.Payload.Signature

Header: { "alg": "HS256", "typ": "JWT" }
Payload: { "sub": "user123", "iat": 1234567890, "exp": 1234568790 }
Signature: HMACSHA256(base64(header) + "." + base64(payload), secret)
```

### Access + Refresh Token Pattern

```typescript
// Token service
class TokenService {
  private readonly accessSecret: string;
  private readonly refreshSecret: string;

  constructor() {
    this.accessSecret = process.env.JWT_ACCESS_SECRET!;
    this.refreshSecret = process.env.JWT_REFRESH_SECRET!;
  }

  generateTokenPair(user: User): TokenPair {
    const accessToken = jwt.sign(
      {
        sub: user.id,
        email: user.email,
        role: user.role,
      },
      this.accessSecret,
      { expiresIn: '15m' }
    );

    const refreshToken = jwt.sign(
      { sub: user.id },
      this.refreshSecret,
      { expiresIn: '7d' }
    );

    return { accessToken, refreshToken };
  }

  verifyAccessToken(token: string): AccessTokenPayload {
    return jwt.verify(token, this.accessSecret) as AccessTokenPayload;
  }

  verifyRefreshToken(token: string): RefreshTokenPayload {
    return jwt.verify(token, this.refreshSecret) as RefreshTokenPayload;
  }
}
```

### Token Refresh Endpoint

```typescript
// POST /api/auth/refresh
export async function POST(req: Request) {
  const { refreshToken } = await req.json();

  try {
    // Verify refresh token
    const payload = tokenService.verifyRefreshToken(refreshToken);

    // Check if token is in database (not revoked)
    const storedToken = await db.refreshToken.findUnique({
      where: { token: hashToken(refreshToken) }
    });

    if (!storedToken || storedToken.revoked) {
      return Response.json({ error: 'Invalid token' }, { status: 401 });
    }

    // Get user
    const user = await db.user.findUnique({
      where: { id: payload.sub }
    });

    if (!user) {
      return Response.json({ error: 'User not found' }, { status: 401 });
    }

    // Generate new token pair
    const tokens = tokenService.generateTokenPair(user);

    // Rotate refresh token (invalidate old, store new)
    await db.refreshToken.update({
      where: { id: storedToken.id },
      data: { revoked: true }
    });

    await db.refreshToken.create({
      data: {
        token: hashToken(tokens.refreshToken),
        userId: user.id,
        expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
      }
    });

    return Response.json(tokens);
  } catch {
    return Response.json({ error: 'Invalid token' }, { status: 401 });
  }
}
```

## OAuth 2.0 Flows

### Authorization Code Flow (Web Apps)

```
┌──────────┐                              ┌──────────┐                              ┌──────────┐
│   User   │                              │ Your App │                              │  OAuth   │
│ Browser  │                              │  Server  │                              │ Provider │
└────┬─────┘                              └────┬─────┘                              └────┬─────┘
     │  1. Click "Login with Google"           │                                        │
     │────────────────────────────────────────>│                                        │
     │                                         │                                        │
     │  2. Redirect to OAuth provider          │                                        │
     │<────────────────────────────────────────│                                        │
     │                                         │                                        │
     │  3. User authorizes                     │                                        │
     │─────────────────────────────────────────────────────────────────────────────────>│
     │                                         │                                        │
     │  4. Redirect with authorization code    │                                        │
     │<─────────────────────────────────────────────────────────────────────────────────│
     │                                         │                                        │
     │  5. Send code to your server            │                                        │
     │────────────────────────────────────────>│                                        │
     │                                         │  6. Exchange code for tokens           │
     │                                         │───────────────────────────────────────>│
     │                                         │                                        │
     │                                         │  7. Access token + ID token            │
     │                                         │<───────────────────────────────────────│
     │                                         │                                        │
     │  8. Set session cookie                  │                                        │
     │<────────────────────────────────────────│                                        │
```

### OAuth Implementation (Next.js + Google)

```typescript
// app/api/auth/google/route.ts
import { google } from 'googleapis';

const oauth2Client = new google.auth.OAuth2(
  process.env.GOOGLE_CLIENT_ID,
  process.env.GOOGLE_CLIENT_SECRET,
  process.env.GOOGLE_REDIRECT_URI
);

// Step 1: Generate auth URL
export async function GET() {
  const authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: ['email', 'profile'],
    state: generateState(), // CSRF protection
  });

  return Response.redirect(authUrl);
}

// app/api/auth/google/callback/route.ts
export async function GET(req: Request) {
  const url = new URL(req.url);
  const code = url.searchParams.get('code');
  const state = url.searchParams.get('state');

  // Verify state (CSRF)
  if (!verifyState(state)) {
    return Response.json({ error: 'Invalid state' }, { status: 400 });
  }

  // Exchange code for tokens
  const { tokens } = await oauth2Client.getToken(code!);
  oauth2Client.setCredentials(tokens);

  // Get user info
  const oauth2 = google.oauth2({ version: 'v2', auth: oauth2Client });
  const { data } = await oauth2.userinfo.get();

  // Create or update user
  const user = await db.user.upsert({
    where: { email: data.email! },
    create: {
      email: data.email!,
      name: data.name!,
      googleId: data.id!,
    },
    update: {
      googleId: data.id!,
    },
  });

  // Create session
  const sessionToken = generateSessionToken();
  await createSession(user.id, sessionToken);

  // Set cookie and redirect
  const response = Response.redirect('/dashboard');
  response.headers.set(
    'Set-Cookie',
    `session=${sessionToken}; HttpOnly; Secure; SameSite=Lax; Path=/`
  );

  return response;
}
```

## Session Management

### Secure Session Configuration

```typescript
// Session store (Redis recommended for production)
import { createClient } from 'redis';

const redis = createClient({ url: process.env.REDIS_URL });

interface Session {
  userId: string;
  createdAt: number;
  lastActivity: number;
  userAgent: string;
  ip: string;
}

async function createSession(
  userId: string,
  req: Request
): Promise<string> {
  const sessionId = crypto.randomUUID();
  const session: Session = {
    userId,
    createdAt: Date.now(),
    lastActivity: Date.now(),
    userAgent: req.headers.get('user-agent') || '',
    ip: req.headers.get('x-forwarded-for') || '',
  };

  await redis.set(
    `session:${sessionId}`,
    JSON.stringify(session),
    { EX: 7 * 24 * 60 * 60 } // 7 days
  );

  return sessionId;
}

async function validateSession(sessionId: string): Promise<Session | null> {
  const data = await redis.get(`session:${sessionId}`);
  if (!data) return null;

  const session = JSON.parse(data) as Session;

  // Update last activity
  session.lastActivity = Date.now();
  await redis.set(
    `session:${sessionId}`,
    JSON.stringify(session),
    { EX: 7 * 24 * 60 * 60 }
  );

  return session;
}

async function destroySession(sessionId: string): Promise<void> {
  await redis.del(`session:${sessionId}`);
}
```

## Multi-Factor Authentication

### TOTP Implementation

```typescript
import { authenticator } from 'otplib';

// Generate secret for user
function generateTotpSecret(): string {
  return authenticator.generateSecret();
}

// Generate QR code URL
function getTotpQrUrl(email: string, secret: string): string {
  return authenticator.keyuri(email, 'YourApp', secret);
}

// Verify TOTP code
function verifyTotpCode(code: string, secret: string): boolean {
  return authenticator.verify({ token: code, secret });
}

// Setup flow
export async function setupMfa(userId: string) {
  const secret = generateTotpSecret();

  // Store encrypted secret (not enabled yet)
  await db.user.update({
    where: { id: userId },
    data: {
      totpSecret: encrypt(secret),
      mfaEnabled: false, // Enable after verification
    },
  });

  const user = await db.user.findUnique({ where: { id: userId } });
  const qrUrl = getTotpQrUrl(user!.email, secret);

  return { secret, qrUrl };
}

// Verify and enable
export async function verifyAndEnableMfa(
  userId: string,
  code: string
): Promise<boolean> {
  const user = await db.user.findUnique({ where: { id: userId } });
  const secret = decrypt(user!.totpSecret!);

  if (verifyTotpCode(code, secret)) {
    await db.user.update({
      where: { id: userId },
      data: { mfaEnabled: true },
    });
    return true;
  }

  return false;
}
```

## Rate Limiting

### Login Rate Limiting

```typescript
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(5, '15 m'), // 5 attempts per 15 min
  analytics: true,
});

export async function POST(req: Request) {
  const { email, password } = await req.json();

  // Rate limit by IP + email combination
  const ip = req.headers.get('x-forwarded-for') || 'unknown';
  const identifier = `login:${ip}:${email}`;

  const { success, limit, remaining, reset } = await ratelimit.limit(identifier);

  if (!success) {
    return Response.json(
      {
        error: 'Too many login attempts',
        retryAfter: Math.ceil((reset - Date.now()) / 1000),
      },
      {
        status: 429,
        headers: {
          'X-RateLimit-Limit': limit.toString(),
          'X-RateLimit-Remaining': remaining.toString(),
          'X-RateLimit-Reset': reset.toString(),
        },
      }
    );
  }

  // Proceed with login...
}
```
