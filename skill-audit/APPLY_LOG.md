# Apply Log — skill-audit patches, round 1

One line per skill: applied / skipped / deferred, and why. Priority order per skill-audit/priority.json (Fix now → Monitor → Revisit quarterly). Only skills with a skill-audit/patches/{skill}.patch.md were in scope for this run.

Skills present in priority.json but with no patch file (scored >3 on every dimension — no patch generated) are noted as "no patch" and were not touched: orlob-discovery-framework-skill, nooks-autopilot, weekly-kpi-report-skill, he-dial-queue-skill, sdr-call-coaching.

| Skill | Bucket | Status | Notes |
|---|---|---|---|
| contact-hunter-skill | Fix now | applied | Deleted orphaned legacy tail (dangling tags, duplicate card/CSV formats, email-guessing/Google-dork section); routed Stage 3 ATL/BTL through qualify_lead; added Gmail-draft handoff; added failure-handling section pointing at self-healing-template.md |
| content-marketing-skill | Fix now | applied | Added product-knowledge verification gate (search_product_knowledge/search_product_catalog) before Epiphan claims; added check_my_copy brand gate before customer-facing drafts; removed stale hardcoded project/tool references |
| business-pulse-skill | Fix now | applied | Added outcome sidecar (success/partial/error) + empty-data guard (never fabricate); added concrete delivery target (saved HTML report); de-duped owner-ID list to point at epiphan-ai-mcp-guide-skill |
| never-split-the-difference-skill | Fix now | applied | Added check_my_copy + get_writing_style brand gate before all email templates/voicemail script, staged via gmail_create_draft; flagged Ackerman pricing example as illustrative-only (needs search_product_catalog for real quotes); added failure-handling section + run log per self-healing-template.md. Skipped: moving court-system example to references/ (optional, out of single-file scope) |
| challenger-sale-skill | Fix now | applied | Added Spec Verification Gate (search_product_catalog/search_product_knowledge) before solution/competitive-reframe content; added Brand Gate (check_my_copy) before emails; added Gmail draft-first delivery contract; added failure ladder + run log per self-healing-template.md; disambiguated vs sales-methodology-implementer-skill. Skipped: moving worked example to references/ (optional/low priority) |
| meddic-call-prep-auto-skill | Fix now | applied | Added spec/competitor verification gate before Competitive Quick Reference table (hardcoded table now fallback-only, flagged unverified); replaced inline Golden Rules + ATL/BTL keyword tables with qualify_lead gate (kept MEDDIC-specific EB questions); added Gmail-draft/HTML delivery stage; added self-healing section per self-healing-template.md |
