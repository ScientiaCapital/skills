# Rollback & Recovery Procedures

Comprehensive guide for safely rolling back changes, recovering from failures, and maintaining system stability.

## When to Rollback

### Automatic Rollback Triggers
```python
ROLLBACK_TRIGGERS = {
    'test_failures': {
        'condition': lambda metrics: metrics['test_pass_rate'] < 0.95,
        'severity': 'HIGH',
        'action': 'immediate_rollback'
    },
    'security_issues': {
        'condition': lambda scan: scan['critical_vulns'] > 0,
        'severity': 'CRITICAL',
        'action': 'immediate_rollback'
    },
    'performance_degradation': {
        'condition': lambda perf: perf['response_time'] > perf['baseline'] * 1.5,
        'severity': 'HIGH',
        'action': 'gradual_rollback'
    },
    'error_rate_spike': {
        'condition': lambda errors: errors['rate'] > errors['baseline'] * 3,
        'severity': 'HIGH',
        'action': 'immediate_rollback'
    },
    'memory_leak': {
        'condition': lambda mem: mem['growth_rate'] > 0.1,  # 10% per hour
        'severity': 'MEDIUM',
        'action': 'scheduled_rollback'
    },
}
```

### Manual Rollback Decisions
```markdown
## Rollback Decision Matrix

| Symptom | Investigation | Rollback? | Alternative |
|---------|---------------|-----------|-------------|
| Tests failing after "fix" | Check if fix addressed root cause | Yes | Debug properly |
| New security warnings | Verify if real vulnerabilities | Yes | Patch immediately |
| Performance slower | Profile and measure impact | Maybe | Optimize first |
| Unexpected behavior | Compare with requirements | Maybe | Feature flag off |
| User complaints | Quantify impact and severity | Maybe | Hotfix if minor |
| Data corruption risk | Assess data integrity | Yes | Immediate action |
```

## Rollback Strategies

### 1. Git-Based Rollback

#### Simple Revert
```bash
#!/bin/bash
# simple-rollback.sh

# Find the last known good commit
echo "Recent commits:"
git log --oneline -10

read -p "Enter the commit hash to revert to: " COMMIT_HASH

# Create a revert commit
git revert $COMMIT_HASH --no-edit

# Verify the revert
echo "Changes reverted:"
git diff HEAD~1
```

#### Selective File Rollback
```bash
#!/bin/bash
# selective-rollback.sh

# Rollback specific files only
FILES_TO_ROLLBACK=(
    "src/api/auth.py"
    "src/models/user.py"
    "tests/test_auth.py"
)

# Find last known good state
GOOD_COMMIT=$(git log --format="%H %s" | grep -m1 "stable:" | cut -d' ' -f1)

# Rollback each file
for file in "${FILES_TO_ROLLBACK[@]}"; do
    echo "Rolling back $file to $GOOD_COMMIT"
    git checkout $GOOD_COMMIT -- $file
done

# Show what changed
git status
git diff --staged
```

#### Branch-Based Rollback
```bash
#!/bin/bash
# branch-rollback.sh

# Create a rollback branch
ROLLBACK_BRANCH="rollback/$(date +%Y%m%d_%H%M%S)"
git checkout -b $ROLLBACK_BRANCH

# Reset to known good state
LAST_GOOD_TAG=$(git tag -l "stable-*" | sort -V | tail -1)
git reset --hard $LAST_GOOD_TAG

# Cherry-pick safe commits if any
read -p "Any commits to keep? (comma-separated hashes): " KEEP_COMMITS
if [ ! -z "$KEEP_COMMITS" ]; then
    IFS=',' read -ra COMMITS <<< "$KEEP_COMMITS"
    for commit in "${COMMITS[@]}"; do
        git cherry-pick $commit || echo "Failed to cherry-pick $commit"
    done
fi
```

### 2. Database Rollback

