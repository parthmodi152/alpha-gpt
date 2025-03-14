"""
Hypothesis database operations for AlphaGPT
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from agent.database.models.hypothesis import Hypothesis
from agent.database.operations.db_connection import get_session_factory


def save_hypothesis(
    thread_id: str,
    checkpoint_id: str,
    state_values: Dict[str, Any],
    session: Optional[Session] = None
) -> Optional[Hypothesis]:
    """
    Save hypothesis data from the graph state to our database
    
    Args:
        thread_id: LangGraph thread ID
        checkpoint_id: LangGraph checkpoint ID
        state_values: The current state values
        session: Optional SQLAlchemy session
        
    Returns:
        Saved hypothesis instance or None if no hypothesis in state
    """
    if not state_values.get("hypothesis"):
        return None
    
    # Create session if needed
    session_factory = get_session_factory()
    session_provided = session is not None
    if not session_provided:
        session = session_factory()
    
    try:
        # Check if we already saved this checkpoint's hypothesis
        existing = (
            session.query(Hypothesis)
            .filter_by(thread_id=thread_id, checkpoint_id=checkpoint_id)
            .first()
        )
        
        if existing:
            return existing
        
        # Get the current iteration
        current_iteration = 0
        last_hypothesis = (
            session.query(Hypothesis)
            .filter_by(thread_id=thread_id)
            .order_by(Hypothesis.iteration.desc())
            .first()
        )
        
        if last_hypothesis:
            current_iteration = last_hypothesis.iteration + 1
        
        # Create new hypothesis record
        hypothesis = Hypothesis(
            thread_id=thread_id,
            checkpoint_id=checkpoint_id,
            trading_idea=state_values.get("trading_idea", ""),
            hypothesis=state_values.get("hypothesis", ""),
            reason=state_values.get("reason", ""),
            concise_reason=state_values.get("concise_reason", ""),
            concise_observation=state_values.get("concise_observation", ""),
            concise_justification=state_values.get("concise_justification", ""),
            concise_knowledge=state_values.get("concise_knowledge", ""),
            iteration=current_iteration,
        )
        
        session.add(hypothesis)
        
        if not session_provided:
            session.commit()
        
        return hypothesis
    
    finally:
        if not session_provided:
            session.close()


def get_hypothesis_history(thread_id: str) -> List[Dict[str, Any]]:
    """
    Get the history of hypotheses for a thread
    
    Args:
        thread_id: The thread ID to query
        
    Returns:
        List of hypothesis dictionaries
    """
    session_factory = get_session_factory()
    session = session_factory()
    
    try:
        hypotheses = (
            session.query(Hypothesis)
            .filter_by(thread_id=thread_id)
            .order_by(Hypothesis.iteration)
            .all()
        )
        
        return [
            {
                "id": h.id,
                "iteration": h.iteration,
                "trading_idea": h.trading_idea,
                "hypothesis": h.hypothesis,
                "reason": h.reason,
                "concise_reason": h.concise_reason,
                "concise_observation": h.concise_observation,
                "concise_justification": h.concise_justification,
                "concise_knowledge": h.concise_knowledge,
                "created_at": h.created_at.isoformat() if h.created_at else None,
            }
            for h in hypotheses
        ]
    
    finally:
        session.close()
