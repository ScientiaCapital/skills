# API Versioning

## Versioning Strategies

### URL Path Versioning (Recommended)

```
GET /api/v1/users
GET /api/v2/users
```

**Pros:**
- Clear and explicit
- Easy to test (just change URL)
- Easy to document
- Works with caching

**Cons:**
- URL pollution
- Need to maintain multiple versions

### Header Versioning

```
GET /api/users
Accept: application/vnd.myapi.v2+json
```

**Pros:**
- Clean URLs
- RESTful purists prefer it

**Cons:**
- Hidden from casual inspection
- Harder to test
- Can't bookmark specific version

### Query Parameter Versioning

```
GET /api/users?version=2
```

**Pros:**
- Easy to add
- Works in browser

**Cons:**
- Pollutes query string
- Optional = default version issues

## When to Create a New Version

### Breaking Changes (Require New Version)

```typescript
// Removing a field
// v1
{ "id": "123", "name": "John", "email": "john@example.com" }

// v2 (email removed - BREAKING)
{ "id": "123", "name": "John" }

// Changing field type
// v1
{ "id": 123 }  // number

// v2 (changed to string - BREAKING)
{ "id": "user_123" }

// Renaming fields
// v1
{ "user_name": "John" }

// v2
{ "userName": "John" }  // Different key - BREAKING

// Changing response structure
// v1
{ "users": [...] }

// v2
{ "data": [...], "pagination": {...} }  // Different shape - BREAKING

// Removing endpoints
// DELETE /api/v1/users/deactivate → BREAKING if removed in v2
```

### Non-Breaking Changes (No New Version Needed)

```typescript
// Adding new optional fields
// v1
{ "id": "123", "name": "John" }

// Still v1 (backwards compatible)
{ "id": "123", "name": "John", "avatar": "https://..." }

// Adding new endpoints
// Still v1
POST /api/v1/users/export  // New endpoint

// Adding new optional query parameters
// Still v1
GET /api/v1/users?include=posts  // New optional param

// Adding new enum values (if client handles unknown gracefully)
// Still v1
{ "status": "archived" }  // New status value
```

## Implementation

### Route Organization

```
src/
├── api/
│   ├── v1/
│   │   ├── users/
│   │   │   ├── route.ts
│   │   │   └── [id]/route.ts
│   │   └── posts/
│   │       └── route.ts
│   └── v2/
│       ├── users/
│       │   ├── route.ts
│       │   └── [id]/route.ts
│       └── posts/
│           └── route.ts
```

### Shared Logic

```typescript
// Shared business logic
// services/userService.ts
export class UserService {
  async getUser(id: string) {
    return db.user.findUnique({ where: { id } });
  }

  async createUser(data: CreateUserInput) {
    return db.user.create({ data });
  }
}

// v1 route - original format
// api/v1/users/route.ts
import { UserService } from '@/services/userService';

export async function GET(req: Request) {
  const users = await userService.getUsers();

  // v1 response format
  return Response.json({
    users: users.map(u => ({
      id: u.id,
      user_name: u.name,  // snake_case in v1
      email: u.email,
    }))
  });
}

// v2 route - new format
// api/v2/users/route.ts
import { UserService } from '@/services/userService';

export async function GET(req: Request) {
  const users = await userService.getUsers();

  // v2 response format
  return Response.json({
    data: users.map(u => ({
      id: u.id,
      userName: u.name,  // camelCase in v2
      // email removed in v2
    })),
    pagination: { hasMore: false }
  });
}
```

### Version Transformers

```typescript
// Transform internal model to versioned response
interface UserInternal {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
}

// v1 transformer
function toV1User(user: UserInternal) {
  return {
    id: user.id,
    user_name: user.name,
    email: user.email,
    created_at: user.createdAt.toISOString(),
  };
}

// v2 transformer
function toV2User(user: UserInternal) {
  return {
    id: user.id,
    userName: user.name,
    createdAt: user.createdAt.toISOString(),
    // email intentionally omitted
  };
}
```

## Deprecation Strategy

### Deprecation Headers

```typescript
// Add deprecation headers
res.setHeader('Deprecation', 'true');
res.setHeader('Sunset', 'Sat, 1 Jan 2025 00:00:00 GMT');
res.setHeader('Link', '</api/v2/users>; rel="successor-version"');
```

### Deprecation Response Field

```typescript
// Include in response body
{
  "data": [...],
  "_meta": {
    "deprecation": {
      "message": "This API version is deprecated",
      "sunsetDate": "2025-01-01",
      "migrationGuide": "https://docs.example.com/migration/v1-to-v2"
    }
  }
}
```

### Deprecation Timeline

1. **Announce** - 6+ months before sunset
2. **Add warnings** - Headers and response metadata
3. **Reduce support** - No new features, security fixes only
4. **Sunset** - Return 410 Gone

```typescript
// After sunset date
if (apiVersion === 'v1' && new Date() > sunsetDate) {
  return Response.json(
    {
      error: {
        code: 'api_version_sunset',
        message: 'API v1 has been retired. Please upgrade to v2.',
        migrationGuide: 'https://docs.example.com/migration'
      }
    },
    { status: 410 } // Gone
  );
}
```

## Version Discovery

### Root Endpoint

```typescript
// GET /api
{
  "versions": {
    "v1": {
      "status": "deprecated",
      "sunset": "2025-01-01",
      "url": "/api/v1"
    },
    "v2": {
      "status": "current",
      "url": "/api/v2"
    },
    "v3": {
      "status": "beta",
      "url": "/api/v3"
    }
  },
  "currentVersion": "v2",
  "documentation": "https://docs.example.com/api"
}
```

## Best Practices

### Do's
- Version from day one
- Use URL path versioning for simplicity
- Share business logic between versions
- Provide migration guides
- Give long deprecation windows (6+ months)
- Monitor version usage before sunsetting

### Don'ts
- Don't create new version for every change
- Don't remove versions without warning
- Don't break backwards compatibility within a version
- Don't have too many active versions (2-3 max)
- Don't version internal APIs the same way
