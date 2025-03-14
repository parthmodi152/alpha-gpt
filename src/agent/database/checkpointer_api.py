"""
AlphaGPT Checkpointer API

This file serves as the main interface for the checkpointing system in AlphaGPT.
It provides a clean API for integrating with LangGraph and working with the database.
"""

import os
from typing import Dict, Any, List, Optional, Union

from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.checkpoint.base import BaseCheckpointSaver
from langchain_core.runnables import RunnableConfig

from agent.database.operations.db_connection import get_db_engine, create_tables
from agent.database.operations.hypothesis_operations import (
    save_hypothesis,
    get_hypothesis_history,
)
from agent.database.operations.alpha_operations import (
    save_alphas,
    get_alphas_for_hypothesis,
)
from agent.database.operations.backtest_operations import (
    save_backtest_results,
    get_backtest_results_for_alpha,
)

from agent.database.operations.db_connection import (
    get_db_url,
    get_db_connection_params,
)


class AlphaGPTCheckpointer:
    """
    Custom checkpointer for AlphaGPT that saves state data to both LangGraph checkpointer
    and our custom database tables for querying later.
    """

    def __init__(self, postgres_saver: Union[PostgresSaver, AsyncPostgresSaver] = None):
        """
        Initialize the AlphaGPT checkpointer with a PostgreSQL saver.

        Args:
            postgres_saver: The LangGraph PostgreSQL saver to use
        """
        self.postgres_saver = postgres_saver or self._create_postgres_saver()
        self.engine = get_db_engine()

        # Ensure tables exist
        create_tables(self.engine)

    def _create_postgres_saver(self) -> PostgresSaver:
        """Create a PostgresSaver instance for LangGraph"""
        # Get database URL from centralized function
        db_url = get_db_url()

        # Get individual parameters for error reporting
        db_params = get_db_connection_params()

        try:
            # Try newer LangGraph versions API
            return PostgresSaver.from_conn_string(db_url)
        except Exception as e:
            # Last resort fallback
            from langgraph.checkpoint.memory import MemorySaver

            print(
                f"Warning: Using MemorySaver as fallback - PostgreSQL connection failed: {str(e)}"
            )
            # Print detailed error info
            import traceback

            print(
                f"Connection details: host={db_params['host']}, port={db_params['port']}, "
                f"db={db_params['db']}, user={db_params['user']}"
            )
            print(f"Error details: {traceback.format_exc()}")

            return MemorySaver()

    def get_saver(self) -> BaseCheckpointSaver:
        """Return the underlying PostgreSQL saver for LangGraph"""
        return self.postgres_saver

    def save_state(self, config: RunnableConfig, state_values: Dict[str, Any]) -> None:
        """
        Save all state data to our custom database tables

        Args:
            config: LangGraph config
            state_values: The current state values
        """
        thread_id = config.get("configurable", {}).get("thread_id")
        checkpoint_id = config.get("configurable", {}).get("checkpoint_id")

        if not thread_id or not checkpoint_id:
            return

        # Save hypothesis first
        hypothesis = save_hypothesis(thread_id, checkpoint_id, state_values)

        # Save alphas if we have a hypothesis
        if hypothesis:
            save_alphas(thread_id, checkpoint_id, state_values, hypothesis.id)

        # Save backtest results
        save_backtest_results(thread_id, checkpoint_id, state_values)

    def get_hypothesis_history(self, thread_id: str) -> List[Dict[str, Any]]:
        """
        Get the history of hypotheses for a thread

        Args:
            thread_id: The thread ID to query

        Returns:
            List of hypothesis dictionaries
        """
        return get_hypothesis_history(thread_id)

    def get_alphas_for_hypothesis(self, hypothesis_id: int) -> List[Dict[str, Any]]:
        """
        Get all alphas for a specific hypothesis

        Args:
            hypothesis_id: The hypothesis ID to query

        Returns:
            List of alpha dictionaries
        """
        return get_alphas_for_hypothesis(hypothesis_id)

    def get_backtest_results_for_alpha(self, alpha_id: int) -> List[Dict[str, Any]]:
        """
        Get all backtest results for a specific alpha

        Args:
            alpha_id: The alpha ID to query

        Returns:
            List of backtest result dictionaries
        """
        return get_backtest_results_for_alpha(alpha_id)


def get_checkpoint_manager() -> AlphaGPTCheckpointer:
    """
    Create and return an AlphaGPT checkpointer instance.
    This manages both LangGraph checkpointing and our custom data storage.

    Returns:
        AlphaGPTCheckpointer instance
    """
    return AlphaGPTCheckpointer()
