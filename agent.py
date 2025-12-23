"""
agent.py
Core agent loop implementing Retrieve -> Reflect -> Plan -> Act -> Store.
"""
from __future__ import annotations

from typing import List, Optional

from models import AgentProfile, AgentState, Memory, StoreEvent, TurnRecord
from memory_stream import MemoryStream
from prompts import planner_prompt, system_prompt
from utils import timestamp


class Agent:
    def __init__(
        self,
        profile: AgentProfile,
        memory_stream: MemoryStream,
        state: Optional[AgentState] = None,
        reflection_period: int = 6,
    ) -> None:
        self.profile = profile
        self.memory_stream = memory_stream
        self.state = state or AgentState()
        self.reflection_period = reflection_period

    def run_step(
        self,
        *,
        context: str,
        other_agent_name: str,
        recent_dialogue: Optional[List[str]] = None,
    ) -> TurnRecord:
        recent_dialogue = recent_dialogue or []
        query = f"{context}\n상대:{other_agent_name}\n내 목표:{self.profile.goal}"
        retrieved = self.memory_stream.retrieve(query)

        reflection_text: Optional[str] = None
        if self.state.turn_index % self.reflection_period == 0:
            summary = " ".join(recent_dialogue[-3:]) if recent_dialogue else ""
            reflection_text = f"{self.profile.name}는 최근 상황을 돌아보며 {summary or '간단한 생각을 정리했다.'}"
            reflection_memory = Memory(
                content=reflection_text,
                memory_type="reflection",
                importance=7,
                source="reflection",
            )
            self.memory_stream.add_memory(reflection_memory)

        plan = self._make_plan(context, reflection_text, retrieved)
        utterance = self._make_utterance(context, plan)
        store_events = self._store_observation(utterance)

        turn_record = TurnRecord(
            speaker=self.profile.name,
            listener=other_agent_name,
            context_in=context,
            retrieved=retrieved,
            reflection=reflection_text,
            plan=plan,
            utterance=utterance,
            store_events=store_events,
            timestamps={"created_at": timestamp()},
        )

        self.state.turn_index += 1
        self.state.last_plan = plan
        self.state.last_utterance = utterance
        self.state.current_context = context
        return turn_record

    def _make_plan(self, context: str, reflection: Optional[str], retrieved) -> str:
        prompt = planner_prompt(self.profile, context)
        memory_hint = retrieved[0].memory.content if retrieved else "이전 기억 없음"
        reflection_hint = reflection or ""
        return f"{prompt} | 참고: {memory_hint}. {reflection_hint}"[:280]

    def _make_utterance(self, context: str, plan: str) -> str:
        sys_prompt = system_prompt(self.profile)
        return f"{sys_prompt} 지금 상황: {context}. 계획: {plan}."

    def _store_observation(self, utterance: str) -> List[StoreEvent]:
        importance = self.memory_stream.importance_for_observation(utterance, goal_hint=self.profile.goal)
        decision = importance >= 6
        events: List[StoreEvent] = [
            StoreEvent(
                memory_type="observation",
                content=utterance,
                importance=importance,
                stored=decision,
                reason="rule-based threshold >=6" if decision else "below threshold",
            )
        ]
        if decision:
            self.memory_stream.add_memory(
                Memory(
                    content=utterance,
                    memory_type="observation",
                    importance=importance,
                    source="agent_said",
                )
            )
        return events
