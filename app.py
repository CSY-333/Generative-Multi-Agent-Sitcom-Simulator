"""
app.py
Streamlit application entry point for the two-agent sitcom simulator.
"""
from __future__ import annotations

import streamlit as st

from agent import Agent
from config import DEFAULT_REFLECTION_PERIOD
from memory_stream import MemoryStream
from models import AgentProfile, AgentState


def _init_session():
    if "agents" not in st.session_state:
        st.session_state.agents = {}
    if "turn_idx" not in st.session_state:
        st.session_state.turn_idx = 0
    if "transcript" not in st.session_state:
        st.session_state.transcript = []


def _build_agent(prefix: str) -> Agent:
    name = st.sidebar.text_input(f"{prefix} Name", value=f"{prefix}Agent")
    traits = st.sidebar.text_area(f"{prefix} Traits", value="공손하고 호기심 많으며, 사교적인 성격")
    goal = st.sidebar.text_area(f"{prefix} Goal", value="새로운 친구를 사귀고, 대화를 통해 상대를 이해한다")
    profile = AgentProfile(name=name, traits=traits, goal=goal)
    state = AgentState(turn_index=st.session_state.turn_idx)
    memory_stream = MemoryStream()
    return Agent(profile=profile, memory_stream=memory_stream, state=state, reflection_period=DEFAULT_REFLECTION_PERIOD)


def _reset_agents():
    st.session_state.agents = {
        "A": _build_agent("Agent A"),
        "B": _build_agent("Agent B"),
    }
    st.session_state.transcript = []
    st.session_state.turn_idx = 0


def _display_turn(turn_record):
    with st.chat_message(turn_record.speaker):
        st.write(turn_record.utterance)
        with st.expander("Debug"):  # type: ignore[attr-defined]
            st.write("Plan:", turn_record.plan)
            if turn_record.reflection:
                st.write("Reflection:", turn_record.reflection)
            st.write("Retrieved:")
            for m in turn_record.retrieved:
                st.write(f"- ({m.final_score:.2f}) {m.memory.content}")
            st.write("Store events:")
            for ev in turn_record.store_events:
                st.write(f"- {ev.memory_type}: {ev.reason} (importance={ev.importance})")


def _run_single_turn(context: str):
    agents = st.session_state.agents
    speaker_key = "A" if st.session_state.turn_idx % 2 == 0 else "B"
    listener_key = "B" if speaker_key == "A" else "A"
    speaker = agents[speaker_key]
    listener = agents[listener_key]

    recent_dialogue = [t.utterance for t in st.session_state.transcript[-4:]]
    turn = speaker.run_step(
        context=context,
        other_agent_name=listener.profile.name,
        recent_dialogue=recent_dialogue,
    )
    st.session_state.transcript.append(turn)
    st.session_state.turn_idx += 1
    _display_turn(turn)


def main():
    st.set_page_config(page_title="Neon Society: Sitcom Agents", layout="wide")
    st.title("Neon Society: Generative Agent RPG (MVP)")
    _init_session()

    st.sidebar.header("Agent Profiles")
    if st.sidebar.button("Reset & Initialize"):
        _reset_agents()

    if not st.session_state.get("agents"):
        _reset_agents()

    st.header("Conversation")
    context = st.text_area("Current context", value="도시 공원에서 우연히 마주쳤다.")
    if st.button("Run 1 Turn"):
        _run_single_turn(context)

    for t in st.session_state.transcript:
        _display_turn(t)


if __name__ == "__main__":
    main()
