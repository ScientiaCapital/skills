# Supabase Row Level Security (RLS)

## RLS Basics

### Why RLS?

```
Without RLS:
┌─────────┐         ┌─────────┐         ┌─────────┐
│ Client  │────────>│   API   │────────>│   DB    │
└─────────┘         └─────────┘         └─────────┘
                    Must check           Trusts API
                    every query

With RLS:
┌─────────┐         ┌─────────┐         ┌─────────┐
│ Client  │────────>│   API   │────────>│   DB    │
└─────────┘         └─────────┘         └─────────┘
                    Can be simpler       Enforces rules
                                        automatically
```

### Enable RLS

```sql
-- Enable on table
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Force RLS for table owner (important!)
ALTER TABLE posts FORCE ROW LEVEL SECURITY;
```

## Policy Patterns

### User Owns Resource

```sql
-- Users can CRUD their own posts
CREATE POLICY "Users manage own posts"
  ON posts
  FOR ALL
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Or split by operation
CREATE POLICY "Users read own posts"
  ON posts FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users create own posts"
  ON posts FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users update own posts"
  ON posts FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users delete own posts"
  ON posts FOR DELETE
  USING (auth.uid() = user_id);
```

### Public Read, Owner Write

```sql
-- Anyone can read published posts
CREATE POLICY "Public read published posts"
  ON posts FOR SELECT
  USING (status = 'published');

-- Only owner can write
CREATE POLICY "Owner manages posts"
  ON posts
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Owner updates posts"
  ON posts FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Owner deletes posts"
  ON posts FOR DELETE
  USING (auth.uid() = user_id);
```

### Organization/Team Access

```sql
-- Users can access resources in their organization
CREATE POLICY "Org members access"
  ON documents FOR SELECT
  USING (
    org_id IN (
      SELECT org_id
      FROM org_members
      WHERE user_id = auth.uid()
    )
  );

-- Admins can do everything
CREATE POLICY "Org admins manage"
  ON documents FOR ALL
  USING (
    org_id IN (
      SELECT org_id
      FROM org_members
      WHERE user_id = auth.uid()
        AND role = 'admin'
    )
  );
```

### Role-Based Access

```sql
-- Check role from JWT claims
CREATE POLICY "Admin full access"
  ON users FOR ALL
  USING (
    auth.jwt() ->> 'role' = 'admin'
  );

-- Or use a roles table
CREATE POLICY "Managers can view team"
  ON employees FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_id = auth.uid()
        AND role IN ('admin', 'manager')
    )
  );
```

## Helper Functions

### Get Current User ID

```sql
-- auth.uid() returns the user's UUID
SELECT auth.uid();

-- Check if user is authenticated
CREATE POLICY "Authenticated only"
  ON sensitive_data FOR SELECT
  USING (auth.uid() IS NOT NULL);
```

### Get JWT Claims

```sql
-- Access custom claims from JWT
CREATE POLICY "Verified email only"
  ON premium_content FOR SELECT
  USING (
    (auth.jwt() -> 'email_verified')::boolean = true
  );

-- Check custom role claim
CREATE POLICY "Premium users"
  ON premium_features FOR SELECT
  USING (
    auth.jwt() ->> 'subscription_tier' = 'premium'
  );
```

### Reusable Policy Functions

```sql
-- Create helper function
CREATE OR REPLACE FUNCTION is_org_member(org_uuid uuid)
RETURNS boolean AS $$
  SELECT EXISTS (
    SELECT 1 FROM org_members
    WHERE org_id = org_uuid
      AND user_id = auth.uid()
  );
$$ LANGUAGE sql SECURITY DEFINER;

-- Use in policies
CREATE POLICY "Org members read"
  ON documents FOR SELECT
  USING (is_org_member(org_id));

CREATE POLICY "Org members write"
  ON documents FOR INSERT
  WITH CHECK (is_org_member(org_id));
```

## Common Patterns

### Soft Delete