#### Migration Rollback
```python
#!/usr/bin/env python3
# db-rollback.py

import subprocess
import json
from datetime import datetime

class DatabaseRollback:
    """Handle database migration rollbacks safely."""
    
    def __init__(self, connection_string):
        self.conn = connection_string
        self.backup_before_rollback = True
        
    def rollback_migration(self, target_version=None):
        """Rollback database migrations."""
        
        # 1. Create backup first
        if self.backup_before_rollback:
            backup_name = f"rollback_backup_{datetime.now():%Y%m%d_%H%M%S}"
            self.create_backup(backup_name)
            
        # 2. Check current version
        current = self.get_current_version()
        print(f"Current version: {current}")
        
        # 3. Determine target
        if not target_version:
            target_version = self.get_previous_version()
            
        print(f"Rolling back to: {target_version}")
        
        # 4. Execute rollback
        try:
            # Using Alembic
            subprocess.run([
                "alembic", "downgrade", target_version
            ], check=True)
            
            # OR using Django
            # subprocess.run([
            #     "python", "manage.py", "migrate", "app_name", target_version
            # ], check=True)
            
            print("Rollback successful")
            
        except subprocess.CalledProcessError as e:
            print(f"Rollback failed: {e}")
            self.restore_from_backup(backup_name)
            raise
            
    def create_backup(self, backup_name):
        """Create database backup before rollback."""
        print(f"Creating backup: {backup_name}")
        
        # PostgreSQL example
        subprocess.run([
            "pg_dump",
            self.conn,
            "-f", f"backups/{backup_name}.sql"
        ], check=True)
        
    def get_migration_history(self):
        """Get migration history."""
        # Implementation depends on migration tool
        pass
```

#### Data Rollback Strategy
```sql
-- Create audit table for data rollback
CREATE TABLE IF NOT EXISTS data_audit (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(255),
    operation VARCHAR(10),
    row_data JSONB,
    changed_by VARCHAR(255),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trigger to capture changes
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO data_audit (table_name, operation, row_data, changed_by)
    VALUES (
        TG_TABLE_NAME,
        TG_OP,
        CASE
            WHEN TG_OP = 'DELETE' THEN row_to_json(OLD)
            ELSE row_to_json(NEW)
        END,
        current_user
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to critical tables
CREATE TRIGGER user_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();
```

### 3. Application Rollback

#### Container-Based Rollback
```bash
#!/bin/bash
# container-rollback.sh

SERVICE_NAME=$1
ROLLBACK_VERSION=${2:-"previous"}

echo "Rolling back $SERVICE_NAME to $ROLLBACK_VERSION"

# Kubernetes rollback
if command -v kubectl &> /dev/null; then
    kubectl rollout history deployment/$SERVICE_NAME
    
    if [ "$ROLLBACK_VERSION" = "previous" ]; then
        kubectl rollout undo deployment/$SERVICE_NAME
    else
        kubectl rollout undo deployment/$SERVICE_NAME --to-revision=$ROLLBACK_VERSION
    fi
    
    kubectl rollout status deployment/$SERVICE_NAME
    
# Docker Swarm rollback
elif command -v docker &> /dev/null; then
    docker service rollback $SERVICE_NAME
    docker service ps $SERVICE_NAME
fi

# Verify rollback
./scripts/smoke-test.sh $SERVICE_NAME
```

#### Feature Flag Rollback
```python
class FeatureFlagRollback:
    """Rollback using feature flags."""
    
    def __init__(self, flag_service):
        self.flags = flag_service
        
    def emergency_disable(self, feature_name, reason):
        """Emergency disable a feature."""
        
        # 1. Disable feature
        self.flags.disable(feature_name)
        
        # 2. Clear caches
        self.clear_feature_caches(feature_name)
        
        # 3. Log the action
        self.log_rollback({
            'feature': feature_name,
            'action': 'emergency_disable',
            'reason': reason,
            'timestamp': datetime.now(),
            'disabled_by': get_current_user()
        })
        
        # 4. Notify team
        self.notify_team(
            f"Feature {feature_name} disabled: {reason}"
        )
        
        # 5. Create incident
        incident_id = self.create_incident({
            'title': f"Feature {feature_name} rolled back",
            'severity': 'P2',
            'reason': reason
        })
        
        return incident_id
        
    def gradual_rollback(self, feature_name, target_percentage=0):
        """Gradually reduce feature exposure."""
        
        current = self.flags.get_rollout_percentage(feature_name)
        
        while current > target_percentage:
            # Reduce by 10% every 5 minutes
            new_percentage = max(current - 10, target_percentage)
            
            self.flags.set_rollout_percentage(
                feature_name,
                new_percentage
            )
            
            # Monitor metrics
            metrics = self.monitor_metrics(5 * 60)  # 5 minutes
            
            if metrics['error_rate'] > metrics['baseline'] * 2:
                # Accelerate rollback
                self.flags.set_rollout_percentage(feature_name, 0)
                break
                
            current = new_percentage
```

