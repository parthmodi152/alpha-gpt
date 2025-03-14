# src/agent/state.py
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class State:
    """Define the state for alpha generation workflow with RD Agent style fields."""

    # Input/Output
    trading_idea: str = ""

    # Hypothesis fields (matching RD Agent structure)
    hypothesis: str = ""
    reason: str = ""
    concise_reason: str = ""
    concise_observation: str = ""
    concise_justification: str = ""
    concise_knowledge: str = ""

    # Alpha generation
    seed_alphas: List[Dict[str, Any]] = field(default_factory=list)
    coded_alphas: List[Dict[str, Any]] = field(default_factory=list)

    # For SOTA tracking and feedback loop
    sota_alphas: List[Dict[str, Any]] = field(default_factory=list)
    feedback: Optional[Dict[str, Any]] = None

    # Historical data for iterations
    hypothesis_history: List[Dict[str, Any]] = field(default_factory=list)
    alpha_history: List[Dict[str, Any]] = field(default_factory=list)
