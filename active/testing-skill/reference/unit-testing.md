# Unit Testing Patterns

## Core Patterns

### Arrange-Act-Assert (AAA)

```typescript
test('calculates tax correctly', () => {
  // Arrange
  const price = 100;
  const taxRate = 0.08;

  // Act
  const result = calculateTax(price, taxRate);

  // Assert
  expect(result).toBe(8);
});
```

### Given-When-Then (BDD)

```typescript
describe('ShoppingCart', () => {
  describe('given an empty cart', () => {
    describe('when adding an item', () => {
      it('then cart contains one item', () => {
        const cart = new ShoppingCart();
        cart.addItem({ id: 1, price: 10 });
        expect(cart.items).toHaveLength(1);
      });
    });
  });
});
```

## Mocking Patterns

### Mock Functions

```typescript
// vitest/jest
const mockCallback = vi.fn();
mockCallback.mockReturnValue(42);
mockCallback.mockImplementation((x) => x * 2);
mockCallback.mockResolvedValue({ data: [] });
mockCallback.mockRejectedValue(new Error('fail'));

// Verify calls
expect(mockCallback).toHaveBeenCalled();
expect(mockCallback).toHaveBeenCalledTimes(2);
expect(mockCallback).toHaveBeenCalledWith('arg1', 'arg2');
```

### Module Mocks

```typescript
// Mock entire module
vi.mock('./database', () => ({
  query: vi.fn().mockResolvedValue([]),
  connect: vi.fn()
}));

// Partial mock
vi.mock('./utils', async () => {
  const actual = await vi.importActual('./utils');
  return {
    ...actual,
    expensiveOperation: vi.fn()
  };
});
```

### Spy on Methods

```typescript
const spy = vi.spyOn(console, 'log');
doSomething();
expect(spy).toHaveBeenCalledWith('expected message');
spy.mockRestore();
```

## Testing Async Code

### Promises

```typescript
test('fetches data', async () => {
  const data = await fetchData();
  expect(data).toEqual({ name: 'test' });
});

// Or with resolves/rejects
test('fetches data', () => {
  return expect(fetchData()).resolves.toEqual({ name: 'test' });
});

test('handles error', () => {
  return expect(fetchBadData()).rejects.toThrow('Not found');
});
```

### Timers

```typescript
beforeEach(() => {
  vi.useFakeTimers();
});

afterEach(() => {
  vi.useRealTimers();
});

test('debounces function', () => {
  const callback = vi.fn();
  const debounced = debounce(callback, 1000);

  debounced();
  debounced();
  debounced();

  expect(callback).not.toHaveBeenCalled();

  vi.advanceTimersByTime(1000);

  expect(callback).toHaveBeenCalledTimes(1);
});
```

## Fixtures and Factories

### Test Factories

```typescript
// Factory function
function createUser(overrides = {}) {
  return {
    id: 1,
    name: 'Test User',
    email: 'test@example.com',
    role: 'user',
    ...overrides
  };
}

test('admin can delete users', () => {
  const admin = createUser({ role: 'admin' });
  expect(canDeleteUsers(admin)).toBe(true);
});

test('regular user cannot delete users', () => {
  const user = createUser({ role: 'user' });
  expect(canDeleteUsers(user)).toBe(false);
});
```

### Fixtures (pytest style)

```python
import pytest

@pytest.fixture
def user():
    return User(name="test", email="test@example.com")

@pytest.fixture
def admin(user):
    user.role = "admin"
    return user

def test_admin_permissions(admin):
    assert admin.can_delete_users() == True
```

## Edge Cases to Test

### Boundary Values

```typescript
describe('pagination', () => {
  test('page 0 returns first page', () => {});
  test('negative page returns first page', () => {});
  test('page beyond total returns empty', () => {});
  test('page size 0 uses default', () => {});
  test('page size negative uses default', () => {});
});
```

### Null/Undefined

```typescript
describe('formatName', () => {
  test('handles null', () => {
    expect(formatName(null)).toBe('');
  });
  test('handles undefined', () => {
    expect(formatName(undefined)).toBe('');
  });
  test('handles empty string', () => {
    expect(formatName('')).toBe('');
  });
});
```

### Collections

```typescript
describe('calculateTotal', () => {
  test('empty array returns 0', () => {});
  test('single item returns item value', () => {});
  test('multiple items returns sum', () => {});
  test('handles negative values', () => {});
});
```

## Common Assertions

```typescript
// Equality
expect(value).toBe(expected);        // Strict equality
expect(value).toEqual(expected);     // Deep equality
expect(value).toStrictEqual(expected); // Strict deep equality

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toBeUndefined();
expect(value).toBeDefined();

// Numbers
expect(value).toBeGreaterThan(3);
expect(value).toBeGreaterThanOrEqual(3);
expect(value).toBeLessThan(5);
expect(value).toBeCloseTo(0.3, 5); // Floating point

// Strings
expect(value).toMatch(/pattern/);
expect(value).toContain('substring');

// Arrays
expect(array).toContain(item);
expect(array).toHaveLength(3);
expect(array).toContainEqual({ id: 1 });

// Objects
expect(object).toHaveProperty('key');
expect(object).toHaveProperty('key', 'value');
expect(object).toMatchObject({ partial: true });

// Errors
expect(() => fn()).toThrow();
expect(() => fn()).toThrow('message');
expect(() => fn()).toThrow(ErrorClass);
```
