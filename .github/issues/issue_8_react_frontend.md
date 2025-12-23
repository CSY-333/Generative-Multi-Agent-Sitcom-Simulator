## 🎯 Problem

Current Streamlit implementation has fundamental limitations:

- Frame rate locked to rerun speed (~1-2 FPS)
- CSS transitions break on iframe recreation
- No native state management for smooth animations
- Limited styling capabilities

## ✅ Solution

Build dedicated React/Next.js frontend with:

- Native React state for 60fps updates
- Framer Motion for buttery-smooth animations
- Full control over CSS/styling
- Mobile-responsive design

## 🔧 Implementation

### Setup Next.js Project

```bash
npx create-next-app@latest neon-society-ui --typescript --tailwind --app
cd neon-society-ui
npm install framer-motion socket.io-client
```

### `app/page.tsx` - Main Component

```typescript
"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { io, Socket } from "socket.io-client";

interface Agent {
  name: string;
  x: number;
  y: number;
  state: "IDLE" | "MOVING" | "THINKING" | "TALKING";
  thought: string;
  plan: string;
}

export default function NeonSociety() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [tick, setTick] = useState(0);
  const [socket, setSocket] = useState<Socket | null>(null);

  useEffect(() => {
    // Connect to backend
    const newSocket = io("http://localhost:8000");

    newSocket.on("world_update", (data) => {
      setAgents(data.agents);
      setTick(data.tick);
    });

    setSocket(newSocket);

    return () => {
      newSocket.disconnect();
    };
  }, []);

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-950 to-slate-900">
      {/* Header */}
      <header className="p-6 bg-slate-900/50 backdrop-blur-md border-b border-cyan-500/20">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-purple-600 bg-clip-text text-transparent">
          🌆 Neon Society
        </h1>
        <p className="text-slate-400 mt-2">Tick: {tick}</p>
      </header>

      {/* World Map */}
      <div className="p-8">
        <WorldMap agents={agents} />
      </div>

      {/* Agent Cards */}
      <div className="grid grid-cols-2 gap-4 p-8">
        {agents.map((agent) => (
          <AgentCard key={agent.name} agent={agent} />
        ))}
      </div>
    </main>
  );
}
```

### `components/WorldMap.tsx`

```typescript
import { motion } from "framer-motion";

const CELL_SIZE = 30;
const MAP_SIZE = 20;

export function WorldMap({ agents }: { agents: Agent[] }) {
  return (
    <div
      className="relative mx-auto bg-gradient-to-br from-slate-800/50 to-slate-900/50 
                 border-2 border-cyan-500 rounded-lg shadow-2xl shadow-cyan-500/20"
      style={{
        width: MAP_SIZE * CELL_SIZE,
        height: MAP_SIZE * CELL_SIZE,
      }}
    >
      {/* Grid Overlay */}
      <div className="absolute inset-0 bg-grid-pattern opacity-10" />

      {/* Agents */}
      {agents.map((agent) => (
        <motion.div
          key={agent.name}
          className="absolute w-7 h-7 rounded-full flex items-center justify-center
                     font-bold text-white text-xs shadow-lg"
          style={{
            backgroundColor: getAgentColor(agent.name),
            boxShadow: `0 0 20px ${getAgentColor(agent.name)}`,
          }}
          animate={{
            x: agent.x * CELL_SIZE,
            y: agent.y * CELL_SIZE,
          }}
          transition={{
            duration: 0.5,
            ease: "easeInOut",
          }}
        >
          {agent.name[0]}

          {/* State Indicator */}
          <StateIndicator state={agent.state} />
        </motion.div>
      ))}
    </div>
  );
}

function StateIndicator({ state }: { state: string }) {
  const animations = {
    TALKING: { scale: [1, 1.2, 1], rotate: [0, 5, -5, 0] },
    THINKING: { opacity: [1, 0.3, 1] },
    MOVING: { rotate: 360 },
    IDLE: {},
  };

  const emoji = {
    TALKING: "💬",
    THINKING: "💭",
    MOVING: "🚶",
    IDLE: "💤",
  }[state];

  return (
    <motion.div
      className="absolute -top-2 -right-2 text-sm"
      animate={animations[state]}
      transition={{ duration: 1, repeat: Infinity }}
    >
      {emoji}
    </motion.div>
  );
}
```

### `components/AgentCard.tsx`

```typescript
import { motion } from "framer-motion";

export function AgentCard({ agent }: { agent: Agent }) {
  return (
    <motion.div
      className="p-4 bg-gradient-to-br from-slate-800/80 to-purple-900/80
                 backdrop-blur-md rounded-lg border border-cyan-500/30
                 shadow-lg hover:shadow-cyan-500/50 transition-shadow"
      whileHover={{ scale: 1.02 }}
    >
      <h3 className="text-xl font-bold text-cyan-400">🧙 {agent.name}</h3>

      <div className="mt-2 text-sm">
        <p className="text-slate-300">
          <span className="text-purple-400">State:</span> {agent.state}
        </p>
        <p className="text-slate-300">
          <span className="text-purple-400">Position:</span> ({agent.x},{" "}
          {agent.y})
        </p>
      </div>

      {agent.thought && (
        <motion.div
          className="mt-3 p-2 bg-cyan-900/30 rounded border-l-2 border-cyan-500"
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <p className="text-xs text-cyan-300">💭 {agent.thought}</p>
        </motion.div>
      )}
    </motion.div>
  );
}
```

### `tailwind.config.js` - Custom Styles

```javascript
module.exports = {
  theme: {
    extend: {
      backgroundImage: {
        "grid-pattern":
          "repeating-linear-gradient(0deg, rgba(100,150,200,0.1) 0px, rgba(100,150,200,0.1) 1px, transparent 1px, transparent 30px)",
      },
    },
  },
};
```

## ✔️ Acceptance Criteria

- [ ] 60fps smooth animations verified
- [ ] Framer Motion transitions work flawlessly
- [ ] WebSocket connection stable
- [ ] Mobile responsive (works on phones)
- [ ] Theme matches Neon Society aesthetic
- [ ] No performance degradation vs Streamlit

## 📊 Performance Targets

| Metric               | Target           |
| -------------------- | ---------------- |
| Animation FPS        | 60               |
| State update latency | <50ms            |
| Initial load time    | <2s              |
| Bundle size          | <500KB (gzipped) |

## 🎨 Design System

**Colors:**

- Primary: Cyan (#00d9ff)
- Secondary: Purple (#a855f7)
- Background: Slate (#0f172a)
- Accents: Hot Pink (#ff006e)

**Animations:**

- Duration: 0.5s (default)
- Easing: ease-in-out
- State transitions: Framer Motion variants

## ⏱️ Estimate

**4-5 days**

## 🏷️ Labels

`architecture`, `frontend`, `priority:low`, `next-gen`, `react`
