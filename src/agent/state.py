"""Define the state structures for the agent."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List


@dataclass
class State:
    """Defines the input state for the agent."""

    trading_idea: str = ""
    retrieved_examples: List[str] = None
    generated_alphas: dict = None
    validated_alphas: dict = None
