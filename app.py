"""
app.py
Streamlit application entry point for 10-Agent Sitcom Simulator.
Now with RPG-style UI and Time Travel features.
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import os

from models import AgentProfile, TurnRecord, AgentState
from agent import Agent
from memory_stream import MemoryStream
from speaker_selector import SpeakerSelector
import config

# Page Config
st.set_page_config(
    page_title="Generative Agent RPG",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for RPG Theme ---
def inject_custom_css():
    st.markdown("""
    <style>
        /* Main Background */
        .stApp {
            background-color: #1a1a2e;
            color: #e0e0e0;
        }
        
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #16213e;
        }
        
        /* Containers */
        .stChatInput, .stTextInput > div > div > input, .stTextArea > div > div > textarea {
            background-color: #0f3460;
            color: #fff;
            border: 1px solid #e94560;
        }
        
        /* Neon Buttons */
        .stButton > button {
            background-color: #e94560;
            color: white;
            border-radius: 5px;
            border: none;
            box-shadow: 0 0 10px #e94560;
        }
        .stButton > button:hover {
            background-color: #ff2e63;
             box-shadow: 0 0 20px #ff2e63;
        }
        
        /* Dialogue Bubbles */
        .rpg-bubble {
            background-color: #0f3460;
            border-left: 5px solid #e94560;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
        }
        .rpg-speaker {
            font-weight: bold;
            color: #e94560;
            font-size: 1.1em;
            margin-bottom: 5px;
        }
        .rpg-text {
            font-family: 'Courier New', Courier, monospace;
            font-size: 1.0em;
        }
        
        /* Metrics */
        div[data-testid="stMetricValue"] {
            color: #e94560;
            text-shadow: 0 0 5px #e94560;
        }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# Initialize Session State
if "agents" not in st.session_state:
    st.session_state.agents = {}  # name -> Agent object
if "transcript" not in st.session_state:
    st.session_state.transcript = []  # list of TurnRecord
if "turn_idx" not in st.session_state:
    st.session_state.turn_idx = 0
if "selector" not in st.session_state:
    st.session_state.selector = SpeakerSelector()

def add_agent(name, traits, goal):
    if name in st.session_state.agents:
        # st.warning(f"Agent {name} already exists!") # Suppress warning for default init
        return
    
    # Initialize Memory Stream
    memory_stream = MemoryStream(name)
    
    # Initialize Agent
    profile = AgentProfile(name=name, traits=traits, goal=goal)
    use_mock = st.session_state.get("use_mock", False)
    agent = Agent(profile, memory_stream, use_mock=use_mock)
    
    st.session_state.agents[name] = agent
    # st.success(f"Added agent: {name}")

def init_default_agents():
    """Initialize with 2 default agents if empty."""
    # Min-jun: Overly dramatic aspiring actor
    if "Min-jun" not in st.session_state.agents:
        add_agent(
            "Min-jun", 
            "Overly dramatic, emotional, speaks like he's in a Shakespeare play, easily offended", 
            "Get cast in a main role and impress Seo-yeon with his acting skills"
        )
    
    # Seo-yeon: Cynical scriptwriter
    if "Seo-yeon" not in st.session_state.agents:
        add_agent(
            "Seo-yeon", 
            "Cynical, dry humor, realistic, constantly tired, coffee addict", 
            "Finish her script deadline and dodge Min-jun's drama"
        )

# Auto-initialize handled in Sidebar after API Key check

# --- Simulation Logic ---
def run_simulation_step():
    agents = st.session_state.agents
    active_names = list(agents.keys())
    
    if len(active_names) < 1:
        return

    # Migration: Ensure all agents have coordinates (Handle old session state)
    for name, agent in agents.items():
        # Check if state is missing x (indicating old schema)
        if not hasattr(agent.state, 'x'):
            # Re-create state object using the current AgentState class definition
            # This works because 'from models import AgentState' should point to the updated class
            # after Streamlit reloads.
            old_data = agent.state.dict()
            # Pydantic ignore extra fields if not in new model? No, new model HAS x,y.
            # But old data doesn't. New model defaults x=10, y=10.
            # We just create a new instance with old data.
            agent.state = AgentState(**old_data)
            
            # Explicitly set defaults if missing (though Pydantic default=10 handles it)
            # Just separate safety check
            if not hasattr(agent.state, 'x'):
                st.error("Model reload failed. Please restart the app completely.")
                return
            
    # 1. Move All Agents
    agent_positions = []
    for name, agent in agents.items():
        # Skip if talking
        if agent.state.current_action == "TALKING":
            continue
            
        agent.state.current_action = "MOVING"
        agent.move()
        agent_positions.append({"name": name, "x": agent.state.x, "y": agent.state.y})
    
    # 2. Check Proximity (Who met whom?)
    # Simple check: If any two agents are close, they form a "Group" and talk.
    # For MVP, we just check if *anyone* is close to *anyone*.
    
    interacting_groups = []
    processed = set()
    
    for i, name_a in enumerate(active_names):
        if name_a in processed:
            continue
            
        group = [name_a]
        agent_a = agents[name_a]
        
        for name_b in active_names[i+1:]:
            if name_b in processed:
                continue
            
            agent_b = agents[name_b]
            dist = ((agent_a.state.x - agent_b.state.x)**2 + (agent_a.state.y - agent_b.state.y)**2)**0.5
            
            if dist <= config.INTERACTION_RADIUS:
                group.append(name_b)
                processed.add(name_b)
        
        if len(group) >= 2:
            interacting_groups.append(group)
            processed.add(name_a)

    # 3. Process Interactions
    if interacting_groups:
        for group in interacting_groups:
            # Mark as TALKING
            for name in group:
                agents[name].state.current_action = "TALKING"
            
            run_conversation_turn(group)
            
            # Return to IDLE after conversation
            for name in group:
                agents[name].state.current_action = "IDLE"
    else:
        # No interaction, just a quiet tick
        # Return everyone to IDLE
        for name in active_names:
            if agents[name].state.current_action != "TALKING":
                agents[name].state.current_action = "IDLE"

    # Increment global time regardless
    st.session_state.turn_idx += 1

