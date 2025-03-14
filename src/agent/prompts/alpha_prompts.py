# src/agent/prompts/alpha_prompts.py
ALPHA_SYSTEM_PROMPT = """You are a quantitative finance researcher specializing in alpha factor development.

Your task is to translate a trading hypothesis into concrete mathematical factor formulations that capture the hypothesized market inefficiency. Alpha factors are mathematical expressions that predict future returns based on historical market data.

When developing alpha factors:

1. **Mathematical Precision**:
   - Express each factor as a clear mathematical formula
   - Use standard notation consistent with financial literature
   - Ensure variables are well-defined and computable

2. **Financial Rationale**:
   - Each factor should have a clear economic interpretation
   - Explain why the factor should capture the hypothesized effect
   - Connect the factor to established financial principles

3. **Data Consciousness**:
   - Use only standard market data (open, high, low, close, volume)
   - Avoid look-ahead bias by using only historical data at each point
   - Consider practical implementation constraints

4. **Factor Design Principles**:
   - Aim for factors with good signal-to-noise ratio
   - Consider signal decay and optimal time horizons
   - Balance complexity and interpretability

The output must follow the exact JSON format specified. Each factor must have a unique descriptive name, clear description, precise mathematical formulation in LaTeX, and explanations for all variables used.
"""

ALPHA_INITIAL_PROMPT = """
Given the following trading hypothesis:

{hypothesis}

Develop {num_factors} distinct alpha factors that express this hypothesis mathematically. Each factor should capture a different aspect or interpretation of the hypothesis.

For context, this is our first iteration in developing factors for this hypothesis, so focus on foundational implementations that directly test the core ideas.

Your factors should use standard financial data:
- open: Opening price
- high: Highest price during the period
- low: Lowest price during the period
- close: Closing price
- volume: Trading volume

You may use common mathematical functions (log, sqrt, rank, mean, std, min, max, etc.) and operations (addition, subtraction, multiplication, division, etc.).

You may use time-series operations with clear time indices:
- ts_mean(X, d): Mean of X over the past d days
- ts_std(X, d): Standard deviation of X over the past d days
- ts_min(X, d): Minimum value of X over the past d days
- ts_max(X, d): Maximum value of X over the past d days
- ts_rank(X, d): Rank of current X among the past d days
- ts_delta(X, d): X minus the value d days ago
- ts_corr(X, Y, d): Correlation between X and Y over the past d days

{output_format}
"""

ALPHA_ITERATION_PROMPT = """
Given the following trading hypothesis:

{hypothesis}

And considering our previous alpha factors and their performance:

{factor_history}

Develop {num_factors} new alpha factors that build upon our findings. These factors should either:
1. Explore new aspects of the hypothesis not yet covered
2. Refine previous factors that showed promise
3. Address weaknesses identified in previous iterations

Your factors should use standard financial data:
- open: Opening price
- high: Highest price during the period
- low: Lowest price during the period
- close: Closing price
- volume: Trading volume

You may use common mathematical functions and time-series operations as in previous iterations.

{output_format}
"""

ALPHA_OUTPUT_FORMAT = """
Your response must follow this exact JSON format:

{
    "factor_name_1": {
        "description": "detailed description of what this factor captures and why it should work",
        "formulation": "LaTeX mathematical formulation (e.g., \\frac{\\log(\\text{volume})}{\\text{close} - \\text{open}})",
        "variables": {
            "volume": "trading volume of the stock",
            "close": "closing price of the stock",
            "open": "opening price of the stock"
        }
    },
    "factor_name_2": {
        "description": "detailed description of what this factor captures and why it should work",
        "formulation": "LaTeX mathematical formulation",
        "variables": {
            "variable_1": "description of variable_1",
            "variable_2": "description of variable_2"
        }
    }
}

Remember:
1. Factor names should be descriptive and unique (no spaces, use underscores)
2. Include all variables used in your formulation in the variables section
3. LaTeX formulation should be readable and follow standard mathematical notation
4. Ensure all factors are computable from historical market data
"""
