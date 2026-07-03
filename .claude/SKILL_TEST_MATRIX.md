# Skill Activation Test Matrix

**Date:** 2026-07-03
**Total Skills:** 86 (2 stable, 84 active)
**Status:** 37/86 validated (carried from 2026-02-22 run) · 49/86 pending re-validation
**Note:** Rebuilt for the P14 harvest (70 → 82 skills). Trigger phrases sourced from each skill's `config.json` `activation_triggers`. ✅ marks are carried forward from the 2026-02-22 run only where the tested trigger phrase is unchanged in the current config; all other skills are marked ⏳ pending re-validation — no pass results are claimed for tests that were never run.
**Naming exceptions:** `nooks-autopilot`, `sdr-dial-lists`, `sdr-call-coaching`, `epiphan-call-playbook` deliberately omit the `-skill` suffix (live-automation names).

## Test Protocol

For each skill:
1. Use the trigger phrase in Claude Code
2. Verify skill activates (shows in skill panel)
3. Check YAML frontmatter parses correctly
4. Mark pass/fail

Legend: ✅ = passed (2026-02-22 run) · ⏳ = pending re-validation

---

## Core Skills (5)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 1 | workflow-enforcer-skill | "automatic on all sessions" | ⏳ | ⏳ | Stable; trigger changed since 2026-02-22 ("follow workflow" removed) — re-validate |
| 2 | project-context-skill | "load project context" / "save context" | ✅ | ✅ | Stable; PASS 2026-02-22 |
| 3 | workflow-orchestrator-skill | "start day" / "end day" | ✅ | ✅ | PASS 2026-02-22 |
| 4 | cost-metering-skill | "cost check" / "budget status" | ✅ | ✅ | PASS 2026-02-22 |
| 5 | portfolio-artifact-skill | "capture metrics" / "portfolio report" | ✅ | ✅ | PASS 2026-02-22 |

---

## Dev Tools (15)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 6 | extension-authoring-skill | "create skill" / "create hook" | ✅ | ✅ | PASS 2026-02-22 |
| 7 | debug-like-expert-skill | "debug systematically" / "root cause analysis" | ✅ | ✅ | PASS 2026-02-22 |
| 8 | planning-prompts-skill | "create plan" / "meta-prompt" | ✅ | ✅ | PASS 2026-02-22 |
| 9 | worktree-manager-skill | "create worktree" / "cleanup worktrees" | ✅ | ✅ | PASS 2026-02-22 |
| 10 | git-workflow-skill | "commit" / "PR" / "branch naming" | ✅ | ✅ | PASS 2026-02-22 |
| 11 | testing-skill | "write tests" / "TDD" / "test coverage" | ✅ | ✅ | PASS 2026-02-22 |
| 12 | api-design-skill | "design API" / "REST endpoints" | ✅ | ✅ | PASS 2026-02-22 |
| 13 | security-skill | "auth" / "JWT" / "security audit" | ✅ | ✅ | PASS 2026-02-22 |
| 14 | api-testing-skill | "postman" / "bruno" / "API testing" | ✅ | ✅ | PASS 2026-02-22 |
| 15 | docker-compose-skill | "docker compose" / "local dev" | ✅ | ✅ | PASS 2026-02-22 |
| 16 | agent-teams-skill | "set up agent team" / "parallel development" | ✅ | ✅ | PASS 2026-02-22 |
| 17 | subagent-teams-skill | "subagent team" / "fan out" / "parallel tasks" | ✅ | ✅ | PASS 2026-02-22 |
| 18 | agent-capability-matrix-skill | "which agent" / "route task" | ✅ | ✅ | PASS 2026-02-22 |
| 19 | heal-skill | "/heal-skill" / "fix broken skill" | ✅ | ✅ | PASS 2026-02-22 |
| 20 | frontend-ui-skill | "React component" / "Tailwind" / "shadcn" | ✅ | ✅ | PASS 2026-02-22 |

---

