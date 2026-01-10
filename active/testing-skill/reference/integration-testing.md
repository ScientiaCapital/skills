# Integration Testing Patterns

## API Testing

### HTTP Endpoint Tests

```typescript
// Using supertest with Express
import request from 'supertest';
import app from './app';

describe('POST /api/users', () => {
  it('creates user with valid data', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'Test', email: 'test@example.com' })
      .expect(201);

    expect(response.body).toMatchObject({
      id: expect.any(Number),
      name: 'Test',
      email: 'test@example.com'
    });
  });

  it('returns 400 for invalid email', async () => {
    await request(app)
      .post('/api/users')
      .send({ name: 'Test', email: 'invalid' })
      .expect(400);
  });

  it('returns 401 without auth token', async () => {
    await request(app)
      .post('/api/users')
      .send({ name: 'Test', email: 'test@example.com' })
      .expect(401);
  });
});
```

### Auth Testing

```typescript
describe('authenticated routes', () => {
  let authToken: string;

  beforeAll(async () => {
    // Create test user and get token
    const response = await request(app)
      .post('/api/auth/login')
      .send({ email: 'test@example.com', password: 'password' });
    authToken = response.body.token;
  });

  it('accesses protected route with token', async () => {
    await request(app)
      .get('/api/profile')
      .set('Authorization', `Bearer ${authToken}`)
      .expect(200);
  });
});
```

## Database Testing

### Test Database Setup

```typescript
// vitest.setup.ts
import { beforeAll, afterAll, beforeEach } from 'vitest';
import { db } from './database';

beforeAll(async () => {
  await db.migrate.latest();
});

beforeEach(async () => {
  await db.seed.run(); // or truncate tables
});

afterAll(async () => {
  await db.destroy();
});
```

### Transaction Rollback Pattern

```typescript
import { db } from './database';

describe('UserRepository', () => {
  let trx: Transaction;

  beforeEach(async () => {
    trx = await db.transaction();
  });

  afterEach(async () => {
    await trx.rollback();
  });

  it('creates user in database', async () => {
    const repo = new UserRepository(trx);
    const user = await repo.create({ name: 'Test' });

    expect(user.id).toBeDefined();
    expect(user.name).toBe('Test');

    // Verify in DB
    const found = await trx('users').where('id', user.id).first();
    expect(found.name).toBe('Test');
  });
});
```

### Supabase Testing

```typescript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY // Use service key for tests
);

describe('Posts table', () => {
  const testUserId = 'test-user-123';

  beforeEach(async () => {
    // Clean up test data
    await supabase.from('posts').delete().eq('user_id', testUserId);
  });

  it('inserts post with RLS', async () => {
    const { data, error } = await supabase
      .from('posts')
      .insert({ title: 'Test', user_id: testUserId })
      .select()
      .single();

    expect(error).toBeNull();
    expect(data.title).toBe('Test');
  });

  it('enforces RLS on select', async () => {
    // Switch to anon key for RLS testing
    const anonClient = createClient(
      process.env.SUPABASE_URL,
      process.env.SUPABASE_ANON_KEY
    );

    const { data, error } = await anonClient
      .from('posts')
      .select()
      .eq('user_id', testUserId);

    // Should be empty (no auth = no access)
    expect(data).toEqual([]);
  });
});
```

## Component Integration Tests

### React Component + API

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import { UserProfile } from './UserProfile';

const server = setupServer(
  rest.get('/api/user/:id', (req, res, ctx) => {
    return res(ctx.json({ id: 1, name: 'Test User' }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('loads and displays user', async () => {
  render(<UserProfile userId={1} />);

  expect(screen.getByText('Loading...')).toBeInTheDocument();

  await waitFor(() => {
    expect(screen.getByText('Test User')).toBeInTheDocument();
  });
});

test('handles error', async () => {
  server.use(
    rest.get('/api/user/:id', (req, res, ctx) => {
      return res(ctx.status(500));
    })
  );

  render(<UserProfile userId={1} />);

  await waitFor(() => {
    expect(screen.getByText('Error loading user')).toBeInTheDocument();
  });
});
```

## External Service Mocking

### MSW (Mock Service Worker)

```typescript
// mocks/handlers.ts
import { rest } from 'msw';

export const handlers = [
  rest.get('https://api.stripe.com/v1/customers/:id', (req, res, ctx) => {
    return res(
      ctx.json({
        id: req.params.id,
        email: 'test@example.com'
      })
    );
  }),

  rest.post('https://api.stripe.com/v1/charges', (req, res, ctx) => {
    return res(
      ctx.json({
        id: 'ch_test_123',
        status: 'succeeded'
      })
    );
  })
];
```

### Nock (Node.js)

```typescript
import nock from 'nock';

beforeEach(() => {
  nock('https://api.external.com')
    .get('/data')
    .reply(200, { results: [] });
});

afterEach(() => {
  nock.cleanAll();
});

test('fetches external data', async () => {
  const data = await fetchExternalData();
  expect(data.results).toEqual([]);
});
```

## Queue/Worker Testing

```typescript
describe('Email Worker', () => {
  let mockEmailService: MockEmailService;

  beforeEach(() => {
    mockEmailService = new MockEmailService();
  });

  it('processes email job', async () => {
    const worker = new EmailWorker(mockEmailService);

    await worker.process({
      to: 'test@example.com',
      subject: 'Test',
      body: 'Hello'
    });

    expect(mockEmailService.sentEmails).toHaveLength(1);
    expect(mockEmailService.sentEmails[0].to).toBe('test@example.com');
  });

  it('retries on failure', async () => {
    mockEmailService.failNextNTimes(2);

    const worker = new EmailWorker(mockEmailService, { maxRetries: 3 });
    await worker.process({ to: 'test@example.com', subject: 'Test' });

    expect(mockEmailService.attemptCount).toBe(3);
    expect(mockEmailService.sentEmails).toHaveLength(1);
  });
});
```

## Integration Test Best Practices

1. **Use real database** - Docker containers for consistent test environment
2. **Clean state** - Reset data before each test
3. **Parallel safety** - Use unique IDs, separate test users
4. **Mock external APIs** - Don't hit real Stripe, SendGrid, etc.
5. **Test error paths** - Network failures, timeouts, 500s
6. **Auth flows** - Test with and without valid tokens
