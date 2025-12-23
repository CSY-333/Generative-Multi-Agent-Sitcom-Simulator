"""
scoring.py
Importance rules, recency calculation, final score aggregation.
"""
import math
from datetime import datetime
from models import Memory

# Keywords for importance scoring
IMPORTANT_KEYWORDS = {
    "event": ["결정", "약속", "실수", "고백", "비밀", "사건", "위기", "성공", "실패"],
    "emotion": ["화남", "기쁨", "불안", "행복", "슬픔", "우울", "놀람", "감동"],
    "relation": ["우리", "너", "나", "함께", "부탁", "도움"],
}

def calculate_importance_score(text: str) -> int:
    """
    Calculate rule-based importance score (1-10).
    """
    score = 3  # Base score
    
    for word in IMPORTANT_KEYWORDS["event"]:
        if word in text:
            score += 2
    
    for word in IMPORTANT_KEYWORDS["emotion"]:
        if word in text:
            score += 1
            
    for word in IMPORTANT_KEYWORDS["relation"]:
        if word in text:
            score += 1
            
    return min(10, max(1, score))

def calculate_recency_score(created_at: datetime, current_time: datetime, decay_factor: float = 0.99) -> float:
    """
    Calculate recency score using exponential decay.
    recency = decay_factor ^ (hours_passed)
    """
    delta = current_time - created_at
    hours_passed = delta.total_seconds() / 3600
    return math.pow(decay_factor, hours_passed)

def calculate_final_score(
    similarity: float,
    recency: float,
    importance: float,
    w_sim: float = 1.0,
    w_rec: float = 1.0,
    w_imp: float = 1.0
) -> float:
    """
    Calculate final retrieval score.
    importance is assumed to be 1-10, so we normalize it to 0-1.
    """
    importance_norm = (importance - 1) / 9
    
    # Simple weighted sum
    total_weight = w_sim + w_rec + w_imp
    if total_weight == 0:
        return 0.0
        
    return (w_sim * similarity + w_rec * recency + w_imp * importance_norm)
