"""
GRPO Reward Functions Library
=============================

Collection of reusable reward function patterns for different use cases.
Import and combine these for your specific training needs.

Usage:
    from reward_functions import (
        correctness_reward,
        format_reward,
        build_keyword_reward,
    )
    
    reward_funcs = [
        correctness_reward,
        format_reward,
        build_keyword_reward(["budget", "timeline"]),
    ]
"""

import re
from typing import Callable, Optional


# =============================================================================
# EXTRACTION HELPERS
# =============================================================================

def extract_xml_tag(text: str, tag: str) -> str:
    """Extract content between XML tags"""
    pattern = rf"<{tag}>(.*?)</{tag}>"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""


def extract_answer(text: str) -> str:
    """Standard answer extraction"""
    return extract_xml_tag(text, "answer")


def extract_reasoning(text: str) -> str:
    """Standard reasoning extraction"""
    return extract_xml_tag(text, "reasoning")


def extract_code_block(text: str, language: str = "") -> str:
    """Extract code from markdown code blocks"""
    pattern = rf"```{language}\s*(.*?)\s*```"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""


def normalize_number(text: str) -> Optional[float]:
    """Parse number from text, handling common formats"""
    if not text:
        return None
    cleaned = text.replace(",", "").replace("$", "").replace("%", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None


# =============================================================================
# CORRECTNESS REWARDS
# =============================================================================

def correctness_reward(completions, answer, **kwargs):
    """
    Binary correctness: +2.0 for exact match, 0.0 otherwise
    
    Use as primary learning signal. Highest weight.
    """
    rewards = []
    for completion, true_answer in zip(completions, answer):
        extracted = extract_answer(completion)
        pred_num = normalize_number(extracted)
        true_num = normalize_number(str(true_answer))
        
        if pred_num is not None and true_num is not None:
            reward = 2.0 if abs(pred_num - true_num) < 0.01 else 0.0
        else:
            reward = 2.0 if extracted.strip().lower() == str(true_answer).strip().lower() else 0.0
        
        rewards.append(reward)
    return rewards


def proximity_reward(completions, answer, **kwargs):
    """
    Gradient reward based on closeness to correct answer.
    Helps model learn direction even when wrong.
    
    Returns: 0.0 to 2.0 based on proximity
    """
    rewards = []
    for completion, true_answer in zip(completions, answer):
        extracted = extract_answer(completion)
        pred_num = normalize_number(extracted)
        true_num = normalize_number(str(true_answer))
        
        if pred_num is not None and true_num is not None:
            if abs(pred_num - true_num) < 0.01:
                reward = 2.0
            else:
                error_ratio = abs(pred_num - true_num) / max(abs(true_num), 1)
                reward = max(0.0, 2.0 * (1.0 - min(error_ratio, 1.0)))
        else:
            reward = 2.0 if extracted.strip().lower() == str(true_answer).strip().lower() else 0.0
        
        rewards.append(reward)
    return rewards


def partial_match_reward(completions, answer, **kwargs):
    """
    Partial credit for answers containing correct elements.
    Good for multi-part answers.
    """
    rewards = []
    for completion, true_answer in zip(completions, answer):
        extracted = extract_answer(completion).lower()
        true_parts = str(true_answer).lower().split()
        
        if not true_parts:
            rewards.append(0.0)
            continue
            
        matches = sum(1 for part in true_parts if part in extracted)
        reward = 2.0 * (matches / len(true_parts))
        rewards.append(reward)
    return rewards


# =============================================================================
# FORMAT REWARDS
# =============================================================================

def format_reward(completions, **kwargs):
    """
    XML format compliance: +0.5 for proper structure
    """
    rewards = []
    for completion in completions:
        has_reasoning = bool(re.search(r"<reasoning>.*?</reasoning>", completion, re.DOTALL))
        has_answer = bool(re.search(r"<answer>.*?</answer>", completion, re.DOTALL))
        
        if has_reasoning and has_answer:
            rewards.append(0.5)
        elif has_answer:
            rewards.append(0.2)
        else:
            rewards.append(0.0)
    return rewards


def strict_format_reward(completions, **kwargs):
    """
    Exact format match with regex: 1.0 or 0.0
    """
    pattern = (
        r"^<reasoning>\s*"
        r"([^<]*(?:<(?!/?reasoning>)[^<]*)*)"
        r"\s*</reasoning>\s*"
        r"<answer>\s*([\s\S]*?)\s*</answer>\s*$"
    )
    rewards = []
    for completion in completions:
        match = re.search(pattern, completion, re.DOTALL)
        rewards.append(1.0 if match else 0.0)
    return rewards


def xml_count_reward(completions, **kwargs):
    """
    Ensure exactly one of each required tag: +0.5 if valid
    """
    rewards = []
    for completion in completions:
        reasoning_count = len(re.findall(r"<reasoning>", completion))
        answer_count = len(re.findall(r"<answer>", completion))
        
        valid = (reasoning_count == 1 and answer_count == 1)
        rewards.append(0.5 if valid else 0.0)
    return rewards


def build_custom_format_reward(
    required_tags: list[str],
    reward_per_tag: float = 0.25
) -> Callable:
    """
    Factory: Create format reward for custom tag structure
    
    Example:
        reward = build_custom_format_reward(["thought", "action", "result"])
    """
    def custom_format_reward(completions, **kwargs):
        rewards = []
        for completion in completions:
            tag_count = 0
            for tag in required_tags:
                if re.search(rf"<{tag}>.*?</{tag}>", completion, re.DOTALL):
                    tag_count += 1
            rewards.append(reward_per_tag * tag_count)
        return rewards
    return custom_format_reward


# =============================================================================
# REASONING QUALITY REWARDS
# =============================================================================

def reasoning_length_reward(completions, min_words=20, max_words=200, **kwargs):
    """
    Reward substantive reasoning length: +0.3 if in range
    """
    rewards = []
    for completion in completions:
        reasoning = extract_reasoning(completion)
        word_count = len(reasoning.split()) if reasoning else 0
        
        if min_words <= word_count <= max_words:
            rewards.append(0.3)
        elif word_count > 0:
            rewards.append(0.1)
        else:
            rewards.append(0.0)
    return rewards


def step_count_reward(completions, min_steps=2, max_steps=10, **kwargs):
    """
    Reward explicit step-by-step reasoning
    """
    step_patterns = [
        r"step \d+",
        r"first[,:]",
        r"second[,:]",
        r"then[,:]",
        r"finally[,:]",
        r"\d+\.",
        r"•",
    ]
    
    rewards = []
    for completion in completions:
        reasoning = extract_reasoning(completion).lower()
        steps = sum(len(re.findall(p, reasoning)) for p in step_patterns)
        
        if min_steps <= steps <= max_steps:
            rewards.append(0.3)
        elif steps > 0:
            rewards.append(0.1)
        else:
            rewards.append(0.0)
    return rewards


def calculation_shown_reward(completions, **kwargs):
    """
    Reward showing mathematical work
    """
    math_patterns = [
        r"\d+\s*[\+\-\*\/]\s*\d+",  # Basic operations
        r"=\s*\d+",                   # Equals results
        r"\d+\s*×\s*\d+",            # Multiplication symbol
    ]
    
    rewards = []
    for completion in completions:
        reasoning = extract_reasoning(completion)
        has_math = any(re.search(p, reasoning) for p in math_patterns)
        rewards.append(0.3 if has_math else 0.0)
    return rewards


# =============================================================================
# CONSTRAINT/PENALTY REWARDS
# =============================================================================

def no_hedging_reward(completions, **kwargs):
    """
    Penalize uncertainty language: -0.3 if hedging
    """
    hedging = [
        "i think", "maybe", "perhaps", "possibly",
        "i'm not sure", "i believe", "it could be",
        "probably", "might be", "not certain"
    ]
    
    rewards = []
    for completion in completions:
        lower = completion.lower()
        has_hedging = any(phrase in lower for phrase in hedging)
        rewards.append(-0.3 if has_hedging else 0.0)
    return rewards


def no_apology_reward(completions, **kwargs):
    """
    Penalize unnecessary apologies: -0.2 if apologizing
    """
    apologies = [
        "i apologize", "sorry", "i'm sorry",
        "my apologies", "forgive me"
    ]
    
    rewards = []
    for completion in completions:
        lower = completion.lower()
        has_apology = any(phrase in lower for phrase in apologies)
        rewards.append(-0.2 if has_apology else 0.0)
    return rewards


def no_repetition_reward(completions, threshold=0.7, **kwargs):
    """
    Penalize repetitive text: -0.5 if too repetitive
    """
    rewards = []
    for completion in completions:
        sentences = [s.strip().lower() for s in completion.split('.') if s.strip()]
        if len(sentences) < 2:
            rewards.append(0.0)
            continue
        
        unique = set(sentences)
        ratio = len(unique) / len(sentences)
        rewards.append(0.0 if ratio >= threshold else -0.5)
    return rewards


def max_length_reward(completions, max_tokens=500, **kwargs):
    """
    Penalize overly long responses: -0.3 if exceeds limit
    """
    rewards = []
    for completion in completions:
        word_count = len(completion.split())
        rewards.append(-0.3 if word_count > max_tokens else 0.0)
    return rewards


def integer_answer_reward(completions, **kwargs):
    """
    Encourage integer answers (for math): +0.2 if integer
    """
    rewards = []
    for completion in completions:
        extracted = extract_answer(completion)
        num = normalize_number(extracted)
        if num is not None and num == int(num):
            rewards.append(0.2)
        else:
            rewards.append(0.0)
    return rewards


# =============================================================================
# DOMAIN-SPECIFIC REWARDS
# =============================================================================

def build_keyword_reward(
    keywords: list[str],
    reward_per_keyword: float = 0.2,
    max_reward: float = 1.0
) -> Callable:
    """
    Factory: Reward presence of specific keywords
    
    Example:
        qualification_reward = build_keyword_reward(
            ["budget", "timeline", "decision maker"],
            reward_per_keyword=0.25
        )
    """
    def keyword_reward(completions, **kwargs):
        rewards = []
        for completion in completions:
            lower = completion.lower()
            hits = sum(1 for kw in keywords if kw.lower() in lower)
            reward = min(hits * reward_per_keyword, max_reward)
            rewards.append(reward)
        return rewards
    return keyword_reward


def build_forbidden_phrases_reward(
    phrases: list[str],
    penalty: float = -0.5
) -> Callable:
    """
    Factory: Penalize forbidden phrases
    
    Example:
        no_price_reward = build_forbidden_phrases_reward(
            ["the price is", "it costs", "total is"],
            penalty=-1.0
        )
    """
    def forbidden_reward(completions, **kwargs):
        rewards = []
        for completion in completions:
            lower = completion.lower()
            has_forbidden = any(phrase.lower() in lower for phrase in phrases)
            rewards.append(penalty if has_forbidden else 0.0)
        return rewards
    return forbidden_reward


# Sales/GTM specific
def qualification_reward(completions, **kwargs):
    """Reward BANT qualification signals"""
    return build_keyword_reward(
        ["budget", "cost", "price", "afford",
         "decision", "approve", "authority",
         "need", "challenge", "problem",
         "timeline", "when", "deadline"],
        reward_per_keyword=0.15,
        max_reward=0.6
    )(completions, **kwargs)


def sales_compliance_reward(completions, **kwargs):
    """Penalize premature commitments"""
    forbidden = [
        "i guarantee", "i promise", "definitely",
        "the price is", "total cost is", "that'll be",
        "you should buy", "you need to buy"
    ]
    return build_forbidden_phrases_reward(
        forbidden, penalty=-0.5
    )(completions, **kwargs)


# Voice AI specific
def brevity_reward(completions, max_words=50, **kwargs):
    """
    Reward concise responses for voice: +0.5 if brief
    """
    rewards = []
    for completion in completions:
        word_count = len(completion.split())
        if word_count <= max_words:
            rewards.append(0.5)
        elif word_count <= max_words * 2:
            rewards.append(0.2)
        else:
            rewards.append(-0.3)
    return rewards


def speakable_reward(completions, **kwargs):
    """
    Penalize text-only patterns unsuitable for speech
    """
    bad_patterns = [
        "**", "- ", "* ", "1.", "2.", "3.",
        "```", "http", "www.",
        "e.g.", "i.e.", "etc.",
        "[", "]", "(see", "click"
    ]
    
    rewards = []
    for completion in completions:
        violations = sum(1 for p in bad_patterns if p in completion)
        rewards.append(-0.2 * violations)
    return rewards


# Code specific
def syntax_valid_reward(completions, **kwargs):
    """Reward syntactically valid Python code"""
    import ast
    
    rewards = []
    for completion in completions:
        code = extract_code_block(completion, "python")
        if not code:
            code = extract_answer(completion)
        
        try:
            ast.parse(code)
            rewards.append(1.0)
        except SyntaxError:
            rewards.append(0.0)
    return rewards


# =============================================================================
# COMPOSITE REWARD BUILDERS
# =============================================================================

def build_reward_suite(
    use_case: str = "reasoning"
) -> list[Callable]:
    """
    Get pre-configured reward function suites
    
    Args:
        use_case: "reasoning", "sales", "voice", "code"
    
    Returns:
        List of reward functions for the use case
    """
    
    base_rewards = [
        correctness_reward,
        format_reward,
    ]
    
    if use_case == "reasoning":
        return base_rewards + [
            reasoning_length_reward,
            step_count_reward,
            no_hedging_reward,
            integer_answer_reward,
        ]
    
    elif use_case == "sales":
        return base_rewards + [
            qualification_reward,
            sales_compliance_reward,
            no_apology_reward,
        ]
    
    elif use_case == "voice":
        return base_rewards + [
            brevity_reward,
            speakable_reward,
            no_hedging_reward,
        ]
    
    elif use_case == "code":
        return [
            syntax_valid_reward,
            format_reward,
            calculation_shown_reward,
        ]
    
    else:
        return base_rewards


# =============================================================================
# REWARD DEBUGGING
# =============================================================================

def test_reward_functions(
    reward_funcs: list[Callable],
    test_completion: str,
    test_answer: str = "42"
):
    """
    Debug utility to test reward functions
    
    Example:
        test_reward_functions(
            [correctness_reward, format_reward],
            "<reasoning>2+2=4</reasoning><answer>4</answer>",
            "4"
        )
    """
    print("="*60)
    print("REWARD FUNCTION TEST")
    print("="*60)
    print(f"\nCompletion: {test_completion[:100]}...")
    print(f"Answer: {test_answer}")
    print()
    
    total = 0.0
    for func in reward_funcs:
        result = func([test_completion], [test_answer])[0]
        total += result
        print(f"  {func.__name__}: {result:+.2f}")
    
    print("-"*40)
    print(f"  TOTAL: {total:+.2f}")
    print()


if __name__ == "__main__":
    # Test the reward functions
    test_completion = """<reasoning>
Let me solve this step by step.
Step 1: The problem asks for 6 * 7
Step 2: 6 * 7 = 42
Therefore, the answer is 42.
</reasoning>
<answer>42</answer>"""
    
    test_reward_functions(
        build_reward_suite("reasoning"),
        test_completion,
        "42"
    )
