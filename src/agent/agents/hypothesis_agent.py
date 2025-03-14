# src/agent/agents/hypothesis_agent.py
from typing import Any, Dict
import json

from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI

from agent.state import State
from agent.prompts.hypothesis_prompts import (
    HYPOTHESIS_SYSTEM_PROMPT,
    HYPOTHESIS_INITIAL_PROMPT,
    HYPOTHESIS_ITERATION_PROMPT,
    HYPOTHESIS_OUTPUT_FORMAT,
)
from agent.database.checkpointer_api import get_checkpoint_manager


async def hypothesis_agent(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Generate or refine a trading hypothesis."""

    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

    # Get checkpoint manager
    checkpointer = get_checkpoint_manager()

    # Get latest hypothesis history from checkpointer
    thread_id = config.get("configurable", {}).get("thread_id", "default")
    hypothesis_history = checkpointer.get_hypothesis_history(thread_id)

    # Determine if this is the first hypothesis or an iteration
    is_first_iteration = not hypothesis_history

    # Prepare prompt based on iteration state
    if is_first_iteration:
        user_prompt = HYPOTHESIS_INITIAL_PROMPT.format(
            trading_idea=state.trading_idea, output_format=HYPOTHESIS_OUTPUT_FORMAT
        )
        iteration = 1
    else:
        # Get the latest hypothesis from history
        latest_hypothesis = hypothesis_history[0] if hypothesis_history else None

        # Get alpha data and backtest results if available
        alpha_data = None
        backtest_data = None

        if latest_hypothesis and latest_hypothesis.get("id"):
            # Get alphas for this hypothesis
            alphas = checkpointer.get_alphas_for_hypothesis(latest_hypothesis["id"])
            if alphas:
                # Get the first alpha
                alpha_data = alphas[0]
                # Get backtest results for this alpha
                if alpha_data and alpha_data.get("id"):
                    backtest_data = checkpointer.get_backtest_results_for_alpha(
                        alpha_data["id"]
                    )

        # Format history for prompt
        formatted_history = "Previous Trading Hypothesis:\n"

        if latest_hypothesis:
            formatted_history += (
                f"Hypothesis: {latest_hypothesis.get('hypothesis', 'N/A')}\n"
            )
            formatted_history += (
                f"Explanation: {latest_hypothesis.get('explanation', 'N/A')}\n"
            )

        if alpha_data:
            formatted_history += (
                f"\nAlpha Expression: {alpha_data.get('expression', 'N/A')}\n"
            )
            formatted_history += (
                f"Alpha Description: {alpha_data.get('description', 'N/A')}\n"
            )

        if backtest_data:
            formatted_history += "\nPerformance Metrics:\n"
            for result in backtest_data:
                ir = result.get("information_ratio", "N/A")
                annualized_return = result.get("annualized_return", "N/A")
                max_drawdown = result.get("max_drawdown", "N/A")
                ic = result.get("ic", "N/A")
                formatted_history += f"Information Ratio: {ir}\n"
                formatted_history += f"Annualized Return: {annualized_return}\n"
                formatted_history += f"Max Drawdown: {max_drawdown}\n"
                formatted_history += f"IC: {ic}\n"

        user_prompt = HYPOTHESIS_ITERATION_PROMPT.format(
            hypothesis_history=formatted_history,
            output_format=HYPOTHESIS_OUTPUT_FORMAT,
        )
        iteration = len(hypothesis_history) + 1

    # Generate hypothesis
    response = await llm.ainvoke(
        [
            {"role": "system", "content": HYPOTHESIS_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]
    )

    # Parse JSON response
    content = response.content
    json_start = content.find("{")
    json_end = content.rfind("}") + 1

    if json_start >= 0 and json_end > json_start:
        json_str = content[json_start:json_end]
        hypothesis_data = json.loads(json_str)
    else:
        hypothesis_data = json.loads(content)

    # Add trading idea and iteration info
    hypothesis_data["trading_idea"] = state.trading_idea
    hypothesis_data["iteration"] = iteration

    # The hypothesis is saved automatically via the checkpointer
    # The checkpoint callback in graph.py will handle saving to the database
    # We don't need to explicitly save it here as the checkpointer captures the state

    return hypothesis_data
