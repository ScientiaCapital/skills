# Test Organization Patterns

## File Structure

### Colocated Tests (Recommended)

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx     # Unit tests
│   │   └── Button.stories.tsx  # Storybook (optional)
│   └── Form/
│       ├── Form.tsx
│       └── Form.test.tsx
├── hooks/
│   ├── useAuth.ts
│   └── useAuth.test.ts
├── utils/
│   ├── format.ts
│   └── format.test.ts
└── services/
    ├── api.ts
    └── api.test.ts
```

### Separate Test Directory

```
src/
├── components/
│   └── Button.tsx
├── utils/
│   └── format.ts
└── ...

tests/
├── unit/
│   ├── components/
│   │   └── Button.test.tsx
│   └── utils/
│       └── format.test.ts
├── integration/
│   └── api.test.ts
└── e2e/
    └── checkout.spec.ts
```

### Hybrid (Most Common)

```
src/
├── components/
│   ├── Button.tsx
│   └── Button.test.tsx        # Colocated unit tests
├── utils/
│   ├── format.ts
│   └── format.test.ts
└── __tests__/                  # Integration tests
    ├── api.integration.test.ts
    └── auth.integration.test.ts

e2e/
└── checkout.spec.ts           # E2E tests separate
```

## Naming Conventions

### File Names

| Pattern | Example | Use Case |
|---------|---------|----------|
| `.test.ts` | `Button.test.tsx` | Default for unit tests |
| `.spec.ts` | `Button.spec.tsx` | Alternative (Jasmine style) |
| `.integration.test.ts` | `api.integration.test.ts` | Integration tests |
| `.e2e.ts` | `checkout.e2e.ts` | E2E tests |

### Test Names

```typescript
// Describe what, not how
describe('UserService', () => {
  describe('createUser', () => {
    // Pattern: "should [expected behavior] when [condition]"
    it('should return user object when given valid email', () => {});
    it('should throw ValidationError when email is invalid', () => {});
    it('should hash password before saving', () => {});
  });
});

// BDD alternative
describe('UserService', () => {
  describe('when creating a user', () => {
    describe('with valid data', () => {
      it('returns the created user', () => {});
      it('sends welcome email', () => {});
    });

    describe('with invalid email', () => {
      it('throws ValidationError', () => {});
      it('does not create user in database', () => {});
    });
  });
});
```

## Test Suites Organization

### Group by Feature

```typescript
describe('Authentication', () => {
  describe('Login', () => {
    it('succeeds with valid credentials', () => {});
    it('fails with invalid password', () => {});
    it('rate limits after 5 failures', () => {});
  });

  describe('Logout', () => {
    it('clears session', () => {});
    it('revokes refresh token', () => {});
  });

  describe('Password Reset', () => {
    it('sends reset email', () => {});
    it('validates reset token', () => {});
  });
});
```

### Group by Method

```typescript
describe('Calculator', () => {
  describe('add', () => {
    it('adds positive numbers', () => {});
    it('adds negative numbers', () => {});
    it('handles zero', () => {});
  });

  describe('divide', () => {
    it('divides numbers', () => {});
    it('throws on divide by zero', () => {});
  });
});
```

## Setup and Teardown

### Scope Levels

```typescript
// Global - runs once for all tests
beforeAll(async () => {
  await connectDatabase();
});

afterAll(async () => {
  await disconnectDatabase();
});

// Per test file - runs for each describe block
describe('UserService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    cleanup();
  });
});
```

### Shared Setup

```typescript
// tests/setup.ts
import { beforeAll, afterAll, beforeEach } from 'vitest';
import { db } from '../src/database';

beforeAll(async () => {
  await db.migrate.latest();
});

beforeEach(async () => {
  await db.truncate(['users', 'posts']);
});

afterAll(async () => {
  await db.destroy();
});
```

## Test Helpers

### Factory Functions

```typescript
// tests/factories/user.ts
export function createUser(overrides: Partial<User> = {}): User {
  return {
    id: Math.random().toString(36),
    name: 'Test User',
    email: `test-${Date.now()}@example.com`,
    createdAt: new Date(),
    ...overrides
  };
}

export function createUsers(count: number): User[] {
  return Array.from({ length: count }, () => createUser());
}
```

### Custom Matchers

```typescript
// tests/matchers.ts
expect.extend({
  toBeValidEmail(received: string) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const pass = emailRegex.test(received);
    return {
      pass,
      message: () => `expected ${received} to be a valid email`
    };
  }
});

// Usage
expect('test@example.com').toBeValidEmail();
```

### Test Utilities

```typescript
// tests/utils.ts
export async function waitForCondition(
  condition: () => boolean,
  timeout = 5000
): Promise<void> {
  const start = Date.now();
  while (!condition()) {
    if (Date.now() - start > timeout) {
      throw new Error('Condition not met within timeout');
    }
    await new Promise(r => setTimeout(r, 100));
  }
}

export function mockDate(date: Date): () => void {
  const original = Date.now;
  Date.now = () => date.getTime();
  return () => { Date.now = original; };
}
```

## Configuration

### vitest.config.ts

```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom', // or 'node'
    setupFiles: ['./tests/setup.ts'],
    include: ['**/*.test.ts', '**/*.test.tsx'],
    exclude: ['node_modules', 'dist'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      exclude: ['**/*.test.ts', 'tests/**']
    }
  }
});
```

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -v --cov=src --cov-report=html
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
```

## Running Tests

### Scripts

```json
{
  "scripts": {
    "test": "vitest",
    "test:watch": "vitest --watch",
    "test:coverage": "vitest --coverage",
    "test:unit": "vitest --testPathPattern=unit",
    "test:integration": "vitest --testPathPattern=integration",
    "test:e2e": "playwright test"
  }
}
```

### Filtering

```bash
# Run specific file
vitest Button.test.tsx

# Run tests matching pattern
vitest -t "should create user"

# Run tests in directory
vitest tests/integration

# Skip slow tests
vitest --exclude "**/*.slow.test.ts"
```
