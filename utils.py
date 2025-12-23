"""
utils.py
Helper utilities for deterministic text generation and formatting.
"""
from __future__ import annotations

import random
from datetime import datetime
from typing import Iterable


def seeded_choice(options: Iterable[str], seed: int) -> str:
    rng = random.Random(seed)
    options_list = list(options)
    if not options_list:
        return ""
    return rng.choice(options_list)


def timestamp() -> str:
    return datetime.utcnow().isoformat()