### 4. Infrastructure Rollback

#### Terraform State Rollback
```bash
#!/bin/bash
# terraform-rollback.sh

# List state history
terraform state list

# Create backup
terraform state pull > terraform.tfstate.backup.$(date +%Y%m%d_%H%M%S)

# Rollback specific resources
RESOURCES_TO_ROLLBACK=(
    "aws_instance.web"
    "aws_db_instance.main"
    "aws_security_group.api"
)

for resource in "${RESOURCES_TO_ROLLBACK[@]}"; do
    echo "Rolling back $resource"
    
    # Import previous state
    terraform import $resource $PREVIOUS_RESOURCE_ID
    
    # Or remove and recreate
    # terraform state rm $resource
    # terraform apply -target=$resource
done
```

## Recovery Workflows

### 1. Incident Response Recovery
```python
class IncidentRecovery:
    """Coordinate incident recovery procedures."""
    
    def __init__(self):
        self.playbook = self.load_playbook()
        self.team = self.get_on_call_team()
        
    def initiate_recovery(self, incident_type, severity):
        """Start recovery procedure."""
        
        incident = {
            'id': generate_incident_id(),
            'type': incident_type,
            'severity': severity,
            'started': datetime.now(),
            'status': 'active',
            'commander': self.assign_incident_commander(),
        }
        
        # Execute playbook
        playbook_steps = self.playbook.get_steps(incident_type)
        
        for step in playbook_steps:
            result = self.execute_step(step, incident)
            
            if not result['success']:
                self.escalate(incident, step, result['error'])
                
        return incident
        
    def execute_step(self, step, incident):
        """Execute recovery step."""
        
        print(f"Executing: {step['name']}")
        
        try:
            if step['type'] == 'rollback':
                return self.perform_rollback(step['target'])
            elif step['type'] == 'restart':
                return self.restart_service(step['service'])
            elif step['type'] == 'scale':
                return self.scale_service(step['service'], step['replicas'])
            elif step['type'] == 'failover':
                return self.initiate_failover(step['from'], step['to'])
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'step': step['name']
            }
```

### 2. Data Recovery
```python
class DataRecovery:
    """Handle data recovery scenarios."""
    
    def __init__(self, backup_service):
        self.backup = backup_service
        
    def recover_from_corruption(self, table_name, corruption_time):
        """Recover from data corruption."""
        
        recovery_plan = {
            'table': table_name,
            'corruption_detected': datetime.now(),
            'corruption_occurred': corruption_time,
            'steps': []
        }
        
        # 1. Isolate corrupted data
        temp_table = f"{table_name}_corrupted_{datetime.now():%Y%m%d_%H%M%S}"
        recovery_plan['steps'].append({
            'action': 'isolate',
            'sql': f"CREATE TABLE {temp_table} AS SELECT * FROM {table_name}"
        })
        
        # 2. Find last good backup
        backup = self.backup.find_backup_before(corruption_time)
        recovery_plan['backup_used'] = backup['id']
        
        # 3. Restore from backup
        recovery_plan['steps'].append({
            'action': 'restore',
            'source': backup['path'],
            'target': table_name
        })
        
        # 4. Replay transactions after backup
        transactions = self.get_transactions_after(backup['timestamp'])
        
        for txn in transactions:
            if txn['timestamp'] < corruption_time:
                recovery_plan['steps'].append({
                    'action': 'replay_transaction',
                    'transaction': txn
                })
                
        # 5. Verify data integrity
        recovery_plan['steps'].append({
            'action': 'verify',
            'checks': [
                'row_count',
                'constraint_validation',
                'referential_integrity'
            ]
        })
        
        return recovery_plan
```

