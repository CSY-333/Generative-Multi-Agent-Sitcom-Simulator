"""
speaker_selector.py
Utility class that decides which agent should speak next.
"""
from __future__ import annotations

import random
from typing import List, Optional


class SpeakerSelector:
    """
    Simple selector that currently supports two strategies:
    - round_robin (default)
    - random
    """

    def __init__(self, strategy: str = "round_robin", seed: Optional[int] = None) -> None:
        self.strategy = strategy
        self._rng = random.Random(seed)
        self._last_index = -1

    def select_next_speaker(
        self,
        context: str,
        agent_names: List[str],
        last_speaker: Optional[str] = None,
    ) -> Optional[str]:
        """
        Determine who should speak next based on the configured strategy.
        """
        if not agent_names:
            return None

        if self.strategy == "round_robin":
            return self._select_round_robin(agent_names, last_speaker)

        return self._select_random(agent_names, last_speaker)

    def _select_round_robin(
        self,
        agent_names: List[str],
        last_speaker: Optional[str],
    ) -> str:
        # Prefer continuing from the last speaker we know about.
        if last_speaker in agent_names:
            next_idx = (agent_names.index(last_speaker) + 1) % len(agent_names)
        else:
            # Fall back to our internal pointer to keep turns fair even after resets.
            next_idx = (self._last_index + 1) % len(agent_names)

        chosen = agent_names[next_idx]
        self._last_index = agent_names.index(chosen)
        return chosen

    def _select_random(
        self,
        agent_names: List[str],
        last_speaker: Optional[str],
    ) -> str:
        # Avoid picking the same speaker twice in a row if possible.
        candidates = [name for name in agent_names if name != last_speaker] or agent_names
        return self._rng.choice(candidates)
