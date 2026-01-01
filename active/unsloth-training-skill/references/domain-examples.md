# Domain-Specific Reward Function Examples

Reference implementations for different application domains.

---

## Voice AI Application

Voice responses need to be concise, natural, and avoid text-oriented formatting.

### Brevity Reward

```python
def brevity_reward(completions, **kwargs):
    """
    Voice responses should be concise (<50 words = +0.5)
    Penalize verbose responses that don't work well spoken.
    """
    rewards = []
    for completion in completions:
        word_count = len(completion.split())
        if word_count <= 30:
            rewards.append(0.5)   # Ideal for voice
        elif word_count <= 50:
            rewards.append(0.3)   # Acceptable
        elif word_count <= 80:
            rewards.append(0.0)   # Too long
        else:
            rewards.append(-0.3)  # Way too long
    return rewards
```

### Speakable Content Reward

```python
def speakable_reward(completions, **kwargs):
    """
    Penalize markdown, bullets, URLs that sound bad spoken.
    Each violation is -0.2.
    """
    bad_patterns = [
        # Markdown formatting
        "**", "__", "- ", "* ", "1.", "2.", "3.",
        "```", "`", "###", "##", "#",
        # URLs and technical references
        "http", "www.", ".com", ".io",
        # Abbreviations that sound awkward
        "e.g.", "i.e.", "etc.", "vs.", "w/",
        # Lists that are hard to follow aurally
        ":\n-", ":\n*", ":\n1.",
    ]

    rewards = []
    for completion in completions:
        violations = sum(1 for p in bad_patterns if p in completion)
        # Cap penalty at -1.0
        rewards.append(max(-0.2 * violations, -1.0))
    return rewards
```

### Natural Speech Patterns

```python
def natural_speech_reward(completions, **kwargs):
    """
    Reward conversational patterns, penalize robotic responses.
    """
    # Conversational starters (good for voice)
    conversational = [
        "sure", "absolutely", "great question",
        "let me", "i'd say", "here's the thing",
    ]

    # Robotic patterns (bad for voice)
    robotic = [
        "as an ai", "i cannot", "i don't have",
        "it is important to note", "it should be noted",
        "in conclusion", "to summarize",
    ]

    rewards = []
    for completion in completions:
        lower = completion.lower()

        # Start with neutral
        reward = 0.0

        # Reward conversational patterns
        if any(phrase in lower[:50] for phrase in conversational):
            reward += 0.2

        # Penalize robotic patterns
        robotic_count = sum(1 for phrase in robotic if phrase in lower)
        reward -= 0.15 * robotic_count

        rewards.append(max(min(reward, 0.4), -0.6))

    return rewards
```

### No Filler Words

```python
def no_filler_reward(completions, **kwargs):
    """
    Penalize common filler words that waste audio time.
    """
    fillers = [
        "basically", "actually", "essentially",
        "to be honest", "you know", "kind of",
        "sort of", "pretty much", "in terms of",
    ]

    rewards = []
    for completion in completions:
        lower = completion.lower()
        filler_count = sum(1 for f in fillers if f in lower)
        rewards.append(-0.1 * filler_count)
    return rewards
```

### Complete Voice AI Reward Stack

```python
# Recommended weights for Voice AI
voice_ai_rewards = [
    # Primary signals
    correctness_reward,        # +2.0 max - Core accuracy
    brevity_reward,            # +0.5 max - Conciseness

    # Quality signals
    speakable_reward,          # -1.0 max penalty - Format compliance
    natural_speech_reward,     # +0.4/-0.6 - Conversational tone

    # Constraints
    no_filler_reward,          # Penalty only - Clean speech
]

# Total range: approximately -2.0 to +3.0
```

---

## Sales Agent Application

Sales agents need to qualify leads (BANT/MEDDIC), avoid premature commitments, and guide toward next steps.

### BANT Qualification Reward

