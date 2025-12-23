# RLS Policy Patterns for Supabase

## Standard User-Owns-Record Pattern

```sql
ALTER TABLE my_table ENABLE ROW LEVEL SECURITY;

-- View own records
DROP POLICY IF EXISTS "Users view own records" ON my_table;
CREATE POLICY "Users view own records" ON my_table
    FOR SELECT
    USING (user_id = auth.uid());

-- Create own records
DROP POLICY IF EXISTS "Users create own records" ON my_table;
CREATE POLICY "Users create own records" ON my_table
    FOR INSERT
    WITH CHECK (user_id = auth.uid());

-- Update own records
DROP POLICY IF EXISTS "Users update own records" ON my_table;
CREATE POLICY "Users update own records" ON my_table
    FOR UPDATE
    USING (user_id = auth.uid());

-- Delete own records
DROP POLICY IF EXISTS "Users delete own records" ON my_table;
CREATE POLICY "Users delete own records" ON my_table
    FOR DELETE
    USING (user_id = auth.uid());

-- Service role full access
DROP POLICY IF EXISTS "Service role full access" ON my_table;
CREATE POLICY "Service role full access" ON my_table
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);
```

## Business-Scoped Pattern

User can access records belonging to their business:

```sql
DROP POLICY IF EXISTS "Users view business records" ON my_table;
CREATE POLICY "Users view business records" ON my_table
    FOR SELECT
    USING (
        business_id IN (
            SELECT id FROM businesses WHERE user_id = auth.uid()
        )
    );
```

## Combined User OR Business Pattern

```sql
DROP POLICY IF EXISTS "Users view own or business records" ON my_table;
CREATE POLICY "Users view own or business records" ON my_table
    FOR SELECT
    USING (
        user_id = auth.uid()
        OR business_id IN (
            SELECT id FROM businesses WHERE user_id = auth.uid()
        )
    );
```

## Public Read Pattern

```sql
DROP POLICY IF EXISTS "Anyone can view active records" ON pricing_config;
CREATE POLICY "Anyone can view active records" ON pricing_config
    FOR SELECT
    USING (is_active = true);
```

## Nested Access (through parent table)

```sql
-- User can view steps if they own the parent execution
DROP POLICY IF EXISTS "Users view own workflow steps" ON workflow_steps;
CREATE POLICY "Users view own workflow steps" ON workflow_steps
    FOR SELECT
    USING (
        execution_id IN (
            SELECT we.id FROM workflow_executions we
            JOIN businesses b ON we.business_id = b.id
            WHERE b.user_id = auth.uid()
        )
    );
```

## Common Mistakes

### Wrong: JWT check for service role
```sql
-- This doesn't work reliably
USING (auth.jwt() ->> 'role' = 'service_role')
```

### Correct: TO clause for service role
```sql
-- Always use TO service_role
FOR ALL TO service_role USING (true) WITH CHECK (true)
```

### Wrong: Missing WITH CHECK on INSERT
```sql
-- INSERT needs WITH CHECK, not USING
FOR INSERT USING (user_id = auth.uid())  -- WRONG
FOR INSERT WITH CHECK (user_id = auth.uid())  -- CORRECT
```