## Infrastructure (8)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 21 | unsloth-training-skill | "train with GRPO" / "fine-tune model" | ✅ | ✅ | PASS 2026-02-22 |
| 22 | langgraph-agents-skill | "LangGraph agent" / "multi-agent" | ✅ | ✅ | PASS 2026-02-22 |
| 23 | runpod-deployment-skill | "deploy to RunPod" / "GPU serverless" | ✅ | ✅ | PASS 2026-02-22 |
| 24 | groq-inference-skill | "groq" / "fast inference" | ✅ | ✅ | PASS 2026-02-22 |
| 25 | openrouter-skill | "openrouter" / "chinese llm" / "deepseek" | ✅ | ✅ | PASS 2026-02-22 |
| 26 | voice-ai-skill | "voice agent" / "Twilio" / "Deepgram" | ✅ | ✅ | PASS 2026-02-22 |
| 27 | supabase-sql-skill | "fix SQL" / "clean migration" | ✅ | ✅ | PASS 2026-02-22 |
| 28 | stripe-stack-skill | "stripe" / "payments" / "billing" | ✅ | ✅ | PASS 2026-02-22 |

---

## Business (19)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 29 | crm-integration-skill | "Close CRM" / "HubSpot" / "Salesforce" | ✅ | ✅ | PASS 2026-02-22 |
| 30 | gtm-pricing-skill | "GTM strategy" / "pricing" / "ICP" | ✅ | ✅ | PASS 2026-02-22 |
| 31 | research-skill | "research company" / "competitive analysis" | ✅ | ✅ | PASS 2026-02-22 |
| 32 | sales-revenue-skill | "discovery call" / "pipeline analysis" / "MEDDIC" | ⏳ | ⏳ | Triggers changed since 2026-02-22 ("cold email" removed in P13 Phase 3) — re-validate |
| 33 | content-marketing-skill | "content strategy" / "LinkedIn post" | ✅ | ✅ | PASS 2026-02-22 |
| 34 | data-analysis-skill | "analyze data" / "analytics dashboard" | ✅ | ✅ | PASS 2026-02-22 |
| 35 | trading-signals-skill | "fibonacci levels" / "elliott wave" / "wyckoff" | ✅ | ✅ | PASS 2026-02-22 |
| 36 | miro-skill | "miro board" / "visual diagram" | ✅ | ✅ | PASS 2026-02-22 |
| 37 | hubspot-revops-skill | "hubspot analytics" / "lead scoring" | ✅ | ✅ | PASS 2026-02-22 |
| 38 | ibkr-api-skill | "IBKR" / "Interactive Brokers" / "IB Gateway" | ⏳ | ⏳ | Added after 2026-02-22 run |
| 39 | prospect-research-to-cadence-skill | "research prospect" / "build cadence for" | ⏳ | ⏳ | Added after 2026-02-22 run |
| 40 | phone-verification-waterfall-skill | "verify phones" / "phone waterfall" / "who can I call" | ⏳ | ⏳ | Added after 2026-02-22 run |
| 41 | meddic-call-prep-auto-skill | "call prep" / "prep me for" / "demo prep" | ⏳ | ⏳ | Added after 2026-02-22 run |
| 42 | deal-momentum-analyzer-skill | "deal health" / "deal momentum" / "pipeline review" | ⏳ | ⏳ | Added after 2026-02-22 run |
| 43 | portfolio-deal-linker-skill | "portfolio update" / "deal closed" | ⏳ | ⏳ | Added after 2026-02-22 run |
| 44 | trading-alert-scheduler-skill | "market digest" / "trading alerts" / "pre-market scan" | ⏳ | ⏳ | Added after 2026-02-22 run |
| 45 | ae-handoff-brief-skill | "handoff to Phil" / "handoff to Lex" / "ae brief" | ⏳ | ⏳ | P13 Phase 4 promotion (2026-04-09) |
| 46 | call-recording-analyzer-skill | "analyze call" / "call review" / "score my call" | ⏳ | ⏳ | P13 Phase 4 promotion (2026-04-09) |
| 47 | dead-deal-recovery-skill | "dead deals" / "stalled deals" / "clean pipeline" | ⏳ | ⏳ | P13 Phase 4 promotion (2026-04-09) |

---

