"""
Alpha factor database operations for AlphaGPT
"""
from typing import Dict, Any, List, Optional
import uuid
from sqlalchemy.orm import Session

from agent.database.models.alpha import Alpha
from agent.database.operations.db_connection import get_session_factory


def save_alphas(
    thread_id: str,
    checkpoint_id: str,
    state_values: Dict[str, Any],
    hypothesis_id: int,
    session: Optional[Session] = None
) -> List[Alpha]:
    """
    Save alpha data from the graph state to our database
    
    Args:
        thread_id: LangGraph thread ID
        checkpoint_id: LangGraph checkpoint ID
        state_values: The current state values
        hypothesis_id: ID of the hypothesis these alphas belong to
        session: Optional SQLAlchemy session
        
    Returns:
        List of saved alpha instances
    """
    saved_alphas = []
    
    if not state_values.get("seed_alphas") and not state_values.get("coded_alphas"):
        return saved_alphas
    
    # Create session if needed
    session_factory = get_session_factory()
    session_provided = session is not None
    if not session_provided:
        session = session_factory()
    
    try:
        # Save seed alphas
        if state_values.get("seed_alphas"):
            for alpha_data in state_values["seed_alphas"]:
                # Check if we already saved this alpha
                alpha_id = alpha_data.get("id", str(uuid.uuid4()))
                existing = (
                    session.query(Alpha)
                    .filter_by(
                        hypothesis_id=hypothesis_id,
                        alpha_id=alpha_id,
                    )
                    .first()
                )
                
                if not existing:
                    alpha = Alpha(
                        thread_id=thread_id,
                        checkpoint_id=checkpoint_id,
                        hypothesis_id=hypothesis_id,
                        alpha_id=alpha_id,
                        expression=alpha_data.get("expression", ""),
                        description=alpha_data.get("description", ""),
                        code=alpha_data.get("code", ""),
                    )
                    session.add(alpha)
                    saved_alphas.append(alpha)
        
        # Save coded alphas
        if state_values.get("coded_alphas"):
            for alpha_data in state_values["coded_alphas"]:
                # Check if we already saved this alpha
                alpha_id = alpha_data.get("id", str(uuid.uuid4()))
                existing = (
                    session.query(Alpha)
                    .filter_by(
                        hypothesis_id=hypothesis_id,
                        alpha_id=alpha_id,
                    )
                    .first()
                )
                
                if not existing:
                    alpha = Alpha(
                        thread_id=thread_id,
                        checkpoint_id=checkpoint_id,
                        hypothesis_id=hypothesis_id,
                        alpha_id=alpha_id,
                        expression=alpha_data.get("expression", ""),
                        description=alpha_data.get("description", ""),
                        code=alpha_data.get("code", ""),
                    )
                    session.add(alpha)
                    saved_alphas.append(alpha)
        
        if not session_provided and saved_alphas:
            session.commit()
        
        return saved_alphas
    
    finally:
        if not session_provided:
            session.close()


def get_alphas_for_hypothesis(hypothesis_id: int) -> List[Dict[str, Any]]:
    """
    Get all alphas for a specific hypothesis
    
    Args:
        hypothesis_id: The hypothesis ID to query
        
    Returns:
        List of alpha dictionaries
    """
    session_factory = get_session_factory()
    session = session_factory()
    
    try:
        alphas = session.query(Alpha).filter_by(hypothesis_id=hypothesis_id).all()
        
        return [
            {
                "id": a.id,
                "alpha_id": a.alpha_id,
                "expression": a.expression,
                "description": a.description,
                "code": a.code,
                "created_at": a.created_at.isoformat() if a.created_at else None,
            }
            for a in alphas
        ]
    
    finally:
        session.close()
