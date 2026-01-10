# Coverage Strategies

## Understanding Coverage Metrics

### Types of Coverage

| Metric | What It Measures | Target |
|--------|------------------|--------|
| **Line Coverage** | Lines of code executed | 70-80% |
| **Branch Coverage** | Decision paths taken (if/else) | 70-80% |
| **Function Coverage** | Functions called | 80-90% |
| **Statement Coverage** | Statements executed | 70-80% |

### The Coverage Trap

**100% coverage ≠ Good tests**

```typescript
// This test hits 100% coverage but tests nothing meaningful
test('user service', () => {
  const service = new UserService();
  service.createUser({ name: 'test' }); // No assertions!
});
```

**Good coverage = meaningful assertions on behavior**

## Coverage Targets by Code Type

### Critical Paths (Target: 100%)

These MUST have thorough coverage:
- Authentication/authorization logic
- Payment processing
- Data mutations (create, update, delete)
- Security-sensitive operations
- Business rule validation

### Business Logic (Target: 80-90%)

- Service layer functions
- Domain models and entities
- Validation rules
- State machines
- Calculation logic

### Infrastructure Code (Target: 60-70%)

- Database repositories
- API clients
- Middleware
- Configuration loading

### UI Components (Target: 70-80%)

- User interactions
- Conditional rendering
- Error states
- Loading states

### Skip Coverage For

- Generated code (Prisma, GraphQL codegen)
- Type definitions
- Constants/config files
- Third-party integrations (mock them instead)
- Trivial getters/setters

## Coverage Configuration

### Vitest/Jest

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'json'],
      thresholds: {
        lines: 70,
        branches: 70,
        functions: 80,
        statements: 70
      },
      exclude: [
        '**/*.d.ts',
        '**/*.config.*',
        '**/types/**',
        '**/generated/**',
        '**/mocks/**',
        '**/__tests__/**'
      ]
    }
  }
});
```

### pytest-cov

```ini
# pytest.ini
[pytest]
addopts = --cov=src --cov-report=html --cov-fail-under=70

# .coveragerc
[run]
omit =
    */tests/*
    */migrations/*
    */__init__.py
    */config.py

[report]
exclude_lines =
    pragma: no cover
    raise NotImplementedError
    if TYPE_CHECKING:
    if __name__ == "__main__":
```

## Identifying Coverage Gaps

### Branch Coverage Example

```typescript
function processOrder(order: Order) {
  if (order.total > 100) {        // Branch 1: > 100
    applyDiscount(order);
  }

  if (order.isPriority) {         // Branch 2: priority
    expediteShipping(order);
  } else {                        // Branch 3: not priority
    standardShipping(order);
  }
}

// Need tests for:
// 1. order.total > 100 (true)
// 2. order.total <= 100 (false)
// 3. order.isPriority = true
// 4. order.isPriority = false
```

### Finding Untested Branches

```bash
# Generate HTML report
vitest --coverage

# Look for yellow/red highlights in coverage report
# Yellow = partial coverage (some branches)
# Red = no coverage
```

## Coverage Anti-Patterns

### 1. Testing Implementation Details

```typescript
// BAD: Testing private method internals
test('_calculateHash returns SHA256', () => {
  expect(service._calculateHash('test')).toBe('abc123');
});

// GOOD: Test public behavior
test('user password is hashed before saving', async () => {
  const user = await service.createUser({ password: 'test' });
  expect(user.password).not.toBe('test');
});
```

### 2. Trivial Tests for Coverage

```typescript
// BAD: Testing constructor for coverage
test('User constructor', () => {
  const user = new User();
  expect(user).toBeDefined();
});

// GOOD: Test meaningful behavior
test('User defaults to inactive status', () => {
  const user = new User();
  expect(user.status).toBe('inactive');
});
```

### 3. Snapshot Test Abuse

```typescript
// BAD: Snapshot for coverage
test('renders', () => {
  const { container } = render(<ComplexForm />);
  expect(container).toMatchSnapshot();
});

// GOOD: Test specific behaviors
test('shows validation error for invalid email', async () => {
  render(<ComplexForm />);
  await userEvent.type(screen.getByLabelText('Email'), 'invalid');
  await userEvent.click(screen.getByRole('button', { name: 'Submit' }));
  expect(screen.getByText('Invalid email')).toBeInTheDocument();
});
```

## Improving Coverage Meaningfully

### 1. Test Error Paths

```typescript
describe('UserService.createUser', () => {
  it('handles database connection error', async () => {
    db.mockRejectedValue(new Error('Connection failed'));

    await expect(service.createUser(validUser))
      .rejects.toThrow('Connection failed');
  });

  it('handles duplicate email', async () => {
    db.mockRejectedValue({ code: '23505' }); // Postgres unique violation

    await expect(service.createUser(validUser))
      .rejects.toThrow('Email already exists');
  });
});
```

### 2. Test Edge Cases

```typescript
describe('calculateDiscount', () => {
  it('returns 0 for orders under minimum', () => {
    expect(calculateDiscount(49.99)).toBe(0);
  });

  it('returns 10% at exactly minimum threshold', () => {
    expect(calculateDiscount(50)).toBe(5);
  });

  it('returns 20% for large orders', () => {
    expect(calculateDiscount(500)).toBe(100);
  });

  it('handles negative values', () => {
    expect(calculateDiscount(-10)).toBe(0);
  });
});
```

### 3. Test All Branches

```typescript
describe('getStatusMessage', () => {
  it.each([
    ['pending', 'Order is being processed'],
    ['shipped', 'Order has been shipped'],
    ['delivered', 'Order delivered'],
    ['cancelled', 'Order was cancelled'],
  ])('returns correct message for %s status', (status, expected) => {
    expect(getStatusMessage(status)).toBe(expected);
  });

  it('throws for unknown status', () => {
    expect(() => getStatusMessage('invalid')).toThrow('Unknown status');
  });
});
```

## Coverage Reports

### Reading HTML Reports

1. **Green** - Fully covered
2. **Yellow** - Partially covered (some branches missed)
3. **Red** - Not covered

### CI Integration

```yaml
# GitHub Actions
- name: Run tests with coverage
  run: npm run test:coverage

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    fail_ci_if_error: true
    minimum_coverage: 70
```

## Summary

1. **Set realistic thresholds** - 70-80% is usually good
2. **Focus on critical paths** - Auth, payments, mutations need 100%
3. **Quality over quantity** - Meaningful assertions beat line counting
4. **Use branch coverage** - More valuable than line coverage
5. **Exclude generated code** - Don't pad metrics with codegen
6. **Test error paths** - These are where bugs hide
7. **Review coverage reports** - Find yellow/red hotspots
