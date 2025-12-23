"""
models.py
Data models for the Generative Multi-Agent Sitcom Simulator.
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Literal, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, validator


MemoryType = Literal["observation", "reflection", "plan"]


class Memory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    content: str
    memory_type: MemoryType
    created_at: datetime = Field(default_factory=datetime.utcnow)
    importance: int = Field(default=3, ge=1, le=10)
    source: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    embedding: Optional[List[float]] = None

    @validator("content")
    def validate_content(cls, value: str) -> str:
        if not value:
            raise ValueError("memory content must not be empty")
        if not (1 <= len(value) <= 2000):
            raise ValueError("memory content must be between 1 and 2000 characters")
        return value


class AgentProfile(BaseModel):
    name: str
    traits: str
    goal: str

    @validator("traits")
    def validate_traits(cls, value: str) -> str:
        if len(value.strip()) < 20:
            raise ValueError("traits should be a descriptive string (>= 20 chars)")
        return value

    @validator("goal")
    def validate_goal(cls, value: str) -> str:
        if len(value.strip()) < 5:
            raise ValueError("goal should be at least one short sentence")
        return value


class AgentState(BaseModel):
    turn_index: int = 0
    current_context: str = ""
    last_plan: Optional[str] = None
    last_utterance: Optional[str] = None
    mood_hint: Optional[str] = None


class StoreEvent(BaseModel):
    memory_type: MemoryType
    content: str
    importance: int
    stored: bool
    reason: str


class ScoredMemory(BaseModel):
    memory: Memory
    similarity: float
    recency_score: float
    importance_score: float
    final_score: float


class TurnRecord(BaseModel):
    turn_id: str = Field(default_factory=lambda: str(uuid4()))
    speaker: str
    listener: str
    context_in: str
    retrieved: List[ScoredMemory]
    reflection: Optional[str]
    plan: str
    utterance: str
    store_events: List[StoreEvent]
    timestamps: dict
