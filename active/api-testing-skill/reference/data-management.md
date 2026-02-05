# Test Data Management

## Data Strategies

### Strategy Selection

| Strategy | When to Use | Pros | Cons |
|----------|-------------|------|------|
| Static fixtures | Deterministic tests | Reproducible | Stale data risk |
| Dynamic generation | Uniqueness needed | Fresh data | Non-deterministic |
| API seeding | Complex relationships | Realistic | Slower setup |
| Database snapshots | Integration tests | Fast reset | Environment coupling |

---

## Static Fixtures

### JSON Data Files

```json
// fixtures/users.json
[
    {
        "email": "admin@test.com",
        "name": "Test Admin",
        "role": "admin"
    },
    {
        "email": "user@test.com",
        "name": "Test User",
        "role": "member"
    },
    {
        "email": "readonly@test.com",
        "name": "Read Only User",
        "role": "viewer"
    }
]
```

### Using with Newman

```bash
# Run collection with data file
newman run collection.json -d fixtures/users.json

# Each iteration uses one data row
# Iteration 1: email = admin@test.com
# Iteration 2: email = user@test.com
# Iteration 3: email = readonly@test.com
```

### Accessing Data Variables

```javascript
// In request body
{
    "email": "{{email}}",
    "name": "{{name}}",
    "role": "{{role}}"
}

// In tests
pm.test("Created user matches input", function () {
    const json = pm.response.json();
    pm.expect(json.email).to.equal(pm.iterationData.get("email"));
});
```

---

## Dynamic Data Generation

### Postman Built-in Variables

```javascript
// UUID
{{$guid}}  // "a1b2c3d4-e5f6-7890-abcd-ef1234567890"

// Timestamp
{{$timestamp}}  // "1612345678"
{{$isoTimestamp}}  // "2024-01-15T10:30:00.000Z"

// Random data
{{$randomInt}}  // 42
{{$randomEmail}}  // "test.user@example.com"
{{$randomFullName}}  // "John Smith"
{{$randomFirstName}}  // "John"
{{$randomLastName}}  // "Smith"
{{$randomPhoneNumber}}  // "+1-555-123-4567"
{{$randomCity}}  // "New York"
{{$randomCountry}}  // "United States"

// Random strings
{{$randomAlphaNumeric}}  // "a1b2c3"
{{$randomWords}}  // "lorem ipsum dolor"
```

### Pre-request Script Generation

```javascript
// Generate unique test data
const timestamp = Date.now();
const randomSuffix = Math.random().toString(36).substring(7);

pm.environment.set("testEmail", `test_${timestamp}@example.com`);
pm.environment.set("testUsername", `user_${randomSuffix}`);
pm.environment.set("testOrderId", `ORD-${timestamp}`);

// Generate realistic data
const names = ["Alice", "Bob", "Charlie", "Diana", "Eve"];
const randomName = names[Math.floor(Math.random() * names.length)];
pm.environment.set("testName", randomName);

// Generate valid phone number
const areaCode = Math.floor(Math.random() * 900) + 100;
const exchange = Math.floor(Math.random() * 900) + 100;
const subscriber = Math.floor(Math.random() * 9000) + 1000;
pm.environment.set("testPhone", `+1${areaCode}${exchange}${subscriber}`);
```

### Bruno Dynamic Variables

```javascript
script:pre-request {
  const uuid = require('uuid');

  bru.setVar("testId", uuid.v4());
  bru.setVar("testEmail", `test_${Date.now()}@example.com`);
  bru.setVar("testTimestamp", new Date().toISOString());
}
```

---

## Data Seeding

### API-Based Seeding

```javascript
// seed/create-test-user.bru
meta {
  name: Seed Test User
  seq: 1
}

post {
  url: {{baseUrl}}/api/admin/seed
  body: json
}

body:json {
  {
    "users": [
      {
        "email": "test-user@example.com",
        "password": "Test123!",
        "role": "admin"
      }
    ],
    "organizations": [
      {
        "name": "Test Org",
        "plan": "enterprise"
      }
    ]
  }
}

tests {
  test("Seeding successful", function() {
    expect(res.status).to.equal(200);
    bru.setVar("seededUserId", res.body.users[0].id);
    bru.setVar("seededOrgId", res.body.organizations[0].id);
  });
}
```

### Setup Collection Pattern

```
setup/
├── 01-reset-database.bru     # Clear test data
├── 02-create-admin.bru       # Create admin user
├── 03-create-test-org.bru    # Create organization
├── 04-create-test-users.bru  # Create test users
└── 05-verify-setup.bru       # Verify setup complete
```

---

## Environment-Specific Data

### Environment Variables

