---
name: champion-identifier-skill
description: Analyze LinkedIn profiles in target accounts to identify potential internal champions. Evaluates role, career path, mutual connections, interests, and suggests personalization approach. Use when you need to find who will champion your solution internally.
---

# Champion Identifier

<objective>
Analyze target accounts to identify the individuals most likely to become internal champions who will advocate for your solution. Scores candidates on role relevance, influence, accessibility, change-agent traits, personal stake, and engagement potential, then provides ranked recommendations with outreach strategies and multi-threading plans.
</objective>

<quick_start>
**Trigger:** "Find potential champions at [Company]" or "Who should I connect with at [Company] to champion our tool?"
**Input:** Target company name, your solution/product, any existing contacts
**Output:** Ranked champion candidates with scores (0-60), outreach templates, org chart, and multi-threading strategy
</quick_start>

<success_criteria>
- [ ] Company context analyzed (stage, news, pain points, decision style)
- [ ] 3-4 champion candidates identified and scored on 6 dimensions
- [ ] Each candidate has outreach strategy (warm intro or direct)
- [ ] Multi-threading plan with coverage map provided
- [ ] Warning signs and red flags documented
- [ ] Champion development plan with phased actions included
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

## Scoring Framework

**Scoring Dimensions** (0-10 each):
1. **Role Relevance** - How directly does their role relate to your solution?
2. **Influence Level** - Can they affect the buying decision?
3. **Accessibility** - Can you reach them? Warm intro possible?
4. **Change Agent** - Track record of adopting new solutions?
5. **Personal Stake** - Do they personally gain if you win?
6. **Engagement Potential** - Likely to respond to outreach?

**Total Champion Score**: 0-60 points
- 50-60: Ideal champion candidate
- 40-49: Strong potential champion
- 30-39: Possible champion with work
- Below 30: Not likely to champion

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
**Champion Score**: 54/60

**Profile**: [Name] | [Title] | [Department] | [Tenure] years

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

| Person | Role | Title | Champion Score | Influence | Status |
|--------|------|-------|---------------|-----------|--------|
| [Name] | Champion | [Title] | 54/60 | High | Not contacted |
| [Name] | Economic Buyer | [Title] | N/A | Final | Via Champion |
| [Name] | Technical Buyer | [Title] | 35/60 | Veto | Should engage |
| [Name] | End User | [Title] | 28/60 | Feedback | Include in demo |

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
1. Start at Director/VP level (too junior = no power, too senior = too busy)
2. Multi-thread to reduce single point of failure
3. Qualify early with validation questions
4. Give value before asking for introductions
5. Document champion interactions in CRM

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-champion-identifier.json`:
```json
{"ts":"[UTC ISO8601]","skill":"champion-identifier","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"profiles_analyzed":[n],"champions_identified":[n],"atl_count":[n],"confidence_high":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated.

</workflow>
