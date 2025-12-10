# Context Engineering for LangGraph Agents

Advanced patterns for memory persistence, context management, and state optimization in multi-agent workflows.

## Memory Persistence Patterns

### Importance-Based Retention

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List

@dataclass
class MemoryEntry:
    """Memory with importance scoring for selective retention."""
    key: str
    content: Dict[str, Any]
    importance_score: float = 0.5  # 0.0-1.0
    access_count: int = 0
    last_accessed: datetime = field(default_factory=datetime.now)

    def update_importance(self, agent_feedback: float):
        """Adjust importance based on agent usage."""
        self.access_count += 1
        self.importance_score = (
            0.7 * self.importance_score + 0.3 * agent_feedback
        )

class MemoryManager:
    """TTL-aware memory with automatic compaction."""

    def __init__(self, max_entries: int = 100):
        self.memories: Dict[str, MemoryEntry] = {}
        self.max_entries = max_entries

    def store(self, key: str, content: Dict[str, Any], importance: float = 0.5):
        """Store memory with importance score."""
        self.memories[key] = MemoryEntry(key, content, importance)
        self._compact_if_needed()

    def _compact_if_needed(self):
        """Remove low-importance memories when limit reached."""
        if len(self.memories) > self.max_entries:
            # Sort by importance × recency
            sorted_keys = sorted(
                self.memories.keys(),
                key=lambda k: (
                    self.memories[k].importance_score *
                    (1 / max(self.memories[k].access_count, 1))
                )
            )
            # Remove bottom 20%
            for key in sorted_keys[:self.max_entries // 5]:
                del self.memories[key]
```

### Redis Checkpointer Integration

```python
from langgraph.checkpoint.redis import RedisSaver
import redis

# Production-grade persistence
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

checkpointer = RedisSaver(redis_client)

# Thread-specific memory with TTL
def save_conversation_state(thread_id: str, state: Dict, ttl: int = 3600):
    """Save state with automatic expiry."""
    redis_client.setex(
        f"conversation:{thread_id}",
        ttl,
        json.dumps(state)
    )
```

## Context Compaction Strategies

### Summarization Pipeline

```python
from anthropic import Anthropic

client = Anthropic()

def compact_conversation_history(messages: List[Dict], max_tokens: int = 1000):
    """Summarize conversation when context limit approached."""

    # Preserve first and last N messages
    critical_start = messages[:2]
    critical_end = messages[-3:]
    middle = messages[2:-3]

    if len(middle) == 0:
        return messages

    # Summarize middle section
    summary_prompt = f"""Summarize this conversation segment concisely:

{middle}

Focus on: decisions made, key data points, unresolved issues."""

    summary = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[{"role": "user", "content": summary_prompt}]
    )

    return critical_start + [
        {"role": "system", "content": f"[Summary]: {summary.content[0].text}"}
    ] + critical_end
```

### Token Budget Management

```python
def estimate_tokens(text: str) -> int:
    """Rough token estimation (4 chars ≈ 1 token)."""
    return len(text) // 4

def trim_to_budget(state: Dict, max_tokens: int = 8000) -> Dict:
    """Ensure state fits within token budget."""
    current = estimate_tokens(str(state))

    if current <= max_tokens:
        return state

    # Priority: current_task > pending > metadata > completed
    trimmed = {
        "current_task": state["current_task"],
        "pending": state["pending"][:5],  # Keep next 5 tasks
        "completed": state["completed"][-3:]  # Keep last 3
    }

    return trimmed
```

## Just-in-Time Context Loading

### Task-Specific Templates

```python
CONTEXT_TEMPLATES = {
    "lead_qualification": """
You are qualifying leads. Focus on:
- Company size and industry
- Budget signals
- Decision maker identification
""",
    "data_enrichment": """
You are enriching contact data. Prioritize:
- Email validation
- LinkedIn profile matching
- Company domain verification
""",
    "outreach_sequence": """
You are crafting outreach sequences. Consider:
- Personalization data available
- Engagement history
- Timezone and send time optimization
"""
}

def load_context_for_node(node_name: str, base_state: Dict) -> str:
    """Inject only relevant context for current node."""
    template = CONTEXT_TEMPLATES.get(node_name, "")

    # Add minimal state data
    context = f"{template}\n\nCurrent data: {base_state.get('current_record', {})}"
    return context
```

### Lazy Loading Pattern

```python
class ContextLoader:
    """Load context only when node executes."""

    def __init__(self):
        self._cache = {}

    def get_context(self, node: str, state: Dict) -> str:
        """Load and cache context for node."""
        cache_key = f"{node}:{state.get('record_id')}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        # Expensive context loading
        context = self._load_from_source(node, state)
        self._cache[cache_key] = context

        return context

    def _load_from_source(self, node: str, state: Dict) -> str:
        """Simulate loading from DB/API."""
        # In production: query vector DB, fetch from API, etc.
        return CONTEXT_TEMPLATES.get(node, "")
```

## Sub-Agent Context Isolation

### State Scoping

```python
def create_sub_agent_context(parent_state: Dict, scope: List[str]) -> Dict:
    """Create isolated state for sub-agent with only needed fields."""
    return {key: parent_state[key] for key in scope if key in parent_state}

# Example: Research sub-agent only needs query and budget
research_context = create_sub_agent_context(
    parent_state,
    scope=["search_query", "max_results", "research_depth"]
)

# Writer sub-agent gets research output but not search details
writer_context = create_sub_agent_context(
    parent_state,
    scope=["research_findings", "tone", "target_audience"]
)
```

### Cross-Agent Communication

```python
from typing_extensions import TypedDict

class SharedMemory(TypedDict):
    """Explicitly defined shared state."""
    project_id: str
    current_phase: str
    critical_findings: List[str]

class AgentPrivateState(TypedDict):
    """Agent-specific state not shared."""
    internal_reasoning: str
    api_credentials: Dict
    retry_count: int

def merge_agent_results(shared: SharedMemory, private: AgentPrivateState) -> Dict:
    """Combine shared and private state safely."""
    return {
        **shared,
        "agent_metadata": {
            "retry_count": private["retry_count"]
        }
        # Private credentials never exposed
    }
```

## Best Practices

1. **Memory Retention**: Use importance scoring + access patterns, not just recency
2. **Token Budgets**: Always reserve 20% for system prompts and output
3. **Context Loading**: Load just-in-time per node, not all upfront
4. **Sub-Agent Isolation**: Share only required fields, never entire state
5. **Compaction Triggers**: Compact at 70% capacity, not 100%
6. **TTL Strategy**: Short (1h) for sessions, long (24h) for project state

## Production Checklist

- [ ] Memory has expiration/compaction strategy
- [ ] Context fits within model's window (100k for Claude)
- [ ] Sub-agents can't access parent's sensitive data
- [ ] State is JSON-serializable for checkpointing
- [ ] Critical information never gets compacted away
