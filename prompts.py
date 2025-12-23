"""
prompts.py
Static prompt templates for planner, reflection, and utterance generation.
These are simple helpers rather than full LLM prompts for the offline MVP.
"""
from __future__ import annotations

from models import AgentProfile


def system_prompt(profile: AgentProfile) -> str:
    return (
        f"너는 {profile.name}이다. "
        f"성격: {profile.traits}. "
        f"목표를 의식하며 말해라: {profile.goal}. "
        "대화는 1~2문장으로 짧게 유지하고 메타발언을 하지 말아라."
    )


def planner_prompt(profile: AgentProfile, context: str) -> str:
    return (
        f"목표: {profile.goal}. 현재 상황: {context}. "
        "다음 턴에서 달성할 구체적인 행동을 한 문장으로 계획하라."
    )


def reflection_prompt(profile: AgentProfile, context: str) -> str:
    return (
        f"{profile.name}의 최근 경험을 돌아보며 1~3개의 교훈을 짧게 기록하라. "
        f"상황: {context}"
    )
