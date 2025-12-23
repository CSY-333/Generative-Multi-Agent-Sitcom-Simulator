"""
Neon Society Gemini Service
Structured JSON output for agent cognition
"""
import os
import json
from typing import Dict, List, Optional

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

import neon_config as config

def configure_gemini(api_key: str) -> bool:
    """
    Configure Gemini API with provided key
    Returns True if successful
    """
    if not GEMINI_AVAILABLE:
        return False
    
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        print(f"Gemini configuration error: {e}")
        return False

def get_gemini_decision(agent_name: str, traits: str, goal: str,
                        position: tuple, memories: List[str],
                        nearby_agents: List[str]) -> Optional[Dict]:
    """
    Get agent decision from Gemini with structured JSON output
    Returns: {"thought": str, "action": str, "plan": str} or None if error
    """
    if not GEMINI_AVAILABLE:
        return None
    
    # Build context
    memory_text = "\n".join([f"- {mem}" for mem in memories[-5:]])  # Last 5 memories
    nearby_text = ", ".join(nearby_agents) if nearby_agents else "No one nearby"
    
    prompt = f"""You are {agent_name}, a character in a simulation.

YOUR PERSONALITY:
{traits}

YOUR GOAL:
{goal}

CURRENT SITUATION:
- Position: ({position[0]}, {position[1]}) on a 20x20 grid
- Nearby agents: {nearby_text}

RECENT MEMORIES:
{memory_text if memory_text else "- No memories yet"}

Based on this, decide your next action. Respond ONLY with valid JSON in this exact format:
{{
  "thought": "your internal monologue (1 sentence)",
  "action": "UP or DOWN or LEFT or RIGHT or STAY",
  "plan": "your short-term plan (1 sentence)"
}}

Remember:
- "thought" should reflect your personality
- "action" must be exactly one of: UP, DOWN, LEFT, RIGHT, STAY
- "plan" should align with your goal"""

    try:
        model = genai.GenerativeModel(config.GEMINI_MODEL)
        
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": config.GEMINI_TEMPERATURE,
                "response_mime_type": "application/json"
            }
        )
        
        # Parse JSON response
        result = json.loads(response.text)
        
        # Validate fields
        if "thought" not in result or "action" not in result or "plan" not in result:
            return None
        
        # Validate action
        if result["action"] not in ["UP", "DOWN", "LEFT", "RIGHT", "STAY"]:
            result["action"] = "STAY"
        
        return result
        
    except Exception as e:
        print(f"Gemini API error: {e}")
        return None

def generate_gemini_dialogue(agent1_name: str, agent1_traits: str,
                             agent2_name: str, agent2_traits: str) -> Optional[Dict]:
    """
    Generate conversation between two agents using Gemini
    Returns: {"dialogue": str, "summary": str} or None if error
    """
    if not GEMINI_AVAILABLE:
        return None
    
    prompt = f"""Generate a brief sitcom-style conversation between two characters who just met:

CHARACTER 1: {agent1_name}
Personality: {agent1_traits}

CHARACTER 2: {agent2_name}
Personality: {agent2_traits}

Create a short, witty exchange (2-3 lines each). Respond ONLY with valid JSON:
{{
  "dialogue": "Character1: 'line'\\nCharacter2: 'line'\\n...",
  "summary": "brief summary of what happened (1 sentence)"
}}"""

    try:
        model = genai.GenerativeModel(config.GEMINI_MODEL)
        
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.8,
                "response_mime_type": "application/json"
            }
        )
        
        result = json.loads(response.text)
        
        if "dialogue" not in result or "summary" not in result:
            return None
        
        return result
        
    except Exception as e:
        print(f"Gemini dialogue error: {e}")
        return None
