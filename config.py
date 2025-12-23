"""
config.py
Configuration constants (weights, parameters).
"""
import os

# Model Settings
DEFAULT_MODEL_NAME = "gpt-3.5-turbo"
DEFAULT_TEMPERATURE = 0.7

# Memory Settings
TOP_N_RETRIEVAL = 20  # Fetch 20 from Vector DB
K_FINAL_RETRIEVAL = 5  # Return top 5 after reranking

# Scoring Weights
WEIGHT_SIMILARITY = 1.0
WEIGHT_RECENCY = 0.5
WEIGHT_IMPORTANCE = 1.0

# Decay Factor for Recency
DECAY_FACTOR = 0.995

# Reflection
REFLECTION_PERIOD = 5  # Reflect every 5 turns

# Paths
CHROMA_PERSIST_DIR = os.path.join(os.getcwd(), "storage", "chroma")

# Map Settings
MAP_SIZE = 20  # 20x20 grid
INTERACTION_RADIUS = 2  # Agents interact if distance <= 2

# Neon Society Settings
THINK_INTERVAL = 8  # Ticks between deep LLM thoughts
MAX_MEMORIES = 20  # LRU memory cap
