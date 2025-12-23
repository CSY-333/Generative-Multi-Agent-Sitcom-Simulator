"""
memory_stream.py
In-memory memory stream with optional Chroma persistence-like semantics.
"""
from __future__ import annotations

from collections import deque
from datetime import datetime
from typing import Deque, Iterable, List, Optional

from models import Memory
from scoring import importance_rule_score, score_memories


class MemoryStream:
    """Lightweight memory store honoring LRU retention and scoring rules."""

    def __init__(self, max_memories: int = 200) -> None:
        self.max_memories = max_memories
        self._memories: Deque[Memory] = deque()

    def add_memory(self, memory: Memory) -> None:
        if len(self._memories) >= self.max_memories:
            self._memories.popleft()
        self._memories.append(memory)

    def bulk_add(self, memories: Iterable[Memory]) -> None:
        for mem in memories:
            self.add_memory(mem)

    def retrieve(
        self,
        query: str,
        *,
        top_n: int = 20,
        k: int = 5,
        w_sim: float = 0.6,
        w_rec: float = 0.2,
        w_imp: float = 0.2,
    ):
        return score_memories(query, list(self._memories)[-top_n:], top_n=top_n, k=k, w_sim=w_sim, w_rec=w_rec, w_imp=w_imp)

    def importance_for_observation(self, text: str, goal_hint: Optional[str] = None) -> int:
        return importance_rule_score(text, goal_hint=goal_hint)

    @property
    def memories(self) -> List[Memory]:
        return list(self._memories)

    def __len__(self) -> int:  # pragma: no cover - trivial
        return len(self._memories)

    def __iter__(self):  # pragma: no cover - trivial
        return iter(self._memories)

    def last_updated(self) -> Optional[datetime]:
        if not self._memories:
            return None
        return self._memories[-1].created_at
