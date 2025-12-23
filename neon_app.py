"""
Neon Society - Streamlit UI
Game-like RPG interface with DVR time travel
"""
import streamlit as st
import pandas as pd
import time
from typing import List

from neon_models import WorldState, AgentSnapshot, Memory
import neon_simulation as sim
import neon_config as config

# Page config
st.set_page_config(
    page_title="Neon Society",
    page_icon="🌆",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0a0e27;
        color: #e0e0e0;
    }
    
    .agent-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d1b4e 100%);
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #00d9ff;
        margin: 10px 0;
        box-shadow: 0 0 20px rgba(0, 217, 255, 0.3);
    }
    
    .stat-box {
        background-color: #1a1a2e;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #f72585;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'world' not in st.session_state:
    # Create initial world with default agents
    world = WorldState()
    
    # Add Min-jun
    world.agents["Min-jun"] = AgentSnapshot(
        name="Min-jun",
        x=5, y=5,
        traits="Overly dramatic, speaks like Shakespeare",
        goal="Become the star of the show",
        cached_direction="RIGHT"  # Start moving
    )
    
    # Add Seo-yeon
    world.agents["Seo-yeon"] = AgentSnapshot(
        name="Seo-yeon",
        x=15, y=15,
        traits="Cynical writer, tired, coffee addict",
        goal="Finish script and avoid drama",
        cached_direction="LEFT"  # Start moving
    )
    
    st.session_state.world = world
    st.session_state.history = []  # DVR history
    st.session_state.is_playing = False
    st.session_state.dvr_mode = False
    st.session_state.use_mock = True  # Default to mock mode
    st.session_state.gemini_configured = False

# Sidebar for configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    
    # Mode selector
    mode = st.radio(
        "Brain Mode",
        ["🎭 Mock (Free)", "🧠 Gemini (API Required)"],
        index=0 if st.session_state.use_mock else 1
    )
    
    st.session_state.use_mock = (mode == "🎭 Mock (Free)")
    
    # API Key input (only show if Gemini mode)
    if not st.session_state.use_mock:
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Get your key from https://makersuite.google.com/app/apikey"
        )
        
        if api_key and not st.session_state.gemini_configured:
            import neon_gemini_service as gemini
            if gemini.configure_gemini(api_key):
                st.session_state.gemini_configured = True
                st.success("✅ Gemini configured!")
            else:
                st.error("❌ Failed to configure Gemini. Check your key or install: pip install google-generativeai")
        
        if not st.session_state.gemini_configured and not api_key:
            st.warning("⚠️ Enter API key to use Gemini mode")
    else:
        st.info("💡 Mock mode uses rule-based logic (no API needed)")
    
    st.divider()

# Header
st.title("🌆 Neon Society: Generative Agent RPG")

# Control Panel
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("▶️ Play" if not st.session_state.is_playing else "⏸️ Pause"):
        st.session_state.is_playing = not st.session_state.is_playing

with col2:
    if st.button("⏭️ Single Tick"):
        # Save snapshot to history
        snapshot = st.session_state.world.copy_snapshot()
        st.session_state.history.append(snapshot)
        
        # Advance simulation
        st.session_state.world = sim.tick(st.session_state.world, st.session_state.use_mock)
        st.rerun()

with col3:
    dvr_toggle = st.toggle("🎬 DVR Mode", value=st.session_state.dvr_mode)
    st.session_state.dvr_mode = dvr_toggle

with col4:
    st.metric("Tick", st.session_state.world.tick)
    if st.session_state.is_playing:
        st.success("🟢 Running")
    else:
        st.info("⏸️ Paused")

# Auto-play loop
if st.session_state.is_playing and not st.session_state.dvr_mode:
    # Save snapshot
    snapshot = st.session_state.world.copy_snapshot()
    st.session_state.history.append(snapshot)
    
    # Advance
    st.session_state.world = sim.tick(st.session_state.world, st.session_state.use_mock)
    
    time.sleep(config.TICK_SPEED_MS / 1000.0)
    st.rerun()

# DVR Timeline
if st.session_state.dvr_mode and st.session_state.history:
    st.markdown("### ⏪ Time Travel")
    
    selected_tick = st.slider(
        "Select Tick",
        min_value=0,
        max_value=len(st.session_state.history) - 1,
        value=len(st.session_state.history) - 1
    )
    
    # Load historical state
    st.session_state.world = st.session_state.history[selected_tick]
    st.info(f"Viewing Tick #{st.session_state.world.tick}")

# Main Display
col_map, col_agents = st.columns([2, 1])

with col_map:
    st.markdown("### 🗺️ World Map")
    
    # Use advanced neon visualization
    import neon_visualization as viz
    viz.render_neon_world_map(
        agents=st.session_state.world.agents,
        map_size=20,
        dvr_mode=st.session_state.dvr_mode,
        selected_agent=None,  # TODO: add selection
        cell_size=30
    )

with col_agents:
    st.markdown("### 👥 Agents")
    
    for name, agent in st.session_state.world.agents.items():
        with st.expander(f"🧙 {name}", expanded=True):
            st.markdown(f"**State:** {agent.state}")
            st.markdown(f"**Position:** ({agent.x}, {agent.y})")
            st.markdown(f"**Goal:** {agent.goal}")
            
            if agent.current_thought:
                st.info(f"💭 {agent.current_thought}")
            
            if agent.current_plan:
                st.success(f"📋 {agent.current_plan}")
            
            # Memory count
            st.caption(f"Memories: {len(agent.memories)}/{config.MAX_MEMORIES}")

# Recent Interactions
if st.session_state.world.recent_interactions:
    st.markdown("### 💬 Recent Conversations")
    
    for interaction in st.session_state.world.recent_interactions[-5:]:
        st.markdown(f"**Tick {interaction.tick}:** {', '.join(interaction.participants)}")
        st.code(interaction.dialogue)
        st.caption(interaction.summary)
        st.divider()
