"""
Neon Society Data Models
Clean implementation following architecture specification
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Literal, Optional
from datetime import datetime
from copy import deepcopy

class Memory(BaseModel):
    """Single memory entry with LRU and importance"""
    id: str = Field(default_factory=lambda: str(__import__('uuid').uuid4()))
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    importance: int = Field(ge=1, le=10)  # 1-10 scale
    type: Literal["observation", "conversation"] = "observation"

class AgentSnapshot(BaseModel):
    """Complete agent state at a single point in time"""
    name: str
    x: int = Field(default=10, ge=0, le=20)
    y: int = Field(default=10, ge=0, le=20)
    traits: str
    goal: str
    
    # State machine
    state: Literal["IDLE", "MOVING", "THINKING", "TALKING"] = "IDLE"
    
    # Throttling
    ticks_until_next_think: int = 0
    cached_direction: Literal["UP", "DOWN", "LEFT", "RIGHT", "STAY"] = "STAY"
    
    # Cognition
    current_thought: str = ""
    current_plan: str = ""
    
    # Memory (LRU capped at 20)
    memories: List[Memory] = Field(default_factory=list)
    
    class Config:
        arbitrary_types_allowed = True

class InteractionRecord(BaseModel):
    """Record of a conversation between agents"""
    tick: int
    participants: List[str]
    dialogue: str
    summary: str

class WorldState(BaseModel):
    """Immutable snapshot of entire world at a tick"""
    tick: int = 0
    agents: Dict[str, AgentSnapshot] = Field(default_factory=dict)
    recent_interactions: List[InteractionRecord] = Field(default_factory=list)
    
    def copy_snapshot(self) -> 'WorldState':
        """Deep copy for DVR history"""
        return WorldState(
            tick=self.tick,
            agents={name: AgentSnapshot(**agent.dict()) for name, agent in self.agents.items()},
            recent_interactions=[InteractionRecord(**rec.dict()) for rec in self.recent_interactions]
        )
    
    class Config:
        arbitrary_types_allowed = True