### 3. Service Recovery
```bash
#!/bin/bash
# service-recovery.sh

SERVICE=$1
MAX_ATTEMPTS=3
ATTEMPT=0

echo "=== Service Recovery: $SERVICE ==="

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    ATTEMPT=$((ATTEMPT + 1))
    echo "Attempt $ATTEMPT of $MAX_ATTEMPTS"
    
    # 1. Check service status
    if systemctl is-active --quiet $SERVICE; then
        echo "Service is running"
        break
    fi
    
    # 2. Try to start service
    echo "Starting service..."
    systemctl start $SERVICE
    
    # 3. Wait for service to stabilize
    sleep 10
    
    # 4. Health check
    if curl -f http://localhost:8080/health > /dev/null 2>&1; then
        echo "Service is healthy"
        break
    else
        echo "Health check failed"
        
        # 5. Check logs
        echo "Recent errors:"
        journalctl -u $SERVICE -n 20 --no-pager | grep -i error
        
        # 6. Try recovery actions
        case $ATTEMPT in
            1)
                echo "Clearing cache..."
                rm -rf /var/cache/$SERVICE/*
                ;;
            2)
                echo "Resetting configuration..."
                cp /etc/$SERVICE/config.default /etc/$SERVICE/config
                ;;
            3)
                echo "Final attempt - full restart..."
                systemctl stop $SERVICE
                sleep 5
                systemctl start $SERVICE
                ;;
        esac
    fi
done

if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
    echo "FAILED to recover service after $MAX_ATTEMPTS attempts"
    exit 1
else
    echo "Service recovered successfully"
fi
```

## Rollback Verification

### Automated Verification Suite
```python
class RollbackVerification:
    """Verify rollback success."""
    
    def __init__(self):
        self.checks = []
        
    def verify_rollback(self, rollback_id):
        """Run comprehensive rollback verification."""
        
        results = {
            'rollback_id': rollback_id,
            'timestamp': datetime.now(),
            'checks': {},
            'overall_status': 'pending'
        }
        
        # 1. Version verification
        results['checks']['version'] = self.verify_version()
        
        # 2. Functionality tests
        results['checks']['smoke_tests'] = self.run_smoke_tests()
        
        # 3. Data integrity
        results['checks']['data_integrity'] = self.verify_data_integrity()
        
        # 4. Performance baseline
        results['checks']['performance'] = self.verify_performance()
        
        # 5. Security scan
        results['checks']['security'] = self.run_security_scan()
        
        # 6. Integration tests
        results['checks']['integrations'] = self.test_integrations()
        
        # Determine overall status
        failed_checks = [
            check for check, result in results['checks'].items()
            if not result['passed']
        ]
        
        if not failed_checks:
            results['overall_status'] = 'success'
        elif len(failed_checks) <= 2:
            results['overall_status'] = 'partial_success'
        else:
            results['overall_status'] = 'failed'
            
        return results
        
    def run_smoke_tests(self):
        """Run critical path smoke tests."""
        
        tests = [
            ('user_login', self.test_user_login),
            ('api_health', self.test_api_health),
            ('database_connection', self.test_db_connection),
            ('critical_endpoints', self.test_critical_endpoints),
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                test_func()
                results.append({'test': test_name, 'status': 'passed'})
            except Exception as e:
                results.append({
                    'test': test_name,
                    'status': 'failed',
                    'error': str(e)
                })
                
        return {
            'passed': all(r['status'] == 'passed' for r in results),
            'details': results
        }
```

## Recovery Playbooks

