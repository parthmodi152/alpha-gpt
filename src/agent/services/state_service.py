"""
State management service for AlphaGPT

This module provides functions for working with graph states and history.
"""

from typing import Dict, Any, Optional

from agent.state import State
from agent.database.checkpointer_api import get_checkpoint_manager

# Import graph lazily to avoid circular imports


def invoke_graph_with_state(
    initial_state: State,
    thread_id: Optional[str] = None,
    checkpoint_id: Optional[str] = None,
) -> State:
    """
    Invoke the graph with an initial state, optionally continuing from a thread

    Args:
        initial_state: The initial state to pass to the graph
        thread_id: Optional thread ID to continue from
        checkpoint_id: Optional checkpoint ID to continue from

    Returns:
        Final state from the graph execution
    """
    config_dict = {}

    if thread_id:
        config_dict["configurable"] = {"thread_id": thread_id}

        if checkpoint_id:
            config_dict["configurable"]["checkpoint_id"] = checkpoint_id

    # Avoid circular import by importing here
    from agent.graph import graph

    # Run the graph with the config
    return graph.invoke(initial_state, config_dict)


def get_state_history(thread_id: str) -> Dict[str, Any]:
    """
    Get the full history of a thread, including hypotheses, alphas, and backtest results

    Args:
        thread_id: Thread ID to get history for

    Returns:
        Dictionary containing thread history
    """
    checkpointer = get_checkpoint_manager()

    # Get all hypotheses for this thread
    hypotheses = checkpointer.get_hypothesis_history(thread_id)

    # Get alphas for each hypothesis
    for hypothesis in hypotheses:
        hypothesis["alphas"] = checkpointer.get_alphas_for_hypothesis(hypothesis["id"])

        # Get backtest results for each alpha
        for alpha in hypothesis["alphas"]:
            alpha["backtest_results"] = checkpointer.get_backtest_results_for_alpha(
                alpha["id"]
            )

    return {"thread_id": thread_id, "hypotheses": hypotheses}
