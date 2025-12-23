"""
Neon Society Configuration
All constants in one place
"""

# World Settings
MAP_SIZE = 20  # 20x20 grid
PROXIMITY_RADIUS = 1.5  # Distance threshold for interaction

# Cognition Settings
THINK_INTERVAL = 8  # Ticks between deep LLM thoughts
MAX_MEMORIES = 20  # LRU memory cap

# Memory Scoring Weights
IMPORTANCE_WEIGHT = 0.5
RECENCY_WEIGHT = 0.5

# Default Importance Scores
CONVERSATION_IMPORTANCE = 7
SELF_OBSERVATION_IMPORTANCE = 4
ENVIRONMENT_IMPORTANCE = 2

# UI Settings
TICK_SPEED_MS = 1000  # Default tick interval in milliseconds
MAX_HISTORY_SIZE = 200  # DVR history cap (prevent memory overflow)

# Gemini/Mock Settings
USE_MOCK = True  # Toggle between Gemini and mock brain
GEMINI_MODEL = "gemini-pro"
GEMINI_TEMPERATURE = 0.7