```python
def qualification_reward(completions, **kwargs):
    """
    Reward BANT signals: Budget, Authority, Need, Timeline.
    +0.25 per signal category addressed.
    """
    signals = {
        "budget": [
            "budget", "cost", "price", "afford", "investment",
            "spending", "allocated", "financing",
        ],
        "authority": [
            "decision", "approve", "stakeholder", "sign off",
            "who else", "team involved", "leadership",
        ],
        "need": [
            "challenge", "problem", "pain point", "struggle",
            "frustrating", "issue", "difficulty", "goal",
        ],
        "timeline": [
            "when", "deadline", "timeline", "urgent",
            "priority", "by when", "timeframe",
        ],
    }

    rewards = []
    for completion in completions:
        lower = completion.lower()
        hits = sum(
            1 for category, keywords in signals.items()
            if any(kw in lower for kw in keywords)
        )
        rewards.append(0.25 * hits)  # Max +1.0 for all 4
    return rewards
```

### MEDDIC Qualification (Enterprise Sales)

```python
def meddic_reward(completions, **kwargs):
    """
    Reward MEDDIC methodology signals for enterprise sales.
    Metrics, Economic Buyer, Decision Criteria, Decision Process,
    Identify Pain, Champion.
    """
    meddic = {
        "metrics": [
            "measure", "kpi", "metric", "roi", "percentage",
            "improvement", "reduction", "increase",
        ],
        "economic_buyer": [
            "budget owner", "final decision", "approve spend",
            "cfo", "ceo", "vp of", "head of",
        ],
        "decision_criteria": [
            "requirements", "must have", "criteria",
            "evaluate", "compare", "looking for",
        ],
        "decision_process": [
            "process", "steps", "timeline", "approval",
            "committee", "review", "procurement",
        ],
        "pain": [
            "pain", "problem", "challenge", "frustration",
            "struggle", "costly", "inefficient",
        ],
        "champion": [
            "advocate", "support", "champion", "internal",
            "on your side", "push this through",
        ],
    }

    rewards = []
    for completion in completions:
        lower = completion.lower()
        hits = sum(
            1 for category, keywords in meddic.items()
            if any(kw in lower for kw in keywords)
        )
        # Scale to max +1.5 for covering most MEDDIC elements
        rewards.append(0.25 * hits)
    return rewards
```

### No Premature Price Commitment

```python
def no_price_commitment_reward(completions, **kwargs):
    """
    Penalize premature pricing before qualification.
    Sales reps should qualify before discussing specific pricing.
    """
    price_commits = [
        "the price is", "it costs", "that'll be",
        "pricing is", "we charge", "the cost is",
        "starting at $", "for $", "per month is",
        "annually it's", "subscription is",
    ]

    # Acceptable price discussion (framing, not commitment)
    acceptable = [
        "depends on", "varies based", "let me understand",
        "factors include", "can range", "need to know more",
    ]

    rewards = []
    for completion in completions:
        lower = completion.lower()

        # Check for hard price commitments
        has_commit = any(p in lower for p in price_commits)
        has_acceptable = any(a in lower for a in acceptable)

        if has_commit and not has_acceptable:
            rewards.append(-1.0)  # Heavy penalty
        else:
            rewards.append(0.0)

    return rewards
```

### Next Step Progression

```python
def next_step_reward(completions, **kwargs):
    """
    Reward clear calls to action and next step proposals.
    """
    next_steps = [
        "schedule", "set up a", "book a", "next step",
        "follow up", "send you", "share with you",
        "demo", "trial", "pilot", "meeting",
        "let's plan", "i'll send", "can we",
    ]

    weak_endings = [
        "let me know", "feel free", "reach out",
        "any questions", "hope this helps",
    ]

    rewards = []
    for completion in completions:
        lower = completion.lower()

        # Check for strong next steps
        has_next_step = any(ns in lower for ns in next_steps)
        has_weak = any(w in lower for w in weak_endings)

        if has_next_step and not has_weak:
            rewards.append(0.5)
        elif has_next_step:
            rewards.append(0.2)  # Has step but weak ending
        elif has_weak:
            rewards.append(-0.2)  # Weak ending only
        else:
            rewards.append(0.0)

    return rewards
```

