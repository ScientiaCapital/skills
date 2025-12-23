# Skills Library

**Branch**: main | **Updated**: 2025-12-23

## Status
Production-ready skills library with 16 skills (2 stable, 14 active). Today added 6 GTM/sales skills for GTME path and copied all to global `~/.claude/skills/`.

## Today's Focus
1. [x] Build gtm-strategy-skill (ICP, positioning, messaging)
2. [x] Build demo-discovery-skill (SPIN, MEDDIC, objection handling)
3. [x] Build revenue-ops-skill (pipeline, CAC/LTV, forecasting)
4. [x] Build content-marketing-skill (LinkedIn, blog SEO, case studies)
5. [x] Build pricing-strategy-skill (tiering, packaging, psychology)
6. [x] Build voice-ai-skill (Cartesia, Deepgram, Twilio, ElevenLabs)
7. [x] Copy all 6 new skills to ~/.claude/skills/
8. [x] Create zips for Claude Desktop in dist/
9. [x] Update SKILLS_INDEX.md with all new entries
10. [x] Run enterprise security/quality checklist

## Done (This Session)
- Created 6 new skills in active/:
  - gtm-strategy-skill (205 lines + 1 reference file)
  - demo-discovery-skill (284 lines)
  - revenue-ops-skill (323 lines)
  - content-marketing-skill (367 lines)
  - pricing-strategy-skill (401 lines)
  - voice-ai-skill (431 lines)
- Copied all to ~/.claude/skills/ (now 16 total)
- Created 6 new zips in dist/ (now 16 total)
- Updated SKILLS_INDEX.md (skill count: 10 → 16)
- Security scan: CLEAN (no secrets, no actual OpenAI usage)
- Frontmatter validation: All valid (name + description only)

## Blockers
None

## Quick Commands
```bash
# View all skills
cat SKILLS_INDEX.md

# Check global skills
ls ~/.claude/skills/

# View zips
ls dist/*.zip
```

## Tech Stack
Markdown | YAML frontmatter | Progressive Disclosure Architecture
