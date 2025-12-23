# Function & Trigger Patterns for Supabase

## Updated_at Trigger

Standard pattern for auto-updating `updated_at` column:

```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_my_table_updated_at ON my_table;
CREATE TRIGGER update_my_table_updated_at
    BEFORE UPDATE ON my_table
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

## Atomic Credit/Balance Deduction

Pattern for safe balance updates with audit trail:

```sql
CREATE OR REPLACE FUNCTION deduct_credits(
    p_user_id UUID,
    p_amount INTEGER,
    p_reason TEXT
)
RETURNS TABLE (success BOOLEAN, new_balance INTEGER, error_message TEXT)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_current_balance INTEGER;
BEGIN
    -- Lock row for atomic update
    SELECT balance INTO v_current_balance
    FROM user_credits
    WHERE user_id = p_user_id
    FOR UPDATE;

    IF NOT FOUND THEN
        RETURN QUERY SELECT false, 0, 'User not found'::TEXT;
        RETURN;
    END IF;

    IF v_current_balance < p_amount THEN
        RETURN QUERY SELECT false, v_current_balance, 'Insufficient balance'::TEXT;
        RETURN;
    END IF;

    -- Deduct
    UPDATE user_credits
    SET balance = balance - p_amount, updated_at = NOW()
    WHERE user_id = p_user_id;

    -- Audit trail
    INSERT INTO transactions (user_id, amount, balance_before, balance_after, reason)
    VALUES (p_user_id, -p_amount, v_current_balance, v_current_balance - p_amount, p_reason);

    RETURN QUERY SELECT true, v_current_balance - p_amount, NULL::TEXT;
END;
$$;
```

## Workflow Step Status Aggregator

Auto-update parent status based on child step states:

```sql
CREATE OR REPLACE FUNCTION update_workflow_status_from_steps()
RETURNS TRIGGER AS $$
DECLARE
    v_total INTEGER;
    v_completed INTEGER;
    v_failed INTEGER;
BEGIN
    SELECT
        COUNT(*),
        COUNT(*) FILTER (WHERE status IN ('completed', 'skipped')),
        COUNT(*) FILTER (WHERE status = 'failed')
    INTO v_total, v_completed, v_failed
    FROM workflow_steps
    WHERE execution_id = NEW.execution_id;

    IF v_failed > 0 THEN
        UPDATE workflow_executions
        SET status = 'failed', completed_at = NOW()
        WHERE id = NEW.execution_id;
    ELSIF v_completed = v_total THEN
        UPDATE workflow_executions
        SET status = 'completed', completed_at = NOW()
        WHERE id = NEW.execution_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS trg_update_workflow_status ON workflow_steps;
CREATE TRIGGER trg_update_workflow_status
    AFTER UPDATE OF status ON workflow_steps
    FOR EACH ROW
    EXECUTE FUNCTION update_workflow_status_from_steps();
```

## Batch Insert Helper

Create multiple related records in one call:

```sql
CREATE OR REPLACE FUNCTION create_workflow_with_steps(
    p_workflow_type TEXT,
    p_business_id UUID
)
RETURNS UUID AS $$
DECLARE
    v_execution_id UUID;
BEGIN
    -- Create parent
    INSERT INTO workflow_executions (workflow_type, business_id, status)
    VALUES (p_workflow_type, p_business_id, 'pending')
    RETURNING id INTO v_execution_id;

    -- Create children
    INSERT INTO workflow_steps (execution_id, step_name, step_order, step_type)
    VALUES
        (v_execution_id, 'step_1', 1, 'init'),
        (v_execution_id, 'step_2', 2, 'process'),
        (v_execution_id, 'step_3', 3, 'complete');

    RETURN v_execution_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

## Granting Permissions

```sql
-- For authenticated users (RLS still applies)
GRANT SELECT ON my_view TO authenticated;

-- For service role functions
GRANT EXECUTE ON FUNCTION my_function(UUID) TO service_role;
```
