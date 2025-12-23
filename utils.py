"""
utils.py
Helper functions for the project.
"""
import hashlib
from datetime import datetime
import numpy as np

def get_hash(text: str) -> str:
    """Returns SHA256 hash of the text."""
    return hashlib.sha256(text.encode()).hexdigest()

def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    if not v1 or not v2:
        return 0.0
    vec1 = np.array(v1)
    vec2 = np.array(v2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(np.dot(vec1, vec2) / (norm1 * norm2))

def normalize_score(score: float, min_val: float, max_val: float) -> float:
    """Normalize a score to 0-1 range."""
    if max_val == min_val:
        return 0.0
    return (score - min_val) / (max_val - min_val)
