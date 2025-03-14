"""
Backtest result database operations for AlphaGPT
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from agent.database.models.backtest_result import BacktestResult
from agent.database.models.alpha import Alpha
from agent.database.operations.db_connection import get_session_factory


def save_backtest_results(
    thread_id: str,
    checkpoint_id: str,
    state_values: Dict[str, Any],
    session: Optional[Session] = None
) -> List[BacktestResult]:
    """
    Save backtest results from the graph state to our database
    
    Args:
        thread_id: LangGraph thread ID
        checkpoint_id: LangGraph checkpoint ID
        state_values: The current state values with backtest results
        session: Optional SQLAlchemy session
        
    Returns:
        List of saved backtest result instances
    """
    saved_results = []
    
    if not state_values.get("sota_alphas"):
        return saved_results
    
    # Create session if needed
    session_factory = get_session_factory()
    session_provided = session is not None
    if not session_provided:
        session = session_factory()
    
    try:
        for sota_alpha in state_values["sota_alphas"]:
            if not sota_alpha.get("backtest_results"):
                continue
            
            # Find the alpha in the database
            alpha = (
                session.query(Alpha)
                .filter_by(thread_id=thread_id, alpha_id=sota_alpha.get("id"))
                .first()
            )
            
            if not alpha:
                continue
            
            # Create backtest result
            backtest_data = sota_alpha.get("backtest_results", {})
            
            result = BacktestResult(
                thread_id=thread_id,
                checkpoint_id=checkpoint_id,
                alpha_id=alpha.id,
                is_sota=True,
                information_ratio=float(backtest_data.get("information_ratio", 0)),
                annualized_return=float(backtest_data.get("annualized_return", 0)),
                max_drawdown=float(backtest_data.get("max_drawdown", 0)),
                ic=float(backtest_data.get("ic", 0)),
                backtest_data=backtest_data,
            )
            
            session.add(result)
            saved_results.append(result)
        
        if not session_provided and saved_results:
            session.commit()
        
        return saved_results
    
    finally:
        if not session_provided:
            session.close()


def get_backtest_results_for_alpha(alpha_id: int) -> List[Dict[str, Any]]:
    """
    Get all backtest results for a specific alpha
    
    Args:
        alpha_id: The alpha ID to query
        
    Returns:
        List of backtest result dictionaries
    """
    session_factory = get_session_factory()
    session = session_factory()
    
    try:
        results = session.query(BacktestResult).filter_by(alpha_id=alpha_id).all()
        
        return [
            {
                "id": r.id,
                "is_sota": r.is_sota,
                "information_ratio": r.information_ratio,
                "annualized_return": r.annualized_return,
                "max_drawdown": r.max_drawdown,
                "ic": r.ic,
                "backtest_data": r.backtest_data,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in results
        ]
    
    finally:
        session.close()
