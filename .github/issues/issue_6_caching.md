## 🎯 Problem

Streamlit re-renders static components every rerun, wasting CPU/time.

**Examples of Static Data:**

- Agent profile cards (name, traits, goal never change)
- Configuration panels
- Map grid background
- Styling/CSS injection

**Impact:** 30-40% of render time spent on unchanging elements

## ✅ Solution

Use `@st.cache_data` to cache expensive computations and rendering.

**Key Insight:**
Cache anything that depends only on immutable inputs!

## 🔧 Implementation

**File:** `neon_app.py`

```python
import streamlit as st
import hashlib

@st.cache_data
def render_agent_profile_card(name: str, traits: str, goal: str):
    """Cache profile cards (never change during session)"""

    html = f"""
    <div class="agent-card">
        <h3>🧙 {name}</h3>
        <p><strong>Traits:</strong> {traits}</p>
        <p><strong>Goal:</strong> {goal}</p>
    </div>
    """
    return html

@st.cache_data
def render_map_grid(size: int, cell_size: int):
    """Cache grid background (static)"""

    grid_html = f"""
    <div class="grid" style="
        width: {size * cell_size}px;
        height: {size * cell_size}px;
        background-image:
            repeating-linear-gradient(...)
    "></div>
    """
    return grid_html

@st.cache_data(ttl=1.0)  # Cache for 1 second (semi-static)
def format_agent_state(agent_json: str):
    """Cache formatted state display

    Note: Use JSON string as key (immutable)
    Pydantic models are mutable and can't be cache keys!
    """
    agent = AgentSnapshot.parse_raw(agent_json)

    state_emoji = {
        "IDLE": "💤",
        "MOVING": "🚶",
        "THINKING": "💭",
        "TALKING": "💬"
    }.get(agent.state, "")

    return f"{agent.name} {state_emoji} ({agent.x}, {agent.y})"

# Usage
for name, agent in st.session_state.world.agents.items():
    # Cache hit if profile unchanged
    card_html = render_agent_profile_card(
        name,
        agent.traits,
        agent.goal
    )
    st.markdown(card_html, unsafe_allow_html=True)

    # Cache with short TTL for dynamic data
    state_display = format_agent_state(agent.json())
    st.text(state_display)
```

**Advanced: Cache visualization components**

```python
@st.cache_data
def generate_neon_css(theme_name: str = "cyberpunk"):
    """Cache CSS generation"""

    if theme_name == "cyberpunk":
        return """
        <style>
            .stApp { background: #0a0e27; }
            .agent-card { border: 2px solid #00d9ff; }
        </style>
        """
    # ... other themes

# Call once, cached for entire session
st.markdown(generate_neon_css(), unsafe_allow_html=True)
```

## ✔️ Acceptance Criteria

- [ ] Profile cards cached (verify with st.cache debug)
- [ ] 30-40% UI rendering speedup measured
- [ ] Cache invalidation works (e.g., on config change)
- [ ] No stale data displayed
- [ ] Memory usage reasonable (cache size < 10MB)

## 📊 Testing

```python
import time

def test_cache_speedup():
    # First call (cache miss)
    start = time.time()
    html1 = render_agent_profile_card("Alice", "Brave", "Save world")
    first_time = time.time() - start

    # Second call (cache hit)
    start = time.time()
    html2 = render_agent_profile_card("Alice", "Brave", "Save world")
    cached_time = time.time() - start

    assert html1 == html2
    assert cached_time < first_time * 0.1  # 10x+ faster
```

## ⚠️ Known Issues

- **Mutable arguments:** Pydantic models can't be cache keys
  - Solution: Convert to JSON string first
- **Memory leaks:** Large caches can accumulate
  - Solution: Use `ttl` parameter or `max_entries`
- **Stale data:** Cache doesn't auto-invalidate
  - Solution: Use short TTL for semi-dynamic data

## 📚 Streamlit Cache Types

| Decorator            | Use Case                       | Example                         |
| -------------------- | ------------------------------ | ------------------------------- |
| `@st.cache_data`     | Pure functions, immutable data | HTML rendering, formatting      |
| `@st.cache_resource` | Expensive objects (DB, models) | ChromaDB client, LLM model      |
| `ttl=N`              | Auto-expire after N seconds    | Dynamic data with lag tolerance |

## ⏱️ Estimate

**2-3 hours**

## 🏷️ Labels

`performance`, `ui`, `priority:medium`, `streamlit`
