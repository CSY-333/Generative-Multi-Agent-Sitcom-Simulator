## 🎯 Problem

Current proximity detection uses naive O(n²) algorithm.

**Performance Impact:**

- 2 agents: 1 comparison
- 10 agents: 45 comparisons ❌
- 100 agents: 4,950 comparisons ❌❌❌

**Current Code (neon_simulation.py:33-60):**

```python
for i, name_a in enumerate(active_names):  # O(n)
    for name_b in active_names[i+1:]:      # O(n)
        dist = calculate_distance(...)      # = O(n²)
```

## ✅ Solution

Implement **Spatial Hash Grid** for O(1) neighbor lookup per agent.

**Key Insight:**
Only check agents in adjacent grid cells, not entire world!

```
Grid Cell Size = INTERACTION_RADIUS
Agent at (10,10) → Cell (2,2)
Only check cells: (1,1), (1,2), (1,3), (2,1), (2,2), ...
```

## 🔧 Implementation

**File:** `neon_spatial.py` (NEW)

```python
from collections import defaultdict
from typing import List, Tuple
import math

class SpatialGrid:
    """Spatial hash grid for O(1) proximity queries"""

    def __init__(self, cell_size: float = 5.0):
        self.cell_size = cell_size
        self.grid: defaultdict[Tuple[int, int], List] = defaultdict(list)

    def clear(self):
        """Clear all cells"""
        self.grid.clear()

    def _get_cell(self, x: float, y: float) -> Tuple[int, int]:
        """Convert world coords to cell coords"""
        return (int(x // self.cell_size), int(y // self.cell_size))

    def insert(self, agent):
        """Insert agent into grid"""
        cell = self._get_cell(agent.x, agent.y)
        self.grid[cell].append(agent)

    def find_nearby(self, agent, radius: float) -> List:
        """Find all agents within radius (O(1) expected)"""
        cell_x, cell_y = self._get_cell(agent.x, agent.y)

        # How many cells to check? (ceil to be safe)
        cell_radius = math.ceil(radius / self.cell_size)

        nearby = []
        for dx in range(-cell_radius, cell_radius + 1):
            for dy in range(-cell_radius, cell_radius + 1):
                check_cell = (cell_x + dx, cell_y + dy)
                nearby.extend(self.grid.get(check_cell, []))

        # Filter by actual distance
        result = []
        for other in nearby:
            if other == agent:
                continue
            dist = math.sqrt((agent.x - other.x)**2 + (agent.y - other.y)**2)
            if dist <= radius:
                result.append(other)

        return result
```

**File:** `neon_simulation.py`

```python
from neon_spatial import SpatialGrid

def detect_interaction_groups(world: WorldState) -> List[List[str]]:
    """Optimized with spatial hash grid"""

    # Build grid
    grid = SpatialGrid(cell_size=config.INTERACTION_RADIUS)
    for agent in world.agents.values():
        grid.insert(agent)

    # Find groups
    processed = set()
    groups = []

    for name, agent in world.agents.items():
        if name in processed:
            continue

        # O(1) lookup!
        nearby_agents = grid.find_nearby(agent, config.INTERACTION_RADIUS)
        nearby_names = [a.name for a in nearby_agents]

        if nearby_names:
            group = [name] + nearby_names
            groups.append(group)
            processed.update(group)

    return groups
```

## ✔️ Acceptance Criteria

- [ ] **10 agents:** <5 comparisons per tick (vs 45 before)
- [ ] **100 agents:** <50 comparisons per tick (vs 4950 before)
- [ ] Correctness: Same results as naive method
- [ ] Performance: 10x faster with 10 agents
- [ ] Performance: 100x faster with 100 agents

## 📊 Testing

```python
def test_spatial_grid_correctness():
    """Verify same results as naive method"""
    agents = create_test_agents(20)

    # Naive O(n²)
    naive_result = naive_proximity(agents)

    # Spatial grid
    grid = SpatialGrid()
    for a in agents:
        grid.insert(a)
    grid_result = [grid.find_nearby(a, 2.0) for a in agents]

    assert set(naive_result) == set(grid_result)

def test_spatial_grid_performance():
    agents = create_test_agents(100)

    start = time.time()
    # Naive: 4950 comparisons
    naive_proximity(agents)
    naive_time = time.time() - start

    start = time.time()
    # Grid: ~50 comparisons
    grid = SpatialGrid()
    for a in agents:
        grid.insert(a)
    for a in agents:
        grid.find_nearby(a, 2.0)
    grid_time = time.time() - start

    assert grid_time < naive_time * 0.01  # 100x faster
```

## 📈 Benchmark Results (Expected)

| Agents | Naive (ms) | Grid (ms) | Speedup |
| ------ | ---------- | --------- | ------- |
| 10     | 2          | 0.2       | 10x     |
| 50     | 50         | 1         | 50x     |
| 100    | 200        | 2         | 100x    |

## ⏱️ Estimate

**4-6 hours**

## 🏷️ Labels

`performance`, `algorithm`, `priority:medium`, `scalability`
