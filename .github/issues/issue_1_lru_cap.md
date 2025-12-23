## 🎯 Problem

Current DVR implementation stores unbounded history, causing memory overflow after 1000+ ticks.

**Measured Impact:**

- Current: ~9KB per snapshot × 1000 ticks = **9MB+ memory usage**
- Risk: Streamlit session crashes at ~50-100MB
- User experience: App becomes unresponsive after long simulations

## ✅ Solution

Implement LRU (Least Recently Used) circular buffer with configurable cap.

**Target:** MAX_HISTORY = 100 snapshots

## 🔧 Implementation

**File:** `neon_app.py`

```python
# Add to neon_config.py
MAX_HISTORY_SIZE = 100

# Update in neon_app.py (line ~141)
if st.session_state.is_playing and not st.session_state.dvr_mode:
    snapshot = st.session_state.world.copy_snapshot()
    st.session_state.history.append(snapshot)

    # NEW: LRU eviction
    if len(st.session_state.history) > config.MAX_HISTORY_SIZE:
        st.session_state.history.pop(0)  # Remove oldest

    st.session_state.world = sim.tick(...)
```

**DVR Slider Update:**

```python
# Update slider max value (line ~154)
max_value = min(len(st.session_state.history) - 1, config.MAX_HISTORY_SIZE - 1)
```

## ✔️ Acceptance Criteria

- [ ] Memory usage stays under 10MB at 1000+ ticks
- [ ] DVR slider works correctly with capped history
- [ ] Oldest snapshots are evicted (FIFO)
- [ ] No performance degradation (<5ms overhead per tick)
- [ ] Config variable allows easy adjustment

## 📊 Testing

```python
def test_lru_cap():
    st.session_state.history = []
    for i in range(200):
        st.session_state.history.append(f"snapshot_{i}")
        # Apply LRU logic here

    assert len(st.session_state.history) == 100
    assert st.session_state.history[0] == "snapshot_100"  # Oldest kept
    assert st.session_state.history[-1] == "snapshot_199"  # Newest
```

## ⏱️ Estimate

**5 minutes**

## 🏷️ Labels

`performance`, `quick-win`, `priority:high`
