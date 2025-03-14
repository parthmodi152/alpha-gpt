# src/agent/agents/alpha_generator_agent.py
from typing import Any, Dict, List, Optional
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from agent.state import State
from agent.prompts.alpha_prompts import (
    ALPHA_SYSTEM_PROMPT,
    ALPHA_INITIAL_PROMPT,
    ALPHA_ITERATION_PROMPT,
    ALPHA_OUTPUT_FORMAT,
)
import json


async def alpha_generator_agent(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Generate alpha factors based on the trading hypothesis.

    Following RD Agent's approach, this agent:
    1. Takes a hypothesis as input
    2. Generates mathematically formulated alpha factors
    3. Provides descriptions and variable definitions
    4. Returns factors in a structured JSON format
    """

    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0.4)

    # Determine if this is the first iteration or a refinement
    is_first_iteration = not state.sota_alphas or len(state.sota_alphas) == 0

    # Default to 5 factors for first iteration, 3 for subsequent ones
    num_factors = 5 if is_first_iteration else 3

    # Prepare prompt based on iteration state
    if is_first_iteration:
        user_prompt = ALPHA_INITIAL_PROMPT.format(
            hypothesis=state.hypothesis,
            num_factors=num_factors,
            output_format=ALPHA_OUTPUT_FORMAT,
        )
    else:
        # Format history from previous factors and their performance
        # Would be expanded with real performance data in full implementation
        factor_history = "Previous factors:\n"

        for i, alpha in enumerate(state.sota_alphas):
            factor_history += f"{i+1}. {alpha.get('name', 'Unnamed factor')}: "
            factor_history += f"{alpha.get('description', 'No description')}\n"
            if "performance" in alpha:
                factor_history += f"   Performance: {alpha['performance']}\n"

        user_prompt = ALPHA_ITERATION_PROMPT.format(
            hypothesis=state.hypothesis,
            factor_history=factor_history,
            num_factors=num_factors,
            output_format=ALPHA_OUTPUT_FORMAT,
        )

    # Generate alpha factors
    try:
        response = await llm.ainvoke(
            [
                {"role": "system", "content": ALPHA_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ]
        )

        # Parse JSON response
        content = response.content

        # Extract JSON if embedded in text
        json_start = content.find("{")
        json_end = content.rfind("}") + 1

        if json_start >= 0 and json_end > json_start:
            json_str = content[json_start:json_end]
            factors_dict = json.loads(json_str)
        else:
            # Fallback if JSON brackets not cleanly found
            factors_dict = json.loads(content)

        # Convert to seed_alphas format
        seed_alphas = []
        for factor_name, factor_data in factors_dict.items():
            seed_alphas.append(
                {
                    "alphaID": factor_name,
                    "expr": factor_data["formulation"],
                    "desc": factor_data["description"],
                    "variables": factor_data["variables"],
                }
            )

        return {"seed_alphas": seed_alphas}

    except Exception as e:
        print(f"Error generating alpha factors: {str(e)}")
        print(
            f"Raw response: {response.content if 'response' in locals() else 'No response'}"
        )

        # Return empty list to avoid breaking the flow
        return {"seed_alphas": []}
