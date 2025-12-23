## 🎯 Problem

Streamlit's rerun architecture creates fundamental limitations:

- Full page reload every tick → 500ms+ overhead
- Cannot achieve true 60fps animations
- iframe recreation breaks CSS transitions
- State management complexity

## ✅ Solution

Separate backend (FastAPI) from frontend (React/Next.js) with WebSocket streaming.

**Architecture:**

```
┌──────────────────┐         WebSocket          ┌──────────────────┐
│  Python Backend  │←─────────────────────────→│  React Frontend  │
│  (Simulation)    │  JSON State Streaming      │  (Visualization) │
│                  │                             │                  │
│  - Tick engine   │                             │  - Smooth UI     │
│  - Gemini calls  │                             │  - 60fps anim    │
│  - Memory DB     │                             │  - Framer Motion │
└──────────────────┘                             └──────────────────┘
```

## 🔧 Implementation

### Backend: `neon_server.py`

```python
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json

app = FastAPI()

# CORS for React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global simulation state
world_state = WorldState()

@app.websocket("/ws/simulation")
async def simulation_stream(websocket: WebSocket):
    """Stream simulation updates to frontend"""
    await websocket.accept()

    try:
        while True:
            # Run simulation tick
            world_state = sim.tick(world_state, use_mock=False)

            # Serialize and send
            payload = {
                "tick": world_state.tick,
                "agents": [
                    {
                        "name": a.name,
                        "x": a.x,
                        "y": a.y,
                        "state": a.state,
                        "thought": a.current_thought,
                        "plan": a.current_plan
                    }
                    for a in world_state.agents.values()
                ],
                "interactions": [
                    {
                        "tick": i.tick,
                        "participants": i.participants,
                        "dialogue": i.dialogue
                    }
                    for i in world_state.recent_interactions[-5:]
                ]
            }

            await websocket.send_json(payload)
            await asyncio.sleep(1.0)  # 1 tick/sec

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

@app.post("/api/control/play")
async def play():
    """Start/stop simulation"""
    # Toggle play state
    return {"status": "playing"}

@app.get("/api/state")
async def get_state():
    """Get current world state"""
    return world_state.dict()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Frontend: React/Next.js

**`pages/index.tsx`**

```typescript
import { useState, useEffect } from "react";
import { motion } from "framer-motion";

interface Agent {
  name: string;
  x: number;
  y: number;
  state: string;
  thought: string;
}

export default function NeonSociety() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [tick, setTick] = useState(0);

  useEffect(() => {
    // Connect to WebSocket
    const ws = new WebSocket("ws://localhost:8000/ws/simulation");

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setAgents(data.agents);
      setTick(data.tick);
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    return () => ws.close();
  }, []);

  return (
    <div className="world-map">
      <h1>Tick: {tick}</h1>

      {agents.map((agent) => (
        <motion.div
          key={agent.name}
          className="agent"
          animate={{
            x: agent.x * 30, // Cell size
            y: agent.y * 30,
          }}
          transition={{
            duration: 0.5,
            ease: "easeInOut",
          }}
        >
          <span>{agent.name[0]}</span>
          {agent.state === "TALKING" && (
            <motion.div
              className="state-indicator"
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ repeat: Infinity, duration: 1 }}
            >
              💬
            </motion.div>
          )}
        </motion.div>
      ))}
    </div>
  );
}
```

**`styles/globals.css`** (Neon theme)

```css
.world-map {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  position: relative;
  border: 2px solid #00d9ff;
  box-shadow: 0 0 30px rgba(0, 217, 255, 0.3);
}

.agent {
  position: absolute;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: #ff006e;
  box-shadow: 0 0 20px currentColor;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
}

.state-indicator {
  position: absolute;
  top: -10px;
  right: -10px;
  font-size: 16px;
}
```

## ✔️ Acceptance Criteria

- [ ] Backend runs independently (`python neon_server.py`)
- [ ] Frontend connects via WebSocket
- [ ] Smooth 60fps animations (Framer Motion)
- [ ] No transition breaks on state updates
- [ ] Latency < 50ms (local network)
- [ ] Error recovery (reconnect on disconnect)

## 📊 Performance Comparison

| Metric               | Streamlit       | WebSocket + React |
| -------------------- | --------------- | ----------------- |
| Animation FPS        | 1-2             | 60                |
| State update latency | 500ms+          | <50ms             |
| Transitions          | Broken (iframe) | Native CSS        |
| Scalability          | Limited         | High              |

## 📚 Tech Stack

**Backend:**

- FastAPI (async Python web framework)
- Uvicorn (ASGI server)
- python-socketio (WebSocket)

**Frontend:**

- Next.js 14 (React framework)
- Framer Motion (animations)
- TailwindCSS (styling)

## ⏱️ Estimate

**2-3 days**

## 🏷️ Labels

`architecture`, `backend`, `priority:low`, `next-gen`