```sql
-- Only show non-deleted records
CREATE POLICY "Hide deleted"
  ON posts FOR SELECT
  USING (deleted_at IS NULL);

-- Prevent hard delete, only soft delete
CREATE POLICY "Soft delete only"
  ON posts FOR DELETE
  USING (false); -- Block all deletes

-- Allow update to set deleted_at
CREATE POLICY "Allow soft delete"
  ON posts FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (
    -- Only allow setting deleted_at, not other fields when deleting
    -- This is simplified; real implementation would be more complex
    auth.uid() = user_id
  );
```

### Time-Based Access

```sql
-- Content expires
CREATE POLICY "Not expired"
  ON content FOR SELECT
  USING (expires_at > now() OR expires_at IS NULL);

-- Allow access during business hours
CREATE POLICY "Business hours"
  ON reports FOR SELECT
  USING (
    EXTRACT(HOUR FROM now()) BETWEEN 9 AND 17
  );
```

### Hierarchical Access

```sql
-- Parent record grants access
CREATE POLICY "Project members access tasks"
  ON tasks FOR SELECT
  USING (
    project_id IN (
      SELECT id FROM projects
      WHERE id = tasks.project_id
      -- Projects policy checks membership
    )
  );

-- Or explicit membership
CREATE POLICY "Task access via project"
  ON tasks FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM project_members
      WHERE project_id = tasks.project_id
        AND user_id = auth.uid()
    )
  );
```

## Testing Policies

### Test as Different Users

```sql
-- Set role to authenticated user
SET request.jwt.claim.sub = 'user-uuid-here';

-- Test query
SELECT * FROM posts;

-- Reset
RESET request.jwt.claim.sub;
```

### Verify Policy Coverage

```sql
-- List all policies
SELECT
  schemaname,
  tablename,
  policyname,
  permissive,
  roles,
  cmd,
  qual,
  with_check
FROM pg_policies
WHERE tablename = 'posts';

-- Check RLS is enabled
SELECT
  relname,
  relrowsecurity,
  relforcerowsecurity
FROM pg_class
WHERE relname = 'posts';
```

## Performance Tips

### Index for Policy Columns

```sql
-- If policy checks user_id frequently
CREATE INDEX idx_posts_user_id ON posts(user_id);

-- For organization queries
CREATE INDEX idx_documents_org_id ON documents(org_id);
CREATE INDEX idx_org_members_user_org ON org_members(user_id, org_id);
```

### Avoid Complex Subqueries

```sql
-- SLOW: Subquery in every row check
CREATE POLICY "Slow"
  ON posts FOR SELECT
  USING (
    (SELECT role FROM users WHERE id = auth.uid()) = 'admin'
  );

-- FASTER: Use function with SECURITY DEFINER
CREATE OR REPLACE FUNCTION is_admin()
RETURNS boolean AS $$
  SELECT EXISTS (
    SELECT 1 FROM users
    WHERE id = auth.uid()
      AND role = 'admin'
  );
$$ LANGUAGE sql SECURITY DEFINER STABLE;

CREATE POLICY "Fast"
  ON posts FOR SELECT
  USING (is_admin());
```

## Debugging

### Check Applied Policies

```sql
-- See what policies affect a query
EXPLAIN (ANALYZE, VERBOSE) SELECT * FROM posts;

-- Check if RLS is blocking
-- Run as service_role (bypasses RLS) vs authenticated
```

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| No rows returned | Policy too restrictive | Check USING clause |
| Insert fails | WITH CHECK fails | Check WITH CHECK clause |
| Still seeing all rows | RLS not enabled | `ALTER TABLE ... ENABLE ROW LEVEL SECURITY` |
| Service role sees all | Service role bypasses RLS | This is expected behavior |

## Migration Checklist

- [ ] RLS enabled on all tables with user data
- [ ] FORCE ROW LEVEL SECURITY on sensitive tables
- [ ] Policies cover all operations (SELECT, INSERT, UPDATE, DELETE)
- [ ] Tested with different user roles
- [ ] Indexed columns used in policies
- [ ] No overly complex subqueries in policies
- [ ] Service role used only on server, never exposed