## BDR Automation (10)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 48 | prospect-enrich-skill | "prospect enrich" / "enrich phoneless" | ⏳ | ⏳ | Scheduled M-F 6:00 AM |
| 49 | prospect-refresh-skill | "prospect refresh" / "search new ICP" | ⏳ | ⏳ | Scheduled Mon 6:30 AM |
| 50 | sequence-load-skill | "sequence load" / "load sequences" / "enroll leads" | ⏳ | ⏳ | Scheduled Mon 7:15 AM |
| 51 | callable-lead-count-skill | "callable leads" / "lead inventory" / "ATL runway" | ⏳ | ⏳ | Scheduled M-F 7:25 AM |
| 52 | morning-brief-skill | "morning brief" / "today's dial list" | ⏳ | ⏳ | Scheduled M-F 7:30 AM |
| 53 | contact-hunter-skill | "find contact info" / "contact hunter" | ⏳ | ⏳ | Category per config.json: BDR Automation |
| 54 | he-dial-queue-skill | "build HE dial queue" / "refresh pod dial list" | ⏳ | ⏳ | NEW P14 harvest |
| 55 | nooks-autopilot | "run nooks autopilot" / "autonomous BDR run" / "hunt leads" | ⏳ | ⏳ | NEW P14 harvest; no `-skill` suffix (live-automation name) |
| 56 | sdr-dial-lists | "build SDR dial lists" / "Edgar's call list" / "Vasil's dial queue" | ⏳ | ⏳ | NEW P14 harvest; no `-skill` suffix (live-automation name) |
| 57 | sdr-call-coaching | "SDR call coaching" / "coaching cards" / "score SDR calls" | ⏳ | ⏳ | NEW P14 harvest; no `-skill` suffix (live-automation name) |

---

## Sales Intelligence (12)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 58 | champion-identifier-skill | "find champion" / "internal champion" | ⏳ | ⏳ | Imported skill |
| 59 | cold-email-sequence-generator-skill | "cold email sequence" / "email campaign" | ⏳ | ⏳ | Imported skill; A/B variant pilot |
| 60 | email-template-generator-skill | "email template" / "write email" | ⏳ | ⏳ | Imported skill |
| 61 | inbound-lead-qualifier-skill | "qualify inbound" / "score lead" | ⏳ | ⏳ | Imported skill |
| 62 | intent-signal-aggregator-skill | "intent signals" / "buyer intent" | ⏳ | ⏳ | Imported skill |
| 63 | linkedin-sales-navigator-alt-skill | "linkedin prospects" / "sales navigator" | ⏳ | ⏳ | Imported skill |
| 64 | lookalike-customer-finder-skill | "lookalike companies" / "similar companies" | ⏳ | ⏳ | Imported skill |
| 65 | meeting-intelligence-system-skill | "meeting notes" / "transcript analysis" | ⏳ | ⏳ | Imported skill |
| 66 | personalization-at-scale-skill | "personalize at scale" / "first lines" | ⏳ | ⏳ | Imported skill |
| 67 | pipeline-health-analyzer-skill | "pipeline health" / "forecast accuracy" | ⏳ | ⏳ | Imported skill |
| 68 | sales-methodology-implementer-skill | "sales methodology" / "implement MEDDIC" | ⏳ | ⏳ | Imported skill |
| 69 | social-selling-content-generator-skill | "social selling" / "LinkedIn content" | ⏳ | ⏳ | Imported skill |

---

## Sales Enablement (7) — NEW P14 Harvest

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 70 | epiphan-ai-mcp-guide-skill | "epiphan mcp" / "epiphan ai tools" / "crm tools" | ⏳ | ⏳ | NEW P14 harvest |
| 71 | business-pulse-skill | "business pulse" / "how are we doing" / "revenue pace" | ⏳ | ⏳ | NEW P14 harvest; "pipeline health" overlaps pipeline-health-analyzer — verify no conflict |
| 72 | close-plan-generator-skill | "close plan" / "build close plan" / "close strategy" | ⏳ | ⏳ | NEW P14 harvest |
| 73 | cost-discovery-coach-skill | "discovery questions" / "calculator discovery" | ⏳ | ⏳ | NEW P14 harvest |
| 74 | demo-execution-playbook-skill | "demo playbook" / "demo flow for" / "demo checklist" | ⏳ | ⏳ | NEW P14 harvest |
| 75 | greenfield-pearl-tracker-skill | "greenfield opportunities" / "new build" / "fly kit" | ⏳ | ⏳ | NEW P14 harvest |
| 76 | epiphan-call-playbook | "call script" / "cold call" / "objection handling" | ⏳ | ⏳ | NEW P14 harvest; no `-skill` suffix (live-automation name); "discovery call" overlaps sales-revenue — verify no conflict |

