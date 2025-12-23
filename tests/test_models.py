"""
test_models.py
Test the integrity of Pydantic models
"""
import pytest
from datetime import datetime
from models import Memory, AgentProfile, AgentState, TurnRecord

def test_memory_creation():
    mem = Memory(content="Test memory", memory_type="observation", importance=5)
    assert mem.id is not None
    assert isinstance(mem.created_at, datetime)
    assert mem.importance == 5

def test_memory_importance_validation():
    with pytest.raises(ValueError):
        Memory(content="Bad", memory_type="observation", importance=11)

def test_agent_state_active_agents():
    state = AgentState(active_agents=["A", "B", "C"])
    assert "A" in state.active_agents
    assert len(state.active_agents) == 3

def test_turn_record_defaults():
    rec = TurnRecord(
        turn_index=1,
        speaker_name="Chulsoo",
        context_in="Quiet room",
        plan="Say hello",
        utterance="Hello"
    )
    assert rec.turn_id is not None
    assert rec.selection_reason is None
