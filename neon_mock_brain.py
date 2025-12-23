"""
Neon Society Mock Brain
Fallback rule-based logic when Gemini unavailable
"""
import random
from typing import Dict, Literal

# Template thoughts for different personality types
DRAMATIC_THOUGHTS = [
    "Ah, the tragedy of existence weighs upon me...",
    "Life is but a stage, and I am merely a player!",
    "The cosmos conspires against my noble pursuits!",
]

CYNICAL_THOUGHTS = [
    "Another tedious day in this simulation...",
    "Everyone here is predictably boring.",
    "I need more coffee to tolerate this.",
]

DEFAULT_THOUGHTS = [
    "I wonder what's happening around here.",
    "Maybe I should explore a bit.",
    "Just going with the flow.",
]

DRAMATIC_PLANS = [
    "Wander dramatically, pondering my destiny",
    "Seek out someone to regale with my tales",
    "Practice my theatrical gestures",
]

CYNICAL_PLANS = [
    "Find a quiet corner to avoid people",
    "Get more coffee if possible",
    "Minimal interaction strategy",
]

DEFAULT_PLANS = [
    "Walk around and see what happens",
    "Maybe talk to someone nearby",
    "Just explore the area",
]

def get_mock_decision(agent_name: str, traits: str, goal: str, 
                      position: tuple, nearby_agents: list) -> Dict:
    """
    Generate mock decision based on simple rules
    Returns: {"thought": str, "action": str, "plan": str}
    """
    # Select templates based on traits
    if "dramatic" in traits.lower() or "shakespeare" in traits.lower():
        thought = random.choice(DRAMATIC_THOUGHTS)
        plan = random.choice(DRAMATIC_PLANS)
    elif "cynical" in traits.lower() or "tired" in traits.lower():
        thought = random.choice(CYNICAL_THOUGHTS)
        plan = random.choice(CYNICAL_PLANS)
    else:
        thought = random.choice(DEFAULT_THOUGHTS)
        plan = random.choice(DEFAULT_PLANS)
    
    # Random walk with slight bias toward center
    x, y = position
    center = 10
    
    # Bias toward center
    if random.random() < 0.3:
        if x < center:
            action = "RIGHT"
        elif x > center:
            action = "LEFT"
        elif y < center:
            action = "DOWN"
        elif y > center:
            action = "UP"
        else:
            action = "STAY"
    else:
        # Random movement
        action = random.choice(["UP", "DOWN", "LEFT", "RIGHT", "STAY", "STAY"])
    
    return {
        "thought": thought,
        "action": action,
        "plan": plan
    }

def generate_mock_dialogue(agent1_name: str, agent1_traits: str,
                           agent2_name: str, agent2_traits: str) -> Dict:
    """
    Generate simple mock conversation
    Returns: {"dialogue": str, "summary": str}
    """
    # Simple template-based dialogue
    greetings = [
        f"{agent1_name}: 'Oh, hello there.'",
        f"{agent1_name}: 'Fancy meeting you here.'",
        f"{agent1_name}: 'Hey!'",
    ]
    
    responses = [
        f"{agent2_name}: 'Hi. How's it going?'",
        f"{agent2_name}: 'Yeah, what's up?'",
        f"{agent2_name}: 'Oh, hey.'",
    ]
    
    dialogue = f"{random.choice(greetings)}\n{random.choice(responses)}"
    summary = f"{agent1_name} and {agent2_name} had a brief chat."
    
    return {
        "dialogue": dialogue,
        "summary": summary
    }
