# src/agent/agents/alpha_generator_agent.py
from typing import Any, Dict, List
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from agent.state import State
from agent.prompts.alpha_prompts import ALPHA_SYSTEM_PROMPT, ALPHA_USER_PROMPT
import json


async def alpha_generator_agent(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Generate seed alpha factors based on the trading hypothesis."""

    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0.4)

    # Format prompt with hypothesis
    user_prompt = ALPHA_USER_PROMPT.format(hypothesis=state.hypothesis)

    # Generate alphas using standard format
    response = await llm.ainvoke(
        [
            {
                "role": "system",
                "content": ALPHA_SYSTEM_PROMPT
                + "\nRespond with a JSON array of alpha objects.",
            },
            {"role": "user", "content": user_prompt},
        ]
    )

    # Process the response text as JSON
    try:
        # Extract JSON array from response
        content = response.content
        json_start = content.find("[")
        json_end = content.rfind("]") + 1

        if json_start >= 0 and json_end > json_start:
            json_str = content[json_start:json_end]
            alphas = json.loads(json_str)
        else:
            # Fallback if JSON brackets not found
            alphas = json.loads(content)

        # Validate alphas have required fields
        validated_alphas = []
        for alpha in alphas:
            if "alphaID" in alpha and "expr" in alpha and "desc" in alpha:
                validated_alphas.append(alpha)

        return {"seed_alphas": validated_alphas}
    except Exception as e:
        print(f"Error parsing alphas: {str(e)}")
        print(f"Raw response: {response.content}")
        return {"seed_alphas": []}
