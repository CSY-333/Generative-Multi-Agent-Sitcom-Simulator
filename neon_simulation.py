"""
Neon Society Simulation Engine
Tick-based world simulation with proximity interactions
"""
import math
from typing import List, Tuple, Dict
from datetime import datetime

from neon_models import WorldState, AgentSnapshot, Memory, InteractionRecord
import neon_config as config
import neon_memory as memory_lib
import neon_mock_brain as mock_brain

def proximity_check(agent1: AgentSnapshot, agent2: AgentSnapshot) -> float:
    """Calculate Euclidean distance between two agents"""
    return math.sqrt((agent1.x - agent2.x)**2 + (agent1.y - agent2.y)**2)

def find_nearby_agents(world: WorldState, agent_name: str) -> List[str]:
    """Find all agents within proximity radius"""
    agent = world.agents[agent_name]
    nearby = []
    
    for other_name, other_agent in world.agents.items():
        if other_name == agent_name:
            continue
        
        distance = proximity_check(agent, other_agent)
        if distance <= config.PROXIMITY_RADIUS:
            nearby.append(other_name)
    
    return nearby

def detect_interaction_groups(world: WorldState) -> List[List[str]]:
    """
    Find groups of agents close enough to interact
    Returns list of groups (each group is list of agent names)
    """
    processed = set()
    groups = []
    
    agent_names = list(world.agents.keys())
    
    for name in agent_names:
        if name in processed:
            continue
        
        # Find all nearby agents
        nearby = find_nearby_agents(world, name)
        
        if nearby:
            # Form a group
            group = [name] + nearby
            groups.append(group)
            
            # Mark all as processed
            processed.add(name)
            for nearby_name in nearby:
                processed.add(nearby_name)
    
    return groups

def process_interaction(world: WorldState, group: List[str], use_mock: bool = True) -> InteractionRecord:
    """
    Generate conversation for a group of agents
    Currently supports pairs (first 2 agents)
    """
    # For MVP, handle pairs
    if len(group) < 2:
        return None
    
    agent1_name = group[0]
    agent2_name = group[1]
    
    agent1 = world.agents[agent1_name]
    agent2 = world.agents[agent2_name]
    
    # Mark as TALKING
    agent1.state = "TALKING"
    agent2.state = "TALKING"
    
    # Generate dialogue
    convo = None
    if not use_mock:
        # Try Gemini first
        import neon_gemini_service as gemini
        convo = gemini.generate_gemini_dialogue(
            agent1_name, agent1.traits,
            agent2_name, agent2.traits
        )
    
    # Fallback to mock
    if convo is None:
        convo = mock_brain.generate_mock_dialogue(
            agent1_name, agent1.traits,
            agent2_name, agent2.traits
        )
    
    # Add to both agents' memories
    memory1 = Memory(
        content=f"Conversation with {agent2_name}: {convo['summary']}",
        importance=config.CONVERSATION_IMPORTANCE,
        type="conversation"
    )
    
    memory2 = Memory(
        content=f"Conversation with {agent1_name}: {convo['summary']}",
        importance=config.CONVERSATION_IMPORTANCE,
        type="conversation"
    )
    
    agent1.memories = memory_lib.add_memory(agent1.memories, memory1)
    agent2.memories = memory_lib.add_memory(agent2.memories, memory2)
    
    # Create interaction record
    return InteractionRecord(
        tick=world.tick,
        participants=[agent1_name, agent2_name],
        dialogue=convo['dialogue'],
        summary=convo['summary']
    )

def process_agent_cognition(agent: AgentSnapshot, use_mock: bool = True) -> None:
    """
    Handle agent's thinking and movement
    Implements THINK_INTERVAL throttling
    """
    # Decrement think timer
    if agent.ticks_until_next_think > 0:
        agent.ticks_until_next_think -= 1
    
    # Time for deep thought?
    if agent.ticks_until_next_think <= 0:
        # Get decision from brain
        decision = None
        
        if not use_mock:
            # Try Gemini first
            import neon_gemini_service as gemini
            memories = [m.content for m in agent.memories]
            decision = gemini.get_gemini_decision(
                agent.name,
                agent.traits,
                agent.goal,
                (agent.x, agent.y),
                memories,
                []  # TODO: pass nearby agents
            )
        
        # Fallback to mock
        if decision is None:
            decision = mock_brain.get_mock_decision(
                agent.name,
                agent.traits,
                agent.goal,
                (agent.x, agent.y),
                []
            )
        
        # Update agent state
        agent.state = "THINKING"
        agent.current_thought = decision['thought']
        agent.current_plan = decision['plan']
        agent.cached_direction = decision['action']
        
        # Reset timer
        agent.ticks_until_next_think = config.THINK_INTERVAL
    
    # Execute movement (using cached direction)
    execute_movement(agent)

def execute_movement(agent: AgentSnapshot) -> None:
    """Move agent based on cached direction"""
    if agent.state == "TALKING":
        return  # Don't move while talking
    
    agent.state = "MOVING"
    
    direction = agent.cached_direction
    
    dx, dy = 0, 0
    if direction == "UP":
        dy = -1
    elif direction == "DOWN":
        dy = 1
    elif direction == "LEFT":
        dx = -1
    elif direction == "RIGHT":
        dx = 1
    # STAY = no movement
    
    # Apply movement with boundary checks
    new_x = max(0, min(config.MAP_SIZE, agent.x + dx))
    new_y = max(0, min(config.MAP_SIZE, agent.y + dy))
    
    agent.x = new_x
    agent.y = new_y

def tick(world: WorldState, use_mock: bool = True) -> WorldState:
    """
    Execute one simulation tick
    Returns updated world state
    """
    # Phase 1: Detect interactions
    interaction_groups = detect_interaction_groups(world)
    
    # Phase 2: Process interactions
    new_interactions = []
    interacting_agents = set()
    
    for group in interaction_groups:
        record = process_interaction(world, group, use_mock)
        if record:
            new_interactions.append(record)
            interacting_agents.update(group)
    
    # Phase 3: Process cognition & movement (for non-interacting agents)
    for agent_name, agent in world.agents.items():
        if agent_name not in interacting_agents:
            process_agent_cognition(agent, use_mock)
        else:
            # Return to IDLE after conversation
            agent.state = "IDLE"
    
    # Update world
    world.recent_interactions.extend(new_interactions)
    world.tick += 1
    
    return world