```javascript
// environments/local.bru
vars {
  baseUrl: http://localhost:3000
  adminEmail: admin@localhost
  testPassword: localtest123
}

// environments/staging.bru
vars {
  baseUrl: https://staging.api.com
  adminEmail: admin@staging.example.com
  testPassword: stagingtest123
}

// environments/ci.bru
vars {
  baseUrl: http://api:3000
  adminEmail: ci@test.example.com
  testPassword: citest123
}
```

### Secret Management

```javascript
// Don't commit secrets - use CI environment variables
// environments/ci.bru
vars {
  baseUrl: http://api:3000
}

vars:secret [
  apiKey,
  adminPassword,
  testUserToken
]
```

```bash
# Set secrets via CLI
bru run --env ci \
  --env-var "apiKey=$API_KEY" \
  --env-var "adminPassword=$ADMIN_PASSWORD"
```

---

## Data Cleanup

### Post-Test Cleanup

```javascript
// In test's post-response script
script:post-response {
  // Cleanup created resource
  if (res.status === 201 && res.body.id) {
    const deleteUrl = `${bru.getVar('baseUrl')}/api/users/${res.body.id}`;

    // Mark for cleanup (actual deletion in cleanup request)
    const toDelete = bru.getVar('resourcesToDelete') || [];
    toDelete.push({ type: 'user', id: res.body.id });
    bru.setVar('resourcesToDelete', JSON.stringify(toDelete));
  }
}
```

### Cleanup Collection

```javascript
// cleanup/delete-test-resources.bru
meta {
  name: Delete Test Resources
  seq: 999  // Run last
}

script:pre-request {
  const resources = JSON.parse(bru.getVar('resourcesToDelete') || '[]');
  bru.setVar('cleanupResources', JSON.stringify(resources));
}

// Multiple DELETE requests in loop (Postman)
const resources = JSON.parse(pm.environment.get('resourcesToDelete') || '[]');

resources.forEach(resource => {
    pm.sendRequest({
        url: `${pm.environment.get('baseUrl')}/api/${resource.type}s/${resource.id}`,
        method: 'DELETE',
        header: {
            'Authorization': `Bearer ${pm.environment.get('authToken')}`
        }
    }, (err, res) => {
        if (err) {
            console.log(`Failed to delete ${resource.type} ${resource.id}:`, err);
        } else {
            console.log(`Deleted ${resource.type} ${resource.id}`);
        }
    });
});
```

### Database Reset (CI)

```yaml
# GitHub Actions
- name: Reset Test Database
  run: |
    docker exec postgres psql -U postgres -d test -c "TRUNCATE users, orders CASCADE;"

- name: Run API Tests
  run: newman run collection.json -e ci.json
```

---

## Data Isolation

### Test User Prefixes

```javascript
// Use consistent prefix for test data
const TEST_PREFIX = "test_";

pm.environment.set("testEmail", `${TEST_PREFIX}${Date.now()}@example.com`);
pm.environment.set("testUsername", `${TEST_PREFIX}user_${Date.now()}`);

// Easy to identify and clean up
// DELETE FROM users WHERE email LIKE 'test_%'
```

### Dedicated Test Tenant

```javascript
// environments/ci.bru
vars {
  tenantId: test-tenant-001
  baseUrl: https://api.example.com/test-tenant-001
}

// All test data isolated to this tenant
```

### Request Tagging

```javascript
// Add header to identify test requests
headers {
  X-Test-Request: true
  X-Test-Run-Id: {{testRunId}}
}

// Server can log/track test requests separately
```

---

## Best Practices

### Data Independence

```javascript
// BAD - Tests depend on each other
// Test 1 creates user
// Test 2 expects user from Test 1

// GOOD - Each test creates its own data
script:pre-request {
  // Create fresh test user for this test
  bru.setVar("testEmail", `test_${Date.now()}@example.com`);
}
```

### Deterministic IDs for Debugging

```javascript
// Use predictable IDs in specific tests
const testCaseId = "TC001";
const timestamp = Date.now();
pm.environment.set("testEmail", `${testCaseId}_${timestamp}@example.com`);

// Easy to trace: "TC001_1612345678@example.com"
```

### Data Validation Before Use

```javascript
// Verify environment setup
pm.test("Environment configured correctly", function () {
    pm.expect(pm.environment.get("baseUrl")).to.exist;
    pm.expect(pm.environment.get("apiKey")).to.exist;
    pm.expect(pm.environment.get("testUserEmail")).to.exist;
});
```

### Idempotent Setup

```javascript
// Create-if-not-exists pattern
script:pre-request {
  const existingUserId = bru.getVar('testUserId');

  if (!existingUserId) {
    // User will be created by this request
    bru.setVar('shouldCreateUser', 'true');
  } else {
    // Skip creation, user already exists
    bru.setVar('shouldCreateUser', 'false');
  }
}
```
