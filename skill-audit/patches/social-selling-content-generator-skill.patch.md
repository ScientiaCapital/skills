# Patch: social-selling-content-generator-skill

**Score:** trigger=3 tool_integration=1 output_contract=2 failure_handling=2 maintainability=2 (sum=10/25)

**Highest-leverage single change (M effort):** Swap generic SaaS personas/stats for Epiphan ICP verticals + real product-knowledge proof points, and add a brand check on Epiphan-referencing posts.
**Expected impact:** Makes generated content on-ICP and on-brand instead of generic filler Tim must rewrite.

## Description

**Before:**
> Generate 30+ LinkedIn posts that attract your target prospects. Creates industry insights, thought leadership, engagement prompts, and comment strategies. Use when building personal brand to attract inbound leads through social selling.

**After (proposed):**
> Generate a 30-day LinkedIn post calendar (industry insight, thought-leadership, engagement prompts) to attract Epiphan ICP prospects and drive inbound. Use when: 'create LinkedIn posts', 'social selling content', '30 days of posts', 'build my personal brand'. For refining an existing draft use linkedin-post-optimizer; for multi-channel repurposing use social-media-content-repurposer.

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 95): "Here's what I'm seeing with 200+ B2B sales teams:"
- **Issue:** No tool calls at all. Fabricated authority stats and hardcoded SaaS persona examples baked into the template; no search_product_knowledge for Epiphan claims, no brand gate for public LinkedIn copy carrying Tim's name.
- **Fix:** Add Epiphan Brand check_my_copy gate for any Epiphan-referencing post; pull real proof points from product knowledge instead of placeholder stats.

### [MED] maintainability
- **Evidence** (line 186-187): "### For CTOs/VPs Engineering
- **Problems**: Developer productivity, tech debt, hiring, infrastructure costs"
- **Issue:** Personas (VP Sales, CTO/VP Eng) and examples are generic SaaS, not Epiphan verticals (Higher Ed, Courts, Gov, Healthcare per CLAUDE.md). Hardcoded off-ICP examples drift users away from real ICP.
- **Fix:** Replace persona set with Epiphan ATL personas and vertical proof points, or reference a shared personas file.

### [MED] output_contract
- **Evidence** (line 15): "**Output:** 30-day content calendar with posts, comment strategies, engagement tactics, and persona-specific templates"
- **Issue:** Output is a markdown calendar with no delivery/staging mechanism (no scheduling, no draft location, no handoff).
- **Fix:** Define where the calendar lands (file/artifact) and how posts get staged for review.

### [MED] trigger_quality
- **Evidence** (line 3): "Use when building personal brand to attract inbound leads through social selling."
- **Issue:** Overlaps linkedin-post-optimizer, content-marketing, social-media-content-repurposer with no boundary.
- **Fix:** Narrow to 'net-new LinkedIn post generation' and point to linkedin-post-optimizer for refining existing drafts.

## Missing tool references

- Epiphan Brand check_my_copy
- Epiphan Brand get_writing_style
- search_product_knowledge

## Self-healing gap (see specs/self-healing-template.md)

Only an outcome sidecar with a partial/error status note; no failure definition tied to run state, no retry->degrade->alert->halt ladder, no run log to ~/.claude/skill-runs/{skill}.jsonl.

## Overlap candidates (flag only — no removal)

- content-marketing-skill
- linkedin-post-optimizer
- social-media-content-repurposer
- linkedin-sales-navigator-alt-skill
