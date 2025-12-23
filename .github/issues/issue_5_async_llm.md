## 🎯 Problem

LLM calls are sequential, causing massive slowdown with multiple agents.

**Current Bottleneck:**

```
Agent 1: Think (500ms) → Wait
Agent 2: Think (500ms) → Wait
Agent 3: Think (500ms) → Wait
...
Total: 10 agents × 500ms = 5000ms per tick ❌
```

**Target:**

```
All agents: Think in parallel (500ms total) ✅
```

## ✅ Solution

Use Python `asyncio` to batch all LLM calls in parallel.

**Architecture:**

```python
async def think_all():
    tasks = [agent1.think(), agent2.think(), ...]
    results = await asyncio.gather(*tasks)  # Parallel!
```

## 🔧 Implementation

**File:** `neon_gemini_service.py`

```python
import asyncio
import google.generativeai as genai

# Convert sync to async
async def get_gemini_decision_async(agent_name, traits, goal, position, memories):
    """Async version of get_gemini_decision"""

    prompt = build_prompt(agent_name, traits, goal, position, memories)

    # Use async Gemini client
    model = genai.GenerativeModel(config.GEMINI_MODEL)

    # Wrap sync call in executor for true async
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,  # Default executor
        lambda: model.generate_content(
            prompt,
            generation_config={
                "temperature": config.GEMINI_TEMPERATURE,
                "response_mime_type": "application/json"
            }
        )
    )

    return json.loads(response.text)

async def batch_get_decisions(agents: List[AgentSnapshot]):
    """Process all agents in parallel"""

    tasks = []
    for agent in agents:
        memories = [m.content for m in agent.memories]
        task = get_gemini_decision_async(
            agent.name,
            agent.traits,
            agent.goal,
            (agent.x, agent.y),
            memories
        )
        tasks.append(task)

    # Wait for all to complete (parallel RTT)
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Handle errors
    decisions = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            # Fallback to mock
            decisions.append(mock_brain.get_mock_decision(...))
        else:
            decisions.append(result)

    return decisions
```

**File:** `neon_simulation.py`

```python
import asyncio

def process_agent_cognition_batch(agents: List[AgentSnapshot], use_mock: bool):
    """Batch version with async LLM"""

    # Filter agents needing deep thought
    thinking_agents = [
        a for a in agents
        if a.ticks_until_next_think <= 0
    ]

    if not thinking_agents or use_mock:
        # Fallback to sync mock
        for agent in thinking_agents:
            process_agent_cognition(agent, use_mock=True)
        return

    # Async batch call
    loop = asyncio.get_event_loop()
    decisions = loop.run_until_complete(
        batch_get_decisions(thinking_agents)
    )

    # Apply decisions
    for agent, decision in zip(thinking_agents, decisions):
        agent.current_thought = decision['thought']
        agent.current_plan = decision['plan']
        agent.cached_direction = decision['action']
        agent.ticks_until_next_think = config.THINK_INTERVAL
```

## ✔️ Acceptance Criteria

- [ ] **10 agents:** Think time < 600ms (vs 5000ms before)
- [ ] **Error handling:** Individual failures don't block others
- [ ] **Rate limits:** Gemini quotas respected (max 60 RPM)
- [ ] **Fallback:** Works with mock mode
- [ ] **Performance:** 8-10x speedup measured

## 📊 Testing

```python
import asyncio
import time

async def test_batch_speedup():
    agents = create_test_agents(10)

    # Sequential (old way)
    start = time.time()
    for agent in agents:
        await get_gemini_decision_async(...)  # 500ms each
    sequential_time = time.time() - start  # ~5000ms

    # Parallel (new way)
    start = time.time()
    results = await batch_get_decisions(agents)  # All at once
    parallel_time = time.time() - start  # ~500ms

    assert parallel_time < sequential_time * 0.2  # 5x+ faster
    assert len(results) == 10
```

## ⚠️ Known Issues

- Gemini rate limits: 60 requests/minute
  - Solution: Add rate limiter (10 agents = OK, 100 = throttle)
- Network errors: One failure can be noisy
  - Solution: `return_exceptions=True` + individual fallback

## 📚 References

- [Python asyncio](https://docs.python.org/3/library/asyncio.html)
- [Gemini Rate Limits](https://ai.google.dev/gemini-api/docs/quota)

## ⏱️ Estimate

**3-4 hours**

## 🏷️ Labels

`performance`, `gemini`, `priority:medium`, `async`
