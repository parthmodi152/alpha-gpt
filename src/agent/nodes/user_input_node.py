from typing import Any, Dict
from langchain_core.runnables import RunnableConfig
from agent.state import State


async def user_input_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Capture user input."""
    return {"trading_idea": "Momentum-based strategy using volume and closing price"}
