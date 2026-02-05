# CI/CD Integration for API Testing

## Newman (Postman CLI)

### Installation

```bash
# Global install
npm install -g newman

# Project dependency
npm install --save-dev newman

# With reporters
npm install -g newman-reporter-htmlextra newman-reporter-junit
```

### Basic Usage

```bash
# Run collection
newman run collection.json

# With environment
newman run collection.json -e staging.json

# With data file
newman run collection.json -d test-data.json

# Multiple iterations
newman run collection.json -n 5

# Specific folder only
newman run collection.json --folder "Users"

# Delay between requests (ms)
newman run collection.json --delay-request 100

# Timeout settings
newman run collection.json --timeout-request 30000 --timeout-script 5000
```

### Reporters

```bash
# CLI output (default)
newman run collection.json

# JUnit for CI
newman run collection.json \
  --reporters junit \
  --reporter-junit-export results.xml

# HTML report
newman run collection.json \
  --reporters htmlextra \
  --reporter-htmlextra-export report.html

# Multiple reporters
newman run collection.json \
  --reporters cli,junit,htmlextra \
  --reporter-junit-export results.xml \
  --reporter-htmlextra-export report.html
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All tests passed |
| 1 | Test failures |
| 2 | Invalid collection |
| 3 | Runtime error |

---

## Bruno CLI

### Installation

```bash
# Global install
npm install -g @usebruno/cli

# Via npx (no install)
npx @usebruno/cli run
```

### Basic Usage

```bash
# Run all requests
bru run

# With environment
bru run --env staging

# Specific file
bru run users/create-user.bru --env local

# Specific folder
bru run users/ --env staging

# Environment variable override
bru run --env staging --env-var "baseUrl=http://localhost:3000"

# Output results
bru run --env ci --output results.json
```

---

## GitHub Actions

### Basic Workflow

```yaml
name: API Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  api-tests:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install Newman
        run: npm install -g newman newman-reporter-htmlextra

      - name: Run API Tests
        run: |
          newman run tests/api/collection.json \
            -e tests/api/ci.json \
            --reporters cli,htmlextra \
            --reporter-htmlextra-export report.html

      - name: Upload Report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: api-test-report
          path: report.html
          retention-days: 7
```

### With Secrets

```yaml
- name: Run API Tests
  env:
    API_KEY: ${{ secrets.STAGING_API_KEY }}
    AUTH_TOKEN: ${{ secrets.TEST_AUTH_TOKEN }}
  run: |
    newman run collection.json \
      -e ci.json \
      --env-var "apiKey=$API_KEY" \
      --env-var "authToken=$AUTH_TOKEN"
```

### With Service Container

```yaml
jobs:
  api-tests:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      api:
        image: my-api:test
        env:
          DATABASE_URL: postgres://test:test@postgres:5432/test
        ports:
          - 3000:3000

    steps:
      - uses: actions/checkout@v4

      - name: Wait for API
        run: |
          timeout 60 bash -c 'until curl -s http://localhost:3000/health; do sleep 2; done'

      - name: Run Tests
        run: |
          newman run collection.json \
            --env-var "baseUrl=http://localhost:3000"
```

### Matrix Testing (Multiple Environments)

```yaml
jobs:
  api-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [staging, production-readonly]

    steps:
      - uses: actions/checkout@v4

      - name: Run Tests - ${{ matrix.environment }}
        run: |
          newman run collection.json \
            -e environments/${{ matrix.environment }}.json \
            --reporters cli,junit \
            --reporter-junit-export results-${{ matrix.environment }}.xml
```

---

## GitLab CI

### Basic Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - test

api-tests:
  stage: test
  image: node:20

  before_script:
    - npm install -g newman newman-reporter-junit

  script:
    - newman run collection.json
        -e ci.json
        --reporters cli,junit
        --reporter-junit-export results.xml

  artifacts:
    when: always
    reports:
      junit: results.xml
    paths:
      - results.xml
    expire_in: 1 week
```

