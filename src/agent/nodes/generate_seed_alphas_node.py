from typing import Any, Dict
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from agent.state import State
from agent.utils.supported_indicators import SUPPORTED_INDICATORS


async def generate_seed_alphas_node(
    state: State, config: RunnableConfig
) -> Dict[str, Any]:
    """Generate 10 unique seed alphas in a structured JSON format."""
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    # Define the structured output schema
    alpha_schema = [
        {
            "alphaID": "alpha1",
            "expr": "log(close / open)",
            "desc": "Measures the logarithmic price change from open to close.",
        }
    ]

    structured_llm = llm.with_structured_output(alpha_schema, method="json_mode")

    # Supported Indicators List
    supported_indicators_text = ", ".join(SUPPORTED_INDICATORS.keys())

    # Prompt
    prompt = """
You are a quantitative researcher specialized in creating novel alpha expressions for financial trading strategies.

Based on the trading idea '{trading_idea}' and the examples provided below, generate 10 unique trading alphas in the following structured JSON format:

[
    {{
        "alphaID": "alpha1",
        "expr": "[mathematical expression]",
        "desc": "[concise explanation of the alpha, its logic, and how it relates to the given trading idea]"
    }},
    {{
        "alphaID": "alpha2",
        "expr": "[mathematical expression]",
        "desc": "[concise explanation of the alpha, its logic, and how it relates to the given trading idea]"
    }},
    ...
    {{
        "alphaID": "alpha10",
        "expr": "[mathematical expression]",
        "desc": "[concise explanation of the alpha, its logic, and how it relates to the given trading idea]"
    }}
]

Examples:
{examples}

Guidelines:
1. Use only the following supported indicators: '{supported_indicators}'.
2. Ensure all expressions are unique and provide financial intuition relevant to the given trading idea.
3. Keep descriptions concise but informative, explaining the financial logic behind each alpha.
4. Avoid duplication of the examples provided.
5. Ensure expressions are syntactically correct and ready for validation.

Provide the output as a JSON array containing exactly 10 alphas.
"""

    # Generate alphas based on the trading idea
    query = prompt.format(
        trading_idea=state.trading_idea,
        supported_indicators=supported_indicators_text,
        examples=state.retrieved_examples,
    )
    alphas = structured_llm.invoke(query)

    # Return the generated alphas
    return {"generated_alphas": alphas}
