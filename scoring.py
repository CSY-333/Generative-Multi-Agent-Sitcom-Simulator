"""
scoring.py
Utility functions for scoring memories and computing recency/importance.
"""
from __future__ import annotations

import hashlib
import math
import re
from collections import Counter
from datetime import datetime
from typing import Iterable, List, Optional

from models import Memory, ScoredMemory


def _tokenize(text: str) -> Counter:
    tokens = re.findall(r"[\w']+", text.lower())
    return Counter(tokens)


def _cosine_similarity(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    intersection = set(a.keys()) & set(b.keys())
    numerator = sum(a[t] * b[t] for t in intersection)
    denom_a = math.sqrt(sum(v * v for v in a.values()))
    denom_b = math.sqrt(sum(v * v for v in b.values()))
    if denom_a == 0 or denom_b == 0:
        return 0.0
    return numerator / (denom_a * denom_b)


def importance_rule_score(text: str, goal_hint: Optional[str] = None) -> int:
    score = 3
    lowered = text.lower()
    if goal_hint and goal_hint.lower() in lowered:
        score += 2
    event_keywords = ["결정", "약속", "실수", "고백", "promise", "decision", "mistake", "confess"]
    emotion_keywords = ["화남", "기쁨", "불안", "angry", "happy", "anxious"]
    name_patterns = [r"\b님\b", r"\b씨\b"]
    if any(k.lower() in lowered for k in event_keywords):
        score += 2
    if any(k.lower() in lowered for k in emotion_keywords):
        score += 1
    if any(re.search(pattern, lowered) for pattern in name_patterns):
        score += 1
    return min(score, 10)


def recency_score(created_at: datetime, now: Optional[datetime] = None, tau_hours: float = 12.0) -> float:
    now = now or datetime.utcnow()
    age_hours = (now - created_at).total_seconds() / 3600
    return math.exp(-age_hours / tau_hours)


def importance_norm(importance: int) -> float:
    return max(0.0, min(1.0, (importance - 1) / 9))


def final_score(similarity: float, recency: float, importance: float, w_sim: float, w_rec: float, w_imp: float) -> float:
    return similarity * w_sim + recency * w_rec + importance * w_imp


def score_memories(
    query: str,
    memories: Iterable[Memory],
    top_n: int = 20,
    k: int = 5,
    w_sim: float = 0.6,
    w_rec: float = 0.2,
    w_imp: float = 0.2,
) -> List[ScoredMemory]:
    query_tokens = _tokenize(query)
    scored: List[ScoredMemory] = []
    for mem in memories:
        sim = _cosine_similarity(query_tokens, _tokenize(mem.content))
        rec = recency_score(mem.created_at)
        imp = importance_norm(mem.importance)
        scored.append(
            ScoredMemory(
                memory=mem,
                similarity=sim,
                recency_score=rec,
                importance_score=imp,
                final_score=final_score(sim, rec, imp, w_sim, w_rec, w_imp),
            )
        )
    scored.sort(key=lambda m: m.final_score, reverse=True)
    return scored[:k]


def cache_key(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
