"""
prompts.py
System prompts, planning prompts, reflection prompts.
"""

def get_system_prompt(name: str, traits: str, goal: str) -> str:
    return f"""너는 '{name}'이다.
다음의 성격(Traits)을 가지고 행동해라: {traits}
너의 목표(Goal)는 다음과 같다: {goal}

규칙:
1. 너의 성격에 맞춰 자연스럽게 한국어로 대화해라.
2. 1~2문장으로 짧게 말해라.
3. 상황에 맞지 않는 말이나 AI 같은 메타 발언("저는 인공지능 모델입니다")은 절대 금지다.
4. 상대방의 말을 경청하고 그에 반응해라.
"""

def get_planner_prompt(context: str, recent_memories: str) -> str:
    return f"""
현재 상황:
{context}

떠오른 생각/기억:
{recent_memories}

위 내용을 바탕으로, **다음 턴에 할 구체적인 행동이나 발화 의도**를 한 문장으로 수립해라.
예시: "철수에게 어제 실수에 대해 사과한다.", "화제를 날씨로 돌린다."
"""

def get_reflection_prompt(recent_observations: str) -> str:
    return f"""
최근 관찰 내용:
{recent_observations}

위 내용을 요약하고, **새롭게 알게 된 사실, 감정의 변화, 또는 관계의 변화**를 1~3문장의 통찰(Insight) 형태로 정리해라.
명확한 정보가 없다면 "특이 사항 없음"이라고 해라.
"""

def get_speaker_selection_prompt(context: str, active_agents: list[str]) -> str:
    agents_str = ", ".join(active_agents)
    return f"""
현재 대화 상황:
{context}

참여 중인 인물: {agents_str}

이 상황에서 **누가 말하는 것이 가장 자연스러운가?**
인물 이름 딱 하나만 출력해라.
"""