### With Variables

```yaml
api-tests:
  stage: test
  variables:
    API_KEY: $STAGING_API_KEY  # From GitLab CI/CD settings

  script:
    - newman run collection.json
        -e ci.json
        --env-var "apiKey=$API_KEY"
```

---

## CircleCI

### Basic Config

```yaml
# .circleci/config.yml
version: 2.1

jobs:
  api-tests:
    docker:
      - image: cimg/node:20.0

    steps:
      - checkout

      - run:
          name: Install Newman
          command: npm install -g newman

      - run:
          name: Run API Tests
          command: |
            newman run collection.json \
              -e ci.json \
              --reporters cli,junit \
              --reporter-junit-export results.xml

      - store_test_results:
          path: results.xml

      - store_artifacts:
          path: results.xml

workflows:
  test:
    jobs:
      - api-tests
```

---

## Jenkins

### Pipeline Script

```groovy
pipeline {
    agent any

    tools {
        nodejs 'node-20'
    }

    stages {
        stage('Setup') {
            steps {
                sh 'npm install -g newman newman-reporter-junit'
            }
        }

        stage('API Tests') {
            steps {
                withCredentials([string(credentialsId: 'api-key', variable: 'API_KEY')]) {
                    sh '''
                        newman run collection.json \
                            -e ci.json \
                            --env-var "apiKey=$API_KEY" \
                            --reporters cli,junit \
                            --reporter-junit-export results.xml
                    '''
                }
            }
            post {
                always {
                    junit 'results.xml'
                }
            }
        }
    }
}
```

---

## Reporting

### HTML Report (htmlextra)

```bash
newman run collection.json \
  --reporters htmlextra \
  --reporter-htmlextra-export report.html \
  --reporter-htmlextra-title "API Test Report" \
  --reporter-htmlextra-browserTitle "API Tests" \
  --reporter-htmlextra-showEnvironmentData \
  --reporter-htmlextra-showGlobalData
```

### JUnit for CI Integration

```bash
newman run collection.json \
  --reporters junit \
  --reporter-junit-export results.xml
```

### Custom JSON Output

```bash
newman run collection.json \
  --reporters json \
  --reporter-json-export results.json
```

### Combining Reporters

```bash
newman run collection.json \
  --reporters cli,junit,htmlextra \
  --reporter-junit-export junit-results.xml \
  --reporter-htmlextra-export detailed-report.html
```

---

## Best Practices

### Environment Configuration

```javascript
// ci.json - Minimal CI environment
{
    "name": "CI",
    "values": [
        {
            "key": "baseUrl",
            "value": "http://localhost:3000",
            "enabled": true
        },
        {
            "key": "timeout",
            "value": "30000",
            "enabled": true
        }
    ]
}
```

### Fail Fast

```bash
# Stop on first failure
newman run collection.json --bail
```

### Parallel Execution

```yaml
# GitHub Actions - parallel jobs
jobs:
  api-tests:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        folder: [users, orders, payments]

    steps:
      - name: Run ${{ matrix.folder }} tests
        run: |
          newman run collection.json \
            --folder "${{ matrix.folder }}" \
            -e ci.json
```

### Retry on Flaky Tests

```yaml
# GitHub Actions retry
- name: Run API Tests
  uses: nick-fields/retry@v2
  with:
    timeout_minutes: 10
    max_attempts: 3
    command: newman run collection.json -e ci.json
```

### Scheduled Health Checks

```yaml
# Run API health checks every hour
name: API Health Check

on:
  schedule:
    - cron: '0 * * * *'  # Every hour

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Health Checks
        run: |
          newman run collection.json \
            --folder "Health Checks" \
            -e production.json
```

### Notifications

```yaml
# Slack notification on failure
- name: Notify Slack on Failure
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "API Tests Failed",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "API tests failed on `${{ github.ref_name }}`\n<${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|View Run>"
            }
          }
        ]
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```
