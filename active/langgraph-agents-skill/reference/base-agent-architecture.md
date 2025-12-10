# Base Agent Architecture

**Level**: 3 (Deep Dive)
**Load When**: User needs detailed agent configuration patterns

## Multi-Provider Setup

### Provider Enumeration

```python
from enum import Enum
from typing import Literal
from dataclasses import dataclass

class ProviderType(str, Enum):
    """Supported LLM providers - NO OPENAI"""
    ANTHROPIC = "anthropic"
    GROQ = "groq"
    CEREBRAS = "cerebras"
    DEEPSEEK = "deepseek"
    OLLAMA = "ollama"
    AUTO = "auto"  # Intelligent provider selection

class OptimizationTarget(str, Enum):
    """What to optimize for in agent execution"""
    COST = "cost"           # Use cheaper models (Groq, Cerebras)
    SPEED = "speed"         # Ultra-fast inference (Groq, Cerebras)
    QUALITY = "quality"     # Best reasoning (Claude Sonnet/Opus)
```

### Provider Selection Strategy

```python
def select_provider(task_type: str, optimize_for: OptimizationTarget) -> ProviderType:
    """Intelligent provider selection based on task requirements"""

    if optimize_for == OptimizationTarget.QUALITY:
        return ProviderType.ANTHROPIC  # Claude for complex reasoning

    if optimize_for == OptimizationTarget.SPEED:
        return ProviderType.CEREBRAS  # Fastest inference

    # COST optimization by task type
    if task_type in ["classification", "extraction", "routing"]:
        return ProviderType.GROQ  # Fast + cheap for simple tasks

    if task_type in ["analysis", "research", "synthesis"]:
        return ProviderType.ANTHROPIC  # Quality for complex tasks

    return ProviderType.GROQ  # Default to cost-effective
```

## Agent Configuration

### Core Configuration Dataclass

```python
@dataclass
class AgentConfig:
    """Base configuration for all agents"""
    name: str
    provider: ProviderType = ProviderType.AUTO
    optimize_for: OptimizationTarget = OptimizationTarget.COST
    use_cache: bool = True
    enable_transfers: bool = True
    grounding_strategy: Literal["strict", "moderate", "permissive"] = "strict"
    temperature: float = 0.7
    max_tokens: int = 4096
    timeout: int = 30  # seconds
```

### Grounding Strategies

- **strict**: Agent must cite sources, no hallucinations tolerated
- **moderate**: Balance creativity and accuracy (default for most tasks)
- **permissive**: Creative freedom, minimal grounding constraints

## Base Agent Factory

### Reusable Agent Template

```python
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langchain_community.chat_models import ChatOllama

def create_agent(config: AgentConfig, tools: list = None):
    """Factory pattern for creating configured agents"""

    # Select provider
    provider = config.provider
    if provider == ProviderType.AUTO:
        provider = select_provider(config.name, config.optimize_for)

    # Initialize LLM based on provider (NO OPENAI)
    if provider == ProviderType.ANTHROPIC:
        llm = ChatAnthropic(
            model="claude-sonnet-4-5-20250929",
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            timeout=config.timeout
        )
    elif provider == ProviderType.GROQ:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=config.temperature,
            max_tokens=config.max_tokens
        )
    elif provider == ProviderType.OLLAMA:
        llm = ChatOllama(
            model="llama3.2",
            temperature=config.temperature
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    # Bind tools if provided
    if tools and config.enable_transfers:
        llm = llm.bind_tools(tools)

    return llm
```

## Error Handling Patterns

### Retry with Fallback Providers

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def invoke_with_fallback(config: AgentConfig, messages: list):
    """Retry with automatic provider fallback"""

    providers = [config.provider, ProviderType.GROQ, ProviderType.ANTHROPIC]

    for provider in providers:
        try:
            config.provider = provider
            agent = create_agent(config)
            return agent.invoke(messages)
        except Exception as e:
            print(f"Provider {provider} failed: {e}")
            continue

    raise RuntimeError("All providers failed")
```

### Graceful Degradation

```python
def safe_invoke(agent, state: dict, fallback_response: str = None):
    """Invoke agent with graceful error handling"""

    try:
        response = agent.invoke(state["messages"])
        return {"messages": [response]}
    except TimeoutError:
        return {"messages": [fallback_response or "Request timed out, retrying..."]}
    except Exception as e:
        return {"messages": [f"Error: {str(e)}. Using fallback."]}
```

## State Management Integration

```python
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """Base state schema for all agents"""
    messages: Annotated[list, add_messages]
    context: dict  # Shared context between agents
    metadata: dict  # Tracking, logging, analytics
```

---

**Next Steps**: See `multi-agent-orchestration.md` for agent coordination patterns.
