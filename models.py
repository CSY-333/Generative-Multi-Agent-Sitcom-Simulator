"""
models.py
Defines Pydantic models for Memory, AgentProfile, TurnRecord, etc.
Supports 10-agent scalability via active_agents list.
"""
import uuid
from datetime import datetime
from typing import Literal, Optional, List, Dict, Any
from pydantic import BaseModel, Field

class Memory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    memory_type: Literal["observation", "reflection", "plan"]
    created_at: datetime = Field(default_factory=datetime.now)
    importance: int = Field(..., ge=1, le=10, description="Importance score 1-10")
    source: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    embedding: Optional[List[float]] = None

    class Config:
        validate_assignment = True

class AgentProfile(BaseModel):
    name: str
    traits: str
    goal: str

class AgentState(BaseModel):
    turn_index: int = 0
    current_context: str = ""
    active_agents: List[str] = Field(default_factory=list, description="List of names of agents currently in the scene")
    last_plan: Optional[str] = None
    last_utterance: Optional[str] = None
    mood_hint: Optional[str] = None
    status: str = "IDLE"
    status_message: str = "Observing the grid"
    thought_preview: Optional[str] = None
    
    # Spatial coordinates (0-20)
    x: int = Field(default=10)
    y: int = Field(default=10)
    
    # Neon Society enhancements
    current_action: Literal["IDLE", "MOVING", "TALKING"] = "IDLE"
    ticks_until_next_think: int = 0  # Throttling counter
    cached_direction: Optional[str] = None  # For movement inertia

class ScoredMemory(BaseModel):
    memory: Memory
    similarity_score: float = 0.0
    recency_score: float = 0.0
    importance_score: float = 0.0
    final_score: float = 0.0

class StoreEvent(BaseModel):
    memory_type: str
    content: str
    importance: int
    stored: bool
    reason: str

class TurnRecord(BaseModel):
    turn_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    turn_index: int
    speaker_name: str
    context_in: str
    retrieved_memories: List[ScoredMemory] = Field(default_factory=list)
    reflection: Optional[str] = None
    plan: str
    utterance: str
    store_events: List[StoreEvent] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # New field for 10-agent logic
    selection_reason: Optional[str] = Field(None, description="Why this agent was selected as speaker")
