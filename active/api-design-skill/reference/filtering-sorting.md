# Filtering and Sorting

## Query Parameters

```
# Simple filters
GET /users?status=active
GET /users?role=admin&status=active

# Range filters
GET /orders?created_after=2024-01-01
GET /orders?total_min=100&total_max=500

# Search
GET /products?search=keyboard
GET /products?q=wireless+keyboard

# Sorting
GET /posts?sort=created_at&order=desc
GET /posts?sort=-created_at  # Prefix with - for desc

# Multiple sorts
GET /posts?sort=status,-created_at

# Field selection (sparse fieldsets)
GET /users?fields=id,name,email
GET /users/{id}?include=posts,comments
```

## Implementation

```typescript
const filterSchema = z.object({
  status: z.enum(['active', 'inactive', 'all']).optional(),
  search: z.string().max(100).optional(),
  created_after: z.coerce.date().optional(),
  created_before: z.coerce.date().optional(),
  sort: z.string().optional(),
  order: z.enum(['asc', 'desc']).default('desc'),
  fields: z.string().optional(),
});

function buildQuery(filters: z.infer<typeof filterSchema>) {
  const where: any = {};

  if (filters.status && filters.status !== 'all') {
    where.status = filters.status;
  }

  if (filters.search) {
    where.OR = [
      { name: { contains: filters.search, mode: 'insensitive' } },
      { email: { contains: filters.search, mode: 'insensitive' } },
    ];
  }

  if (filters.created_after) {
    where.createdAt = { gte: filters.created_after };
  }

  return where;
}
```
