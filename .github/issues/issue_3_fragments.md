## 🎯 Problem

Every tick triggers full page rerun (`st.rerun()`), causing 500ms+ overhead.

**Bottleneck Analysis:**

- Map updates: Only agents move (2-3 elements change)
- Sidebar: Static configuration (never changes)
- Agent cards: Only 1-2 update per tick
- **But entire app reruns** → Wasteful!

## ✅ Solution

Use Streamlit Fragments (1.30+) to isolate updates to only changed components.

**Architecture:**

```
┌─────────────────────────────────────┐
│  Sidebar (Static) - No rerun        │
├─────────────────────────────────────┤
│  ┌──────────────────────────┐       │
│  │ Map Fragment (Dynamic)   │ ← Only this reruns
│  └──────────────────────────┘       │
│  ┌──────────────────────────┐       │
│  │ Agents Fragment          │ ← And this
│  └──────────────────────────┘       │
└─────────────────────────────────────┘
```

## 🔧 Implementation

**Requirement:** Streamlit >= 1.30.0

```bash
pip install streamlit>=1.30.0
```

**File:** `neon_app.py`

```python
import streamlit as st

# Fragment 1: World Map (updates every tick)
@st.experimental_fragment(run_every="1s")  # Auto-rerun
def world_map_fragment():
    st.markdown("### 🗺️ World Map")

    import neon_visualization as viz
    viz.render_neon_world_map(
        agents=st.session_state.world.agents,
        map_size=20,
        dvr_mode=st.session_state.dvr_mode
    )

# Fragment 2: Agent Cards (updates every tick)
@st.experimental_fragment(run_every="1s")
def agent_panel_fragment():
    st.markdown("### 👥 Agents")

    for name, agent in st.session_state.world.agents.items():
        with st.expander(f"🧙 {name}", expanded=False):
            st.markdown(f"**State:** {agent.state}")
            st.markdown(f"**Position:** ({agent.x}, {agent.y})")
            if agent.current_thought:
                st.info(f"💭 {agent.current_thought}")

# Main app (runs once, then only fragments update)
st.title("🌆 Neon Society")

# Control panel (static, no rerun needed)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("▶️ Play"):
        st.session_state.is_playing = True

# Fragments auto-update
world_map_fragment()
agent_panel_fragment()
```

**Alternative: Manual Fragment Trigger**

```python
@st.experimental_fragment
def world_map_fragment():
    # Manual control, no auto-rerun
    ...

# Trigger fragment rerun on button click
if st.session_state.is_playing:
    world_map_fragment.rerun()  # Only this fragment
```

## ✔️ Acceptance Criteria

- [ ] Sidebar doesn't rerun when map updates
- [ ] 50%+ speed improvement measured (tick < 250ms)
- [ ] No visual glitches or stale data
- [ ] Fragment isolation verified (debug logs)
- [ ] Works with Auto-Play mode

## 📊 Testing

```python
import time

def test_fragment_performance():
    # Before: Full rerun
    start = time.time()
    st.rerun()
    full_rerun_time = time.time() - start

    # After: Fragment only
    start = time.time()
    world_map_fragment.rerun()
    fragment_time = time.time() - start

    assert fragment_time < full_rerun_time * 0.5  # 50% faster
```

## ⚠️ Known Issues

- Fragments are experimental (may change in Streamlit updates)
- `run_every` requires Streamlit running (not for testing)
- Nested fragments can cause complexity

## 📚 References

- [Streamlit Fragments Docs](https://docs.streamlit.io/library/api-reference/execution-flow/st.experimental_fragment)

## ⏱️ Estimate

**1-2 hours**

## 🏷️ Labels

`performance`, `ui`, `priority:high`, `streamlit`
