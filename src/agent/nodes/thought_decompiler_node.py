from typing import Any, Dict
from langchain_core.runnables import RunnableConfig
from agent.state import State
from agent.utils.supported_indicators import SUPPORTED_INDICATORS
import sympy as sp


async def thought_decompiler_node(
    state: State, config: RunnableConfig
) -> Dict[str, Any]:
    """
    Validates and parses generated alphas into a structured format.
    """
    generated_alphas = state.generated_alphas.get("alphas", [])
    validated_alphas = []

    # Define variables
    VARIABLES = ["open", "close", "high", "low", "volume"]

    # Create symbols for variables
    symbols_dict = {var: sp.Symbol(var) for var in VARIABLES}

    # Combine locals for sympify
    locals_dict = {**SUPPORTED_INDICATORS, **symbols_dict}

    # Helper function to get function names
    def get_func_name(func):
        if hasattr(func.func, "name"):
            return func.func.name
        elif hasattr(func.func, "__name__"):
            return func.func.__name__
        elif isinstance(func.func, str):
            return func.func
        else:
            return str(func.func)

    for alpha in generated_alphas:
        try:
            # Extract alpha fields
            alpha_id = alpha.get("alphaID")
            raw_expr = alpha.get("expr")
            desc = alpha.get("desc")

            # Validate presence of required fields
            if not alpha_id or not raw_expr or not desc:
                raise ValueError(f"Alpha {alpha_id} is missing required fields.")

            # Validate expression using SymPy
            parsed_expr = sp.sympify(raw_expr, locals=locals_dict)

            # Extract variables, indicators, and operations
            variables = list(parsed_expr.free_symbols)
            indicators = [
                get_func_name(func)
                for func in parsed_expr.atoms(sp.Function)
                if get_func_name(func) in SUPPORTED_INDICATORS
            ]
            operations = [
                str(op) for op in parsed_expr.atoms(sp.Mul, sp.Add, sp.Pow, sp.Function)
            ]

            # Convert variables to strings
            variables = [str(var) for var in variables]

            # Build structured alpha
            structured_alpha = {
                "alphaID": alpha_id,
                "expr": raw_expr,  # Use raw expression for readability
                "desc": desc,
                "variables": variables,
                "indicators": indicators,
                "operations": operations,
            }

            validated_alphas.append(structured_alpha)

        except Exception as e:
            # Handle and log invalid alphas
            print(f"Error parsing alpha {alpha.get('alphaID')}: {e}")

    # Return validated and structured alphas
    return {"validated_alphas": validated_alphas}