def run_conversation_turn(active_agent_names):
    agents = st.session_state.agents
    
    # Context Assembly
    recent_dialogue = "\n".join([f"{t.speaker_name}: {t.utterance}" for t in st.session_state.transcript[-5:]])
    context = f"Situation: Agents {', '.join(active_agent_names)} met.\nRecent Log:\n{recent_dialogue}"
    
    # Localize Context: Only showing global log for MVP, but should ideally be local
    
    # Select Speaker just from this group
    last_speaker = st.session_state.transcript[-1].speaker_name if st.session_state.transcript else None
    next_speaker_name = st.session_state.selector.select_next_speaker(
        context, active_agent_names, last_speaker
    )
    
    if not next_speaker_name: return
    
    speaker_agent = agents[next_speaker_name]
    other_agents = [name for name in active_agent_names if name != next_speaker_name]
    
    # Run Step
    record = speaker_agent.run_step(context, other_agents)
    
    # Others Observe
    for name in other_agents:
        agents[name].observe(f"{next_speaker_name} said: {record.utterance}")
    
    st.session_state.transcript.append(record)


# --- Main Area ---
st.title("⚔️ Agent RPG Simulation")

# Top Controls
col_control, col_stat = st.columns([1, 3])
with col_control:
    auto_play = st.toggle("🔄 Auto Play", value=False)
    if st.button("▶️ Step Once"):
        run_simulation_step()
        st.rerun()

with col_stat:
    total_turns = st.session_state.turn_idx
    st.metric("Timeline (Turn)", f"{total_turns}")

# Auto Play Loop
if auto_play:
    import time
    run_simulation_step()
    time.sleep(1.0) # 1 sec delay
    st.rerun()

# --- Map Visualization ---
st.markdown("### 🗺️ World Map")

# Create DataFrame for Map
map_data = []
for name, agent in st.session_state.agents.items():
    # Fallback if x/y missing (though run_simulation_step should fix it, this protects the UI render)
    ax = getattr(agent.state, 'x', 10)
    ay = getattr(agent.state, 'y', 10)
    
    # State indicator
    state = getattr(agent.state, 'current_action', 'IDLE')
    state_emoji = {
        "IDLE": "💤",
        "MOVING": "🚶",
        "TALKING": "💬"
    }.get(state, "")
    
    map_data.append({
        "name": f"{name} {state_emoji}", 
        "x": ax, 
        "y": ay,
        "size": 100 # bubble size
    })
df_map = pd.DataFrame(map_data)

if not df_map.empty:
    st.scatter_chart(
        df_map, 
        x='x', 
        y='y', 
        size='size', 
        color='name',
        height=400
    )
else:
    st.info("No agents on the map.")

# --- Transcript & Timeline ---
# ... (Reusing existing Timeline logic below)


# --- Time Slider ---
if total_turns > 0:
    st.markdown("### ⏳ Time Travel")
    
    if total_turns > 1:
        selected_turn = st.slider(
            "Select Turn to Inspect", 
            min_value=1, 
            max_value=total_turns, 
            value=total_turns,
            step=1
        )
    else:
        st.info("Start of the timeline.")
        selected_turn = 1
    
    # Get record for the selected turn (index is turn-1)
    # Ensure index is within bounds (handle edge case where transcript might be empty or cleared)
    if st.session_state.transcript:
        record_idx = selected_turn - 1
        current_record = st.session_state.transcript[record_idx]
        
        st.divider()
        st.subheader(f"Turn {selected_turn}: {current_record.speaker_name}'s Action")
        
        col_main, col_debug = st.columns([3, 2])
        
        with col_main:
            # RPG Style Message
            st.markdown(f"""
            <div class="rpg-bubble">
                <div class="rpg-speaker">{current_record.speaker_name}</div>
                <div class="rpg-text">"{current_record.utterance}"</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show context leading up to this point?
            # For now, just the current turn action is focused.
            
        with col_debug:
            st.markdown(f"#### 🧠 {current_record.speaker_name}'s Brain")
            
            tab_mem, tab_plan, tab_score = st.tabs(["Memories", "Plan", "Scores"])
            
            with tab_mem:
                st.caption("Retrieved Memories for this turn:")
                for sm in current_record.retrieved_memories:
                     st.info(f"{sm.memory.content} (Imp: {sm.memory.importance})")
            
            with tab_plan:
                st.caption("Reflection & Plan")
                if current_record.reflection:
                    st.success(f"**Reflection:** {current_record.reflection}")
                st.warning(f"**Plan:** {current_record.plan}")
                
            with tab_score:
                st.caption("Detailed Scoring")
                score_data = []
                for sm in current_record.retrieved_memories:
                    score_data.append({
                        "Mem": sm.memory.content[:15] + "..",
                        "Fin": f"{sm.final_score:.2f}",
                        "Sim": f"{sm.similarity_score:.2f}",
                        "Rec": f"{sm.recency_score:.2f}",
                        "Imp": f"{sm.importance_score:.2f}"
                    })
                if score_data:
                    st.dataframe(pd.DataFrame(score_data))
    else:
        st.info("Start the simulation to see the timeline.")
else:
    st.info("Press 'Next Turn' to start the story.")