### Complete Sales Agent Reward Stack

```python
# Recommended weights for Sales Agent
sales_agent_rewards = [
    # Primary signals
    correctness_reward,          # +2.0 max - Accurate info
    qualification_reward,        # +1.0 max - BANT coverage

    # Quality signals
    next_step_reward,            # +0.5 max - Clear CTA

    # Constraints
    no_price_commitment_reward,  # -1.0 penalty - No premature pricing
]

# For enterprise sales, swap in:
# meddic_reward instead of qualification_reward
```

---

## Customer Support Agent

Support agents need empathy, clear solutions, and escalation awareness.

### Empathy Acknowledgment

```python
def empathy_reward(completions, **kwargs):
    """
    Reward acknowledgment of customer frustration.
    """
    empathy_phrases = [
        "i understand", "i can see", "that's frustrating",
        "sorry to hear", "i appreciate", "thank you for",
        "makes sense", "completely understand",
    ]

    rewards = []
    for completion in completions:
        lower = completion.lower()
        # Check first 100 chars for empathy (should come early)
        early_text = lower[:100]
        has_empathy = any(p in early_text for p in empathy_phrases)
        rewards.append(0.3 if has_empathy else 0.0)
    return rewards
```

### Clear Solution Steps

```python
def solution_clarity_reward(completions, **kwargs):
    """
    Reward clear, actionable solution steps.
    """
    action_indicators = [
        "first,", "step 1", "to fix this", "you can",
        "try this", "here's how", "the solution",
        "1.", "2.", "3.",  # Numbered steps OK for support
    ]

    rewards = []
    for completion in completions:
        lower = completion.lower()
        has_actions = any(a in lower for a in action_indicators)
        rewards.append(0.4 if has_actions else 0.0)
    return rewards
```

---

## Code Assistant

Code assistants need accuracy, proper formatting, and explanations.

### Code Block Formatting

```python
def code_format_reward(completions, **kwargs):
    """
    Reward properly formatted code blocks.
    """
    rewards = []
    for completion in completions:
        has_code_block = "```" in completion
        # Check for language specification
        has_lang = any(
            f"```{lang}" in completion.lower()
            for lang in ["python", "javascript", "typescript", "bash", "sql"]
        )

        if has_code_block and has_lang:
            rewards.append(0.4)
        elif has_code_block:
            rewards.append(0.2)
        else:
            rewards.append(0.0)
    return rewards
```

### Code Explanation Present

```python
def explanation_reward(completions, **kwargs):
    """
    Reward code + explanation combinations.
    """
    explanation_markers = [
        "this code", "this function", "this will",
        "here's what", "the output", "returns",
        "explanation:", "note:", "this does",
    ]

    rewards = []
    for completion in completions:
        lower = completion.lower()
        has_code = "```" in completion
        has_explanation = any(m in lower for m in explanation_markers)

        if has_code and has_explanation:
            rewards.append(0.3)
        else:
            rewards.append(0.0)
    return rewards
```

---

## Integration Pattern

### Combining Domain Rewards with Core Rewards

```python
def build_reward_stack(domain="general"):
    """
    Build a reward function stack for a specific domain.
    """
    # Always include core rewards
    core_rewards = [
        correctness_reward,    # +2.0 - Primary signal
        format_reward,         # +0.5 - Structure compliance
    ]

    domain_rewards = {
        "voice_ai": [
            brevity_reward,
            speakable_reward,
            natural_speech_reward,
        ],
        "sales": [
            qualification_reward,
            next_step_reward,
            no_price_commitment_reward,
        ],
        "support": [
            empathy_reward,
            solution_clarity_reward,
        ],
        "code": [
            code_format_reward,
            explanation_reward,
        ],
        "general": [
            reasoning_length_reward,
            no_hedging_reward,
        ],
    }

    return core_rewards + domain_rewards.get(domain, domain_rewards["general"])
```
