# src/agent/agents/alpha_coder_agent.py
from typing import Any, Dict, List
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from agent.state import State
from agent.prompts.alpha_coder_prompts import (
    ALPHA_CODER_SYSTEM_PROMPT,
    ALPHA_CODER_USER_PROMPT,
)


async def alpha_coder_agent(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Generate Python code for the seed alpha factors."""

    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0.1)

    # Process each alpha and generate code
    coded_alphas = []

    for alpha in state.seed_alphas:
        try:
            # Format prompt with alpha details
            user_prompt = ALPHA_CODER_USER_PROMPT.format(
                alpha_id=alpha["alphaID"],
                expression=alpha["expr"],
                description=alpha["desc"],
            )

            # Generate code
            response = await llm.ainvoke(
                [
                    {"role": "system", "content": ALPHA_CODER_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ]
            )

            # Extract code from the response
            content = response.content
            code_start = content.find("```python")
            code_end = content.rfind("```")

            if code_start >= 0 and code_end > code_start:
                code = content[code_start + 9 : code_end].strip()
            else:
                code = content

            # Add code to the alpha information
            coded_alpha = alpha.copy()
            coded_alpha["code"] = code
            coded_alphas.append(coded_alpha)

        except Exception as e:
            print(f"Error coding alpha {alpha.get('alphaID')}: {str(e)}")

    # Return coded alphas
    return {"coded_alphas": coded_alphas}
