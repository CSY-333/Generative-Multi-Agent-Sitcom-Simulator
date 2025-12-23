## 🎯 Problem

Full state snapshots waste 90% memory storing unchanged agent data.

**Current Waste:**

- Agent at (5,5) stays still for 10 ticks → Same data copied 10 times
- Only 1-2 agents move per tick, but all 10 are copied
- **9KB per snapshot** → Target: **1KB per snapshot**

## ✅ Solution

Store only deltas (changes) between ticks instead of full world state.

**Architecture:**

```
Full Snapshot (Tick 0) → Diff (Tick 1) → Diff (Tick 2) → ...
```

Reconstruction: Base + Sum(Diffs)

## 🔧 Implementation

**File:** `neon_models.py`

```python
class WorldStateDiff(BaseModel):
    """Store only changes, not full state"""
    tick: int
    changed_agents: Dict[str, AgentSnapshot] = Field(default_factory=dict)
    new_interactions: List[InteractionRecord] = Field(default_factory=list)

    def apply_to(self, base_world: WorldState) -> WorldState:
        """Reconstruct world state from diff"""
        new_world = base_world.copy()
        new_world.tick = self.tick

        # Apply agent changes
        for name, agent in self.changed_agents.items():
            new_world.agents[name] = agent

        # Append interactions
        new_world.recent_interactions.extend(self.new_interactions)

        return new_world

def create_diff(prev: WorldState, curr: WorldState) -> WorldStateDiff:
    """Generate diff between two states"""
    changed = {}

    for name, agent in curr.agents.items():
        prev_agent = prev.agents.get(name)
        if prev_agent is None or agent != prev_agent:
            changed[name] = agent

    # Only new interactions (last N)
    new_interactions = curr.recent_interactions[len(prev.recent_interactions):]

    return WorldStateDiff(
        tick=curr.tick,
        changed_agents=changed,
        new_interactions=list(new_interactions)
    )
```

**File:** `neon_app.py`

```python
# Update snapshot storage (line ~141)
if st.session_state.is_playing:
    prev_world = st.session_state.world
    curr_world = sim.tick(...)

    # Store diff instead of full snapshot
    diff = create_diff(prev_world, curr_world)
    st.session_state.history.append(diff)

    st.session_state.world = curr_world

# DVR reconstruction (line ~162)
if st.session_state.dvr_mode:
    # Reconstruct from base + diffs
    base = st.session_state.history[0]  # Full snapshot at tick 0
    reconstructed = base

    for diff in st.session_state.history[1:selected_tick+1]:
        reconstructed = diff.apply_to(reconstructed)

    st.session_state.world = reconstructed
```

## ✔️ Acceptance Criteria

- [ ] Memory usage: <1KB per diff (90% reduction verified)
- [ ] DVR reconstruction produces identical state
- [ ] No data loss over 1000 ticks
- [ ] Performance: <10ms per diff creation
- [ ] Backward compatible (can migrate old snapshots)

## 📊 Testing

```python
def test_diff_accuracy():
    world1 = create_test_world()
    world2 = sim.tick(world1)

    diff = create_diff(world1, world2)
    reconstructed = diff.apply_to(world1)

    assert reconstructed == world2  # Perfect reconstruction

def test_memory_savings():
    full_size = len(pickle.dumps(world2))
    diff_size = len(pickle.dumps(diff))

    assert diff_size < full_size * 0.2  # <20% of original
```

## ⏱️ Estimate

**1-2 hours**

## 🏷️ Labels

`performance`, `optimization`, `priority:high`