---

## Sales Automation (1) — NEW P14 Harvest

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 77 | post-demo-automation-skill | "post-demo" / "demo follow-up" / "send demo recap" | ⏳ | ⏳ | NEW P14 harvest |

---

## Strategy (5)

| # | Skill | Trigger Phrase | YAML | Activation | Notes |
|---|-------|---------------|------|------------|-------|
| 78 | business-model-canvas-skill | "business model canvas" / "value proposition" | ✅ | ✅ | PASS 2026-02-22 |
| 79 | blue-ocean-strategy-skill | "blue ocean" / "ERRC framework" | ✅ | ✅ | PASS 2026-02-22 |
| 80 | jobs-to-be-done-skill | "jobs to be done" / "JTBD" | ⏳ | ⏳ | Added after 2026-02-22 run |
| 81 | challenger-sale-skill | "challenger sale" / "commercial teaching" | ⏳ | ⏳ | Added after 2026-02-22 run |
| 82 | never-split-the-difference-skill | "never split the difference" / "tactical empathy" | ⏳ | ⏳ | Added after 2026-02-22 run |

---

## Summary

| Category | Count | Validated (2026-02-22) | Pending Re-validation |
|----------|-------|------------------------|-----------------------|
| Core | 5 | 4 | 1 |
| Dev Tools | 15 | 15 | 0 |
| Infrastructure | 8 | 8 | 0 |
| Business | 19 | 8 | 11 |
| BDR Automation | 10 | 0 | 10 |
| Sales Intelligence | 12 | 0 | 12 |
| Sales Enablement | 7 | 0 | 7 |
| Sales Automation | 1 | 0 | 1 |
| Strategy | 5 | 2 | 3 |
| P15 New | 4 | 0 | 4 |
| **Total** | **86** | **37** | **49** |

---

## Changes This Rebuild (2026-07-03 — P14)

| Change | Notes |
|--------|-------|
| Matrix rebuilt 39 → 82 skills | Covers every directory in `active/` (80) + `stable/` (2), verified via filesystem |
| 12 P14 harvest skills added | business-pulse, close-plan-generator, cost-discovery-coach, demo-execution-playbook, epiphan-ai-mcp-guide, greenfield-pearl-tracker, he-dial-queue, nooks-autopilot, post-demo-automation, sdr-dial-lists, sdr-call-coaching, epiphan-call-playbook |
| 31 previously-untracked skills added | Skills created between 2026-02-22 and P13 Phase 4 that never entered the matrix |
| PASS carried forward for 37 of original 39 | Trigger phrase verified unchanged in current config.json |
| 2 downgraded to pending | workflow-enforcer-skill ("follow workflow" removed), sales-revenue-skill ("cold email" removed in P13 Phase 3 trigger-conflict cleanup) |
| Categories realigned to config.json | contact-hunter now BDR Automation; new Sales Enablement + Sales Automation sections |
| 4 P15 skills added (82 → 86) | batch-send-drafts, orlob-discovery-framework, sdr-email-sms-playbook, weekly-kpi-report |

---

## Automated Testing

```bash
# Run all integration tests across all skills (T1-T9)
./scripts/test-skills.sh

# Verbose output (shows individual test results)
./scripts/test-skills.sh --verbose

# Test a single skill
./scripts/test-skills.sh --skill business-pulse-skill
```

Tests: T1 (files exist), T2 (YAML frontmatter), T3 (config.json schema), T4 (XML sections), T5 (line count), T6 (circular deps), T7 (integrates_with refs), T8 (activation_triggers), T9 (per-skill checks).

## Manual Test Commands

```bash
# Verify skill count (includes the 4 non--skill-suffix dirs)
ls -d active/*/ stable/*/ | wc -l
# Expected: 82

# Check YAML frontmatter (first 5 lines of each SKILL.md)
for dir in active/*/ stable/*/; do
  echo "=== $(basename $dir) ===" && head -5 "$dir/SKILL.md"
done
```
