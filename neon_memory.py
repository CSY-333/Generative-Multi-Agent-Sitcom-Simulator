"""
Neon Society Memory Management
LRU + Importance-based retrieval
"""
from typing import List
from datetime import datetime
from neon_models import Memory
import neon_config as config

def add_memory(memories: List[Memory], new_memory: Memory) -> List[Memory]:
    """
    Add memory with LRU eviction if at capacity
    """
    # Add new memory
    memories.append(new_memory)
    
    # Enforce LRU cap
    if len(memories) > config.MAX_MEMORIES:
        # Sort by timestamp (oldest first)
        memories.sort(key=lambda m: m.timestamp)
        # Remove oldest
        memories.pop(0)
    
    return memories

def get_top_memories(memories: List[Memory], k: int = 5) -> List[Memory]:
    """
    Retrieve top-k memories by combined importance and recency
    """
    if not memories:
        return []
    
    now = datetime.now()
    
    # Score each memory
    scored = []
    for mem in memories:
        # Normalize importance (1-10 -> 0-1)
        importance_score = (mem.importance - 1) / 9.0
        
        # Recency score (exponential decay)
        age_seconds = (now - mem.timestamp).total_seconds()
        age_hours = age_seconds / 3600.0
        recency_score = max(0.0, 1.0 - (age_hours / 24.0))  # Decay over 24 hours
        
        # Combined score
        final_score = (
            importance_score * config.IMPORTANCE_WEIGHT +
            recency_score * config.RECENCY_WEIGHT
        )
        
        scored.append((mem, final_score))
    
    # Sort by score descending
    scored.sort(key=lambda x: x[1], reverse=True)
    
    # Return top-k
    return [mem for mem, score in scored[:k]]
