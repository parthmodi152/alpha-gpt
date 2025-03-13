# src/agent/agents/user_input_agent.py
from typing import Any, Dict
from langchain_core.runnables import RunnableConfig
from agent.state import State


async def user_input_agent(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Capture user trading idea input.

    In a real application, this would get input from the user.
    For demonstration, we'll use a predefined idea.
    """
    # This would normally come from user input
    # In a real app, this could be a web form, API endpoint, etc.
    return {
        "trading_idea": state.trading_idea
        or "Momentum-based strategy using volume and closing price"
    }
