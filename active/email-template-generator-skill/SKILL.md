---
name: email-template-generator-skill
description: Generate professional email templates for various business scenarios including sales outreach, customer support, internal communications, follow-ups, and apologies. Creates personalized, tone-appropriate templates with subject lines and formatting. Use when users need to write business emails, cold outreach, or professional communications.
---

# Email Template Generator

<objective>
Generate professional, tone-appropriate email templates for any business scenario including sales outreach, customer support, follow-ups, apologies, meeting requests, and internal communications. Produces 3 length variations (short/standard/detailed) with subject lines, personalization tokens, A/B test suggestions, and timing recommendations.
</objective>

<quick_start>
**Trigger:** "Write a cold email for [scenario]" or "Create a [type] email template"
**Input:** Email type, recipient/audience, purpose, desired tone, specific details to include
**Output:** 3 template variations (short, standard, detailed) with subject lines, personalization tokens, and optimization tips
</quick_start>

<success_criteria>
- [ ] Email type and audience identified
- [ ] 3 variations provided (short/mobile, standard, detailed)
- [ ] Each has clear subject line and single CTA
- [ ] Personalization tokens marked with [PLACEHOLDERS]
- [ ] A/B test suggestions for subject lines included
- [ ] Timing and follow-up cadence recommended
- [ ] Under 200 words for cold outreach templates
</success_criteria>

<workflow>

## Instructions

When a user requests an email template or needs help writing business emails:

1. **Identify Email Type**:
   - Sales/Cold outreach
   - Customer support response
   - Follow-up email
   - Apology/service recovery
   - Internal team communication
   - Meeting request
   - Thank you note
   - Rejection/decline

2. **Gather Context**:
   - What is the purpose of this email?
   - Who is the recipient (role, relationship)?
   - What action do you want them to take?
   - What tone is appropriate (formal, casual, friendly, apologetic)?
   - Any specific details or information to include?

3. **Generate Template** with:
   - **Subject Line**: Clear, compelling, action-oriented
   - **Opening**: Personalized greeting and context
   - **Body**: Main message broken into scannable paragraphs
   - **Call-to-Action**: Clear next step
   - **Closing**: Professional sign-off
   - **Variables**: [PLACEHOLDERS] for personalization

4. **Provide 3 Variations**:
   - **Short version**: 3-4 sentences, mobile-friendly
   - **Standard version**: 2-3 paragraphs, balanced
   - **Detailed version**: Comprehensive with extra context

5. **Include Best Practices**:
   - Subject line tips (A/B test suggestions)
   - Personalization tokens to use
   - Timing recommendations
   - Follow-up cadence
   - Common mistakes to avoid

6. **Format Output**:
   ```
   📧 EMAIL TEMPLATE: [Type]

   🎯 PURPOSE: [Goal]
   👤 AUDIENCE: [Recipient type]

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   VERSION 1: SHORT (Mobile-Friendly)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Subject: [Subject line]

   [Email content]

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   VERSION 2: STANDARD (Recommended)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Subject: [Subject line]

   [Email content]

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   VERSION 3: DETAILED (Comprehensive)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Subject: [Subject line]

   [Email content]

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   💡 OPTIMIZATION TIPS
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   ✅ Subject Line:
      • [Tip 1]
      • [Tip 2]

   ✅ Personalization:
      • [Token 1]
      • [Token 2]

   ✅ Timing:
      • Best send time: [Time]
      • Follow-up: [Cadence]

   ✅ A/B Testing:
      • Test subject lines: [Option A] vs [Option B]

   ⚠️ Common Mistakes:
      • [Mistake 1]
      • [Mistake 2]
   ```

7. **Special Scenarios**:
   - **Cold outreach**: Focus on value proposition, social proof
   - **Apology emails**: Acknowledge issue, take responsibility, offer solution
   - **Follow-ups**: Reference previous conversation, add new value
   - **Sales**: Problem → Solution → Proof → CTA structure

## Example Triggers

- "Write a cold email for B2B SaaS sales"
- "Generate a customer apology email template"
- "Create a meeting request email"
- "Help me write a follow-up email after a sales call"
- "Professional email to decline a proposal"

## Output Quality

Ensure all templates:
- Have clear, actionable subject lines
- Use conversational but professional tone
- Include specific personalization opportunities
- Have one clear call-to-action
- Are mobile-friendly (short paragraphs, scannable)
- Follow email best practices (under 200 words for cold outreach)
- Avoid spam trigger words
- Include unsubscribe for cold outreach

Generate effective, conversion-optimized email templates that users can immediately customize and send.

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-email-template-generator.json`:
```json
{"ts":"[UTC ISO8601]","skill":"email-template-generator","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"templates_generated":[n],"email_types":[n],"personalization_tokens":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated.

</workflow>
