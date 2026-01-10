# Pagination Patterns

## Comparison

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| Cursor | Real-time data, infinite scroll | Consistent, fast | Can't jump to page |
| Offset | Static data, page numbers | Simple, can jump | Slow on large data, drift |
| Keyset | Large datasets | Very fast | Requires sortable key |

## Cursor-Based Pagination

### Response Format

```typescript
interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    hasMore: boolean;
    nextCursor: string | null;
    prevCursor?: string | null;
  };
}
```

### Implementation

```typescript
// Encoding
function encodeCursor(data: object): string {
  return Buffer.from(JSON.stringify(data)).toString('base64url');
}

function decodeCursor(cursor: string): Record<string, unknown> {
  try {
    return JSON.parse(Buffer.from(cursor, 'base64url').toString());
  } catch {
    throw new ValidationError([{
      field: 'cursor',
      code: 'invalid_cursor',
      message: 'Invalid cursor format'
    }]);
  }
}

// Query
interface PaginationParams {
  limit?: number;
  cursor?: string;
}

async function getPosts(params: PaginationParams) {
  const limit = Math.min(params.limit || 20, 100); // Max 100
  const where: any = {};

  if (params.cursor) {
    const { id, createdAt } = decodeCursor(params.cursor);
    where.OR = [
      { createdAt: { lt: new Date(createdAt as string) } },
      {
        createdAt: new Date(createdAt as string),
        id: { lt: id as string }
      }
    ];
  }

  const posts = await db.post.findMany({
    where,
    orderBy: [
      { createdAt: 'desc' },
      { id: 'desc' }
    ],
    take: limit + 1, // Fetch one extra
  });

  const hasMore = posts.length > limit;
  const data = hasMore ? posts.slice(0, -1) : posts;

  const lastItem = data[data.length - 1];

  return {
    data,
    pagination: {
      hasMore,
      nextCursor: hasMore && lastItem
        ? encodeCursor({ id: lastItem.id, createdAt: lastItem.createdAt.toISOString() })
        : null,
    },
  };
}
```

### Bidirectional Cursors

```typescript
async function getPostsBidirectional(params: {
  limit?: number;
  after?: string;
  before?: string;
}) {
  const limit = Math.min(params.limit || 20, 100);

  let where: any = {};
  let orderBy: any = [{ createdAt: 'desc' }, { id: 'desc' }];

  if (params.after) {
    const { id, createdAt } = decodeCursor(params.after);
    where = {
      OR: [
        { createdAt: { lt: new Date(createdAt as string) } },
        { createdAt: new Date(createdAt as string), id: { lt: id } }
      ]
    };
  } else if (params.before) {
    const { id, createdAt } = decodeCursor(params.before);
    where = {
      OR: [
        { createdAt: { gt: new Date(createdAt as string) } },
        { createdAt: new Date(createdAt as string), id: { gt: id } }
      ]
    };
    orderBy = [{ createdAt: 'asc' }, { id: 'asc' }];
  }

  let posts = await db.post.findMany({
    where,
    orderBy,
    take: limit + 1,
  });

  // Reverse if we fetched backwards
  if (params.before) {
    posts = posts.reverse();
  }

  const hasMore = posts.length > limit;
  const data = hasMore ? posts.slice(0, -1) : posts;

  const firstItem = data[0];
  const lastItem = data[data.length - 1];

  return {
    data,
    pagination: {
      hasNextPage: hasMore,
      hasPrevPage: !!(params.after || params.before),
      startCursor: firstItem
        ? encodeCursor({ id: firstItem.id, createdAt: firstItem.createdAt.toISOString() })
        : null,
      endCursor: lastItem
        ? encodeCursor({ id: lastItem.id, createdAt: lastItem.createdAt.toISOString() })
        : null,
    },
  };
}
```

## Offset-Based Pagination

### Response Format

```typescript
interface OffsetPaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}
```

### Implementation

```typescript
async function getPostsOffset(params: { page?: number; limit?: number }) {
  const page = Math.max(params.page || 1, 1);
  const limit = Math.min(params.limit || 20, 100);
  const offset = (page - 1) * limit;

  const [posts, total] = await Promise.all([
    db.post.findMany({
      skip: offset,
      take: limit,
      orderBy: { createdAt: 'desc' },
    }),
    db.post.count(),
  ]);

  return {
    data: posts,
    pagination: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
    },
  };
}
```

### Performance Warning

```sql
-- This gets slower as offset increases
SELECT * FROM posts ORDER BY created_at DESC LIMIT 20 OFFSET 10000;
-- Database must scan 10,020 rows

-- Better: Use keyset pagination
SELECT * FROM posts
WHERE created_at < '2024-01-15T10:00:00Z'
ORDER BY created_at DESC
LIMIT 20;
-- Only scans 20 rows
```

## Keyset Pagination

### When to Use

- Very large datasets
- Single sort column
- No need for page numbers

### Implementation

```typescript
async function getPostsKeyset(params: {
  limit?: number;
  lastCreatedAt?: Date;
  lastId?: string;
}) {
  const limit = Math.min(params.limit || 20, 100);

  const where: any = {};
  if (params.lastCreatedAt && params.lastId) {
    where.OR = [
      { createdAt: { lt: params.lastCreatedAt } },
      {
        createdAt: params.lastCreatedAt,
        id: { lt: params.lastId }
      }
    ];
  }

  const posts = await db.post.findMany({
    where,
    orderBy: [
      { createdAt: 'desc' },
      { id: 'desc' }
    ],
    take: limit + 1,
  });

  const hasMore = posts.length > limit;
  const data = hasMore ? posts.slice(0, -1) : posts;
  const lastItem = data[data.length - 1];

  return {
    data,
    nextKey: hasMore && lastItem
      ? { createdAt: lastItem.createdAt, id: lastItem.id }
      : null,
  };
}
```

## GraphQL Pagination (Relay Style)

### Schema

```graphql
type Query {
  posts(first: Int, after: String, last: Int, before: String): PostConnection!
}

type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
  totalCount: Int
}

type PostEdge {
  node: Post!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

### Resolver

```typescript
async function postsResolver(
  _: unknown,
  args: { first?: number; after?: string; last?: number; before?: string }
) {
  const limit = args.first || args.last || 20;

  // ... fetch data with cursor logic ...

  return {
    edges: posts.map(post => ({
      node: post,
      cursor: encodeCursor({ id: post.id }),
    })),
    pageInfo: {
      hasNextPage: hasMore,
      hasPreviousPage: !!args.after,
      startCursor: posts[0] ? encodeCursor({ id: posts[0].id }) : null,
      endCursor: lastPost ? encodeCursor({ id: lastPost.id }) : null,
    },
    totalCount: await db.post.count(),
  };
}
```

## Best Practices

### Limits

```typescript
const DEFAULT_LIMIT = 20;
const MAX_LIMIT = 100;

function sanitizeLimit(requested?: number): number {
  if (!requested) return DEFAULT_LIMIT;
  if (requested < 1) return DEFAULT_LIMIT;
  if (requested > MAX_LIMIT) return MAX_LIMIT;
  return Math.floor(requested);
}
```

### Sorting + Pagination

```typescript
// Always include unique column in sort for stable pagination
const orderBy = [
  { [sortField]: sortOrder },
  { id: 'desc' } // Tiebreaker
];
```

### Total Count (Use Sparingly)

```typescript
// COUNT can be expensive on large tables
// Only include if needed
interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    hasMore: boolean;
    nextCursor: string | null;
    // total?: number; // Optional, expensive
  };
}

// If you need total, consider caching
const total = await redis.get('posts:count') ||
  await db.post.count();
```