### Database Corruption Playbook
```markdown
# Database Corruption Recovery Playbook

## Immediate Actions (0-5 minutes)
1. **ALERT TEAM** - Page on-call DBA
2. **ISOLATE** - Prevent further writes
   ```sql
   ALTER DATABASE mydb SET default_transaction_read_only = on;
   ```
3. **SNAPSHOT** - Create immediate backup
   ```bash
   pg_dump corrupted_db > emergency_backup_$(date +%s).sql
   ```

## Assessment (5-15 minutes)
1. Identify corruption scope
2. Determine last known good state
3. Estimate data loss window
4. Choose recovery strategy

## Recovery Strategies
### Option A: Point-in-Time Recovery
- Best when: Corruption time is known
- Data loss: Minimal
- Time: 30-60 minutes

### Option B: Backup Restore
- Best when: Recent backup available
- Data loss: Since last backup
- Time: 15-30 minutes

### Option C: Replica Promotion
- Best when: Healthy replica exists
- Data loss: Replication lag only
- Time: 5-10 minutes

## Validation
1. Run integrity checks
2. Verify row counts
3. Test application functionality
4. Monitor for recurring issues
```

### Service Outage Playbook
```python
SERVICE_PLAYBOOK = {
    'detection': {
        'alerts': ['pager_duty', 'slack', 'email'],
        'escalation_time': 5,  # minutes
    },
    'triage': {
        'steps': [
            'check_service_status',
            'review_recent_changes',
            'examine_logs',
            'check_dependencies',
            'assess_impact'
        ]
    },
    'mitigation': {
        'quick_wins': [
            'restart_service',
            'clear_cache',
            'increase_resources',
            'enable_fallback'
        ],
        'rollback_triggers': [
            'recent_deployment',
            'config_change',
            'dependency_update'
        ]
    },
    'recovery': {
        'verification': [
            'health_checks',
            'synthetic_monitoring',
            'real_user_monitoring',
            'error_rate_baseline'
        ]
    },
    'postmortem': {
        'timeline': 'within_48_hours',
        'participants': ['oncall', 'service_owner', 'sre'],
        'deliverables': ['root_cause', 'action_items', 'runbook_updates']
    }
}
```

## Prevention Strategies

### 1. Rollback Readiness
```yaml
# rollback-readiness.yaml
rollback_requirements:
  version_control:
    - semantic_versioning: true
    - tagged_releases: true
    - rollback_scripts: true
    
  database:
    - reversible_migrations: true
    - backup_frequency: hourly
    - backup_retention: 30_days
    
  application:
    - feature_flags: true
    - backward_compatibility: 2_versions
    - health_checks: comprehensive
    
  infrastructure:
    - immutable_deployments: true
    - blue_green_capable: true
    - state_management: versioned
```

### 2. Automated Rollback Testing
```python
def test_rollback_capability():
    """Test rollback procedures in staging."""
    
    # Deploy new version
    deploy_version("v2.0.0")
    
    # Verify deployment
    assert health_check() == "healthy"
    
    # Simulate rollback scenarios
    scenarios = [
        'immediate_rollback',
        'rollback_under_load',
        'partial_rollback',
        'data_migration_rollback'
    ]
    
    for scenario in scenarios:
        # Execute rollback
        rollback_result = execute_rollback_scenario(scenario)
        
        # Verify rollback
        assert rollback_result['success']
        assert version_check() == "v1.9.0"
        assert data_integrity_check() == "passed"
        
        # Restore to new version for next test
        deploy_version("v2.0.0")
```

### 3. Rollback Metrics
```python
ROLLBACK_METRICS = {
    'mttr': {  # Mean Time To Rollback
        'target': 300,  # 5 minutes
        'measurement': 'from_decision_to_stable'
    },
    'rollback_success_rate': {
        'target': 0.99,  # 99%
        'measurement': 'successful_rollbacks / total_rollbacks'
    },
    'automated_rollback_percentage': {
        'target': 0.80,  # 80%
        'measurement': 'automated_rollbacks / total_rollbacks'
    },
    'data_loss_incidents': {
        'target': 0,
        'measurement': 'count_per_quarter'
    }
}
```