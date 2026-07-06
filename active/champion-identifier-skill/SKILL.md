---
name: champion-identifier-skill
description: Analyze LinkedIn profiles in target accounts to identify potential internal champions. Evaluates role, career path, mutual connections, interests, and suggests personalization approach. Use when you need to find who will champion your solution internally.
---

# Champion Identifier

<objective>
Analyze target accounts to identify the individuals most likely to become internal champions who will advocate for your solution. Scores candidates on role relevance, influence, accessibility, change-agent traits, personal stake, and engagement potential, then provides ranked recommendations with outreach strategies and multi-threading plans.
</objective>

<quick_start>
**Trigger:** "Find potential champions at [Company]" or "Who at [Company] would internally advocate for our solution?" — this is the champion/advocacy play (multi-candidate, influence-scored). For a single named-person point-lookup, use `contact-hunter-skill` instead.
**Input:** Target company name, your solution/product, any existing contacts
**Output:** Ranked champion candidates — sourced from real HubSpot/Apollo contact data, ATL/BTL/gray tier from `qualify_lead` — with scores (0-60), outreach templates staged as Gmail drafts, org chart, and multi-threading strategy
**MCP Tools:** `mcp__claude_ai_Epiphan_Ai__hubspot_search_contacts`, `mcp__claude_ai_Apollo_io__apollo_contacts_search`, `qualify_lead`, `mcp__claude_ai_Gmail__create_draft`, `mcp__claude_ai_Epiphan_Ai__hubspot_create_contact_note`
</quick_start>

<success_criteria>
- [ ] Company context analyzed (stage, news, pain points, decision style)
- [ ] Candidates sourced from real data — `hubspot_search_contacts` first, `apollo_contacts_search` waterfall for org-chart gaps — never invented names or titles
- [ ] `qualify_lead` called on every candidate for ATL/BTL/gray tier before ranking (per `skill-audit/specs/suppression-spec.md`) — no inline "Director/VP level" or keyword-based ATL derivation
- [ ] 3-4 champion candidates identified and scored on 6 dimensions, each grounded in a real signal (title/tenure from HubSpot/Apollo, engagement from HubSpot activity history)
- [ ] Each candidate has outreach strategy (warm intro or direct); outreach template staged as a Gmail draft for the top 1-2 candidates
- [ ] Multi-threading plan with coverage map provided
- [ ] Warning signs and red flags documented
- [ ] Champion development plan with phased actions included
- [ ] "No champion found" degrade path applied if no candidate clears the `qualify_lead` gate; sidecar `atl_count` sourced from `qualify_lead`, not self-reported
</success_criteria>

<workflow>

## What Makes a Great Champion?

**The Champion Profile**:
- **Has Pain**: Directly affected by the problem you solve
- **Has Power**: Can influence decision or control budget
- **Has Gain**: Personally benefits when you win (promotion, bonus, easier life)
- **Is Accessible**: You can reach them and build relationship
- **Is Willing**: Open to new solutions and vendors

**Champion vs. Coach vs. Blocker**:
- **Champion**: Actively sells for you internally, has skin in the game
- **Coach**: Helpful but passive, gives you intel but won't advocate
- **Blocker**: Opposes your solution (loves incumbent, risk-averse, loses if you win)

## Stage 1: Source Real Candidates (HubSpot + Apollo)

Champion candidates must come from real contact data — never invented from a persona
description or LinkedIn inference alone.

**MCP Tool:** `mcp__claude_ai_Epiphan_Ai__hubspot_search_contacts`
```
Search by: company name / domain
Return: contactId, firstName, lastName, jobtitle, department, hubspot_owner_id,
        lifecyclestage, last_activity_date, and engagement history (email opens/replies,
        meetings, form fills) for each existing contact at the account
```

If HubSpot returns fewer than 3-4 plausible candidates (thin account coverage), fill org-chart
gaps with:

**MCP Tool:** `mcp__claude_ai_Apollo_io__apollo_contacts_search`
```
Search by: organization_name
Filters: seniority IN [manager, director, vp, c_suite], country IN [US, CA]
```

Every candidate that reaches the Scoring Framework, DMU table, or Output Format below must
trace back to a `hubspot_search_contacts` or `apollo_contacts_search` result. If neither tool
returns usable candidates, do not fabricate names — see the no-champion degrade path (Stage 2).

## Stage 2: ATL/BTL Gate — `qualify_lead`

Call `qualify_lead` on every Stage 1 candidate before scoring or ranking. Per
`skill-audit/specs/suppression-spec.md`, this is the single gate for ATL/BTL/gray tiering,
Golden Rules, and suppression — do not re-derive "Director/VP level" or NEVER-ATL keyword
tables inline.

- `power_level = atl` → eligible to lead with; score and rank normally
- `power_level = gray` → include, flagged for manual review — Tim decides whether to lead with them
- `power_level = btl` → keep as a Coach/User-tier contact (see Warning Signs / Who NOT to Lead
  With); never rank as the #1-#3 champion
- `junk = true` or suppressed → exclude entirely, note the reason

**No-champion degrade path:** if zero candidates clear `power_level ∈ {atl, gray}`, do not force
a ranking to fill three slots. Output whatever DMU/org-chart context was found, mark the run
`status: "partial"` with `error: "no_champion_above_threshold"`, and recommend the Discovery
Questions path below to surface a champion on the next call instead.

## Scoring Framework

**Scoring Dimensions** (0-10 each) — score only candidates that passed Stage 1 (real source)
and Stage 2 (`qualify_lead`):
1. **Role Relevance** - How directly does their role relate to your solution? (ground in the real `jobtitle`/`department`, not a guess)
2. **Influence Level** - Can they affect the buying decision? (informed by `qualify_lead`'s `power_level`, not a replacement for it — see Stage 2 for the actual ATL/BTL tier)
3. **Accessibility** - Can you reach them? Warm intro possible? (existing HubSpot owner/contact, or a real mutual-connection signal)
4. **Change Agent** - Track record of adopting new solutions? (from real tenure/history where available; otherwise score conservatively and say "insufficient data")
5. **Personal Stake** - Do they personally gain if you win?
6. **Engagement Potential** - Likely to respond to outreach? (ground in real HubSpot engagement history — opens, replies, meetings; if no engagement history exists, score ≤5/10 and note "no engagement history" rather than inventing a number)

**Total Champion Score**: 0-60 points
- 50-60: Ideal champion candidate
- 40-49: Strong potential champion
- 30-39: Possible champion with work
- Below 30: Not likely to champion

**ATL/BTL is never re-derived here** — the tier shown throughout (candidate cards, DMU table,
sidecar `atl_count`) is the `qualify_lead` `power_level` from Stage 2.

## Output Format

```markdown
# Champion Identification: [Company Name]

**Company**: [Company Name] | **Industry**: [Industry] | **Size**: [Employees]
**Your Solution**: [What you sell] | **Analysis Date**: [Date]

---

## Target Account Overview

**Company Context**:
- Stage: [Startup/Growth/Enterprise] | Recent News: [Funding/Growth/Changes]
- Likely Pain Points: [Based on stage and industry]
- Decision-Making Style: [Committee/Top-down/Consensus]

**Your Connection**:
- Existing Contacts: [X] | Mutual Connections: [X] 2nd degree
- Inbound Interest: [Yes/No] | Competitive Intel: [Competitor?]

---

## Champion Candidates (Ranked)

### #1 IDEAL CHAMPION: [Name]
**Champion Score**: 54/60 | **Tier**: ATL (via `qualify_lead`)

**Profile**: [Name] | [Title] | [Department] | [Tenure] years | **Source**: HubSpot contactId [id] (or Apollo, if not yet in HubSpot)

**Scoring**: Role Relevance: 10/10 | Influence: 9/10 | Accessibility: 8/10
Change Agent: 9/10 | Personal Stake: 10/10 | Engagement: 8/10

**Why They're Ideal**:
- Pain: [Specific pain points their role experiences]
- Gain: [Career/team/personal impact when you win]
- Help: Can give insight into process, intro to EB, advocate internally

**Outreach Strategy**:
Best Approach: [Warm intro via X / Direct outreach]

Warm Intro Message:
> Hey [Mutual], I'm trying to connect with [Name] at [Company].
> We help [companies like theirs] with [problem]. Would you be
> comfortable making an intro?

Direct Outreach:
> Subject: [Company] - [Specific Problem]
> Hi [First Name], I noticed [observation] and thought you might
> be dealing with [problem]. We helped [similar company] reduce
> [metric] by [X%]. Worth a quick call?

**Personalization Hooks**:
- Recent Activity: [LinkedIn posts, job change, etc.]
- Shared Interests: [University, conference, group]
- Best Opening: "Hi [Name], saw you recently [activity]..."

### #2 STRONG POTENTIAL: [Name]
**Champion Score**: 47/60

[Profile, scoring breakdown, strengths, concerns, outreach approach]

### #3 GOOD BACKUP: [Name]
**Champion Score**: 42/60

[Similar structure, slightly shorter]

---

## Who NOT to Lead With

### [Name] - [Title]
**Why Not**: [Too senior / Wrong department / Blocker risk]
**But Consider**: [When they might be useful later]

---

## Multi-Threading Strategy

1. **Start With**: Champion #1 - Highest probability
2. **Parallel Outreach**: Champion #2 - Different department
3. **Economic Buyer Access**: Ask Champion #1 to introduce up
4. **Technical Validator**: Connect with [Technical Person]
5. **User Buy-In**: Get feedback from [End User Rep]

**Coverage Map**:
Economic Buyer (Decision): [Name, Title]
  → Champion (Advocate): [Champion #1]
    → Technical (Validate): [Technical Person]
      → Users (Adopt): [User Team]

---

## Account Mapping (DMU)

| Person | Role | Title | Champion Score | Tier (qualify_lead) | Influence | Status |
|--------|------|-------|---------------|---------------------|-----------|--------|
| [Name] | Champion | [Title] | 54/60 | ATL | High | Not contacted |
| [Name] | Economic Buyer | [Title] | N/A | ATL | Final | Via Champion |
| [Name] | Technical Buyer | [Title] | 35/60 | GRAY | Veto | Should engage |
| [Name] | End User | [Title] | 28/60 | BTL | Feedback | Include in demo |

---

## Champion Development Plan

### Phase 1: Initial Contact (Week 1)
- [ ] Secure warm intro or send personalized outreach
- [ ] Schedule discovery call
**Success**: Meeting scheduled

### Phase 2: Discovery & Qualification (Week 1-2)
- [ ] Run discovery call, validate pain
- [ ] Assess influence and willingness
- [ ] Get them to open up about process and players
**Success**: They articulate pain clearly and agree to next step

### Phase 3: Value Demonstration (Week 2-3)
- [ ] Tailored demo focused on their pain points
- [ ] Share case study, calculate ROI
**Success**: They say "this would really help us"

### Phase 4: Champion Activation (Week 3-4)
- [ ] Ask: "Would you be comfortable introducing me to [decision maker]?"
- [ ] Provide ammo to sell internally (ROI calc, one-pager)
**Success**: They introduce you to economic buyer

### Phase 5: Deal Progression (Ongoing)
- [ ] Regular check-ins, coaching on internal process
- [ ] Get input on proposal, have them socialize internally
**Success**: Deal moves forward with their help
```

## Stage 3: Stage Outreach as Gmail Drafts

Per CLAUDE.md's draft-first workflow, outreach templates are not terminal text — stage them.

**MCP Tool:** `mcp__claude_ai_Gmail__create_draft` (send-from `tkipper@epiphan.com`)

For the top 1-2 ranked candidates (ATL or GRAY only — never BTL/junk/suppressed), fill the
Warm Intro or Direct Outreach template with the candidate's real name/title/company and create
a Gmail draft rather than leaving it as inline text. Note the draft id/link in the candidate
card. If `create_draft` is unavailable, degrade to inline text and mark the run `partial`.

## Discovery Questions

**For Discovery Calls**:
1. "Walk me through how [process] works today at [Company]"
2. "What's working well? What's frustrating?"
3. "If you could wave a magic wand, what would you fix?"
4. "Who else is impacted by [problem]?"
5. "What have you tried? Why didn't it work?"

**For Champion Qualification**:
1. "Is this problem on your roadmap to solve?"
2. "How did buying decisions work in the past?"
3. "Who typically gets involved?"
4. "What would success look like for you personally?"
5. "Would you be comfortable introducing me to [economic buyer]?"

## Warning Signs (Not Actually a Champion)

- **Too Agreeable**: Says yes to everything but never takes action
- **Can't Get You to Others**: Always has excuse why you can't meet boss
- **Doesn't Know Process**: Can't describe how buying decisions get made
- **Not Actually Affected**: Talks about problem in abstract, no personal examples
- **No Skin in Game**: No personal KPIs tied to the problem

**Action**: Keep them in loop but find the REAL champion who has pain.

## Pro Tips

**Finding Champions**: Look for recent hires (want quick wins), promotions (want to prove themselves), pain posters (share challenges on LinkedIn), change agents (adopt new tools), event speakers (accessible).

**Building Relationships**: Make them look good internally, arm them with talking points and ROI, coach them on selling you internally, don't put them in awkward political positions.

**Best Practices**:
1. Lead with `power_level = atl` per `qualify_lead` (too junior = no power, too senior = too busy); GRAY needs Tim's manual ok; never lead with BTL
2. Multi-thread to reduce single point of failure
3. Qualify early with validation questions
4. Give value before asking for introductions
5. Document champion interactions in CRM — once outreach begins, log it via `mcp__claude_ai_Epiphan_Ai__hubspot_create_contact_note` on the champion's contact record rather than leaving it as a manual to-do

## Failure Handling & Outcome Logging

Follow `skill-audit/specs/self-healing-template.md` for the failure ladder (retry → degrade →
alert → halt) and the three-way status definition (success/partial/error — always name the
failing stage for partial/error). The Stage 2 "no-champion-found" case is a defined partial/error
outcome, not silent: if HubSpot/Apollo return candidates but none clear the `qualify_lead` gate,
status is `partial` with `error: "no_champion_above_threshold"`; if Stage 1 returns zero
candidates at all, status is `error`. Distinguish either from a tool failure (HubSpot/Apollo/
qualify_lead unreachable — name the failing stage).

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-champion-identifier.json`:
```json
{"ts":"[UTC ISO8601]","skill":"champion-identifier","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"profiles_analyzed":[n],"champions_identified":[n],"atl_count":[n from qualify_lead power_level==atl, not self-scored],"confidence_high":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced (including the
no-champion-found degrade path above). Use "error" only if no output was generated.

</workflow>

<dependencies>
## MCP tools
- `mcp__claude_ai_Epiphan_Ai__hubspot_search_contacts` — real candidate sourcing (Stage 1)
- `mcp__claude_ai_Apollo_io__apollo_contacts_search` — org-chart gap-fill when HubSpot coverage is thin (Stage 1)
- `qualify_lead` — single ATL/BTL/gray/junk + suppression gate (Stage 2)
- `mcp__claude_ai_Gmail__create_draft` — outreach draft staging for top 1-2 candidates (Stage 3)
- `mcp__claude_ai_Epiphan_Ai__hubspot_create_contact_note` — optional CRM logging once outreach begins

## Sibling skills referenced (overlap — flag only, no removal)
- `contact-hunter-skill` — use for a single named-person point-lookup instead of a multi-candidate champion sweep
- `linkedin-sales-navigator-alt-skill` — LinkedIn-side prospecting; complementary, not a replacement for the HubSpot/Apollo/qualify_lead grounding here
- `meddic-call-prep-auto-skill` — Economic Buyer identification for a specific call; reuse its ATL/BTL validation logic where it overlaps with Stage 2
</dependencies>

## Guardrails
- Every champion candidate must trace back to a `hubspot_search_contacts` or `apollo_contacts_search` result — never a fabricated name, title, or score.
- Never hand-roll ATL/BTL/Golden-Rules logic inline — `qualify_lead` is the single gate (`skill-audit/specs/suppression-spec.md`).
- Never lead with or draft outreach to a BTL, junk, or suppressed contact; GRAY requires Tim's manual ok.
- If zero candidates clear the `qualify_lead` gate, do not force a ranking — use the no-champion degrade path.

## Skill metadata
**Version:** 1.0.1 · **Author:** Tim Kipper · **Status:** Active · **Tier:** P2 (BDR Enablement)
