# src/agent/agents/hypothesis_agent.py
from typing import Any, Dict
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from agent.state import State
from agent.prompts.hypothesis_prompts import (
    HYPOTHESIS_SYSTEM_PROMPT,
    HYPOTHESIS_USER_PROMPT,
)


async def hypothesis_agent(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Generate a detailed trading hypothesis from the trading idea."""

    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

    # Format prompt with trading idea
    user_prompt = HYPOTHESIS_USER_PROMPT.format(trading_idea=state.trading_idea)

    # Generate hypothesis
    response = await llm.ainvoke(
        [
            {"role": "system", "content": HYPOTHESIS_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]
    )

    # Return generated hypothesis
    return {"hypothesis": response.content}
