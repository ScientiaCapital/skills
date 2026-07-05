# Patch: content-marketing-skill

**Score:** trigger=3 tool_integration=1 output_contract=2 failure_handling=1 maintainability=4 (sum=11/25)

**Highest-leverage single change (S effort):** Add a product-knowledge + brand gate for any Epiphan-specific claim and strip the stale hardcoded project/tool references.
**Expected impact:** Prevents unverified claims in published assets and stops the skill pointing users at defunct projects.

## Description

**Before:**
> B2B content marketing - thought leadership, SEO, LinkedIn, blog posts, case studies, and video scripts. Use when creating content strategy, writing posts, or building demand gen assets.

**After (proposed):**
> B2B content strategy + asset creation umbrella: content pillars, calendars, SEO blogs, case studies, video scripts, and repurposing. Use when: 'content strategy', 'content calendar', 'write a blog post', 'SEO article', 'case study', 'video script'. For LinkedIn-only post generation use social-selling-content-generator; for repurposing one asset into many use social-media-content-repurposer.

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 288): "- Quantified outcomes (3-5 metrics)"
- **Issue:** Case-study and blog frameworks instruct quantified customer results and product claims but never call search_product_knowledge/search_product_catalog to source them, and no brand gate on public copy. Pure template skill, zero tool integration.
- **Fix:** Gate any Epiphan-specific claim through product knowledge and run check_my_copy on customer-facing drafts.

### [MED] failure_handling
- **Evidence** (line 400): "Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated."
- **Issue:** Only status semantics defined; no run-state failure definition, no retry/degrade path, no run log. success_criteria are content-quality checks not run health.
- **Fix:** Add a degrade path (product-knowledge lookup fails -> mark partial, flag unverified claim) and a run log line.

### [MED] trigger_quality
- **Evidence** (line 3): "Use when creating content strategy, writing posts, or building demand gen assets."
- **Issue:** Broad demand-gen scope collides with social-selling-content-generator, webinar-to-content-multiplier, social-media-content-repurposer with no boundary.
- **Fix:** Position as the strategy/calendar/SEO umbrella and point to specialized skills for single-channel execution.

### [LOW] maintainability
- **Evidence** (line 381): "- **Projects**: coperniq-video-factory, gtm-engineer-journey"
- **Issue:** Hardcoded external project names (coperniq-video-factory, gtm-engineer-journey) and tool list (WordPress, Canva, Descript) that are stale/irrelevant to Epiphan BDR context and will drift.
- **Fix:** Remove or move stale integration notes to a reference file; keep SKILL.md context-neutral.

## Missing tool references

- search_product_knowledge
- search_product_catalog
- Epiphan Brand check_my_copy

## Self-healing gap (see specs/self-healing-template.md)

Status enum with partial/error semantics but no run-state failure definition, no retry->degrade->alert->halt ladder, no run log to ~/.claude/skill-runs/{skill}.jsonl. Good progressive disclosure (reference/*.md) but self-healing absent.

## Overlap candidates (flag only — no removal)

- social-selling-content-generator-skill
- webinar-to-content-multiplier
- social-media-content-repurposer
- seo-content-optimizer
- landing-page-copywriter
