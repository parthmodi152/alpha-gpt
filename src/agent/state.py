# src/agent/state.py
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class State:
    """Define the state for alpha generation workflow."""

    # Input/Output
    trading_idea: str = ""
    hypothesis: str = ""

    # Alpha generation
    seed_alphas: List[Dict[str, Any]] = field(default_factory=list)
    coded_alphas: List[Dict[str, Any]] = field(default_factory=list)

    # For future SOTA tracking
    sota_alphas: List[Dict[str, Any]] = field(default_factory=list)
    feedback: Optional[Dict[str, Any]] = None
