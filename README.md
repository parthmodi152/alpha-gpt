# Alpha-GPT: Human-AI Interactive Alpha Mining for Quantitative Investment

Alpha-GPT is an advanced Human-AI collaborative framework designed for **Quantitative Investment**. It leverages cutting-edge tools like **LangGraph**, **Zipline**, **Alphalens**, and **PyGAD** to generate, evaluate, and optimize financial trading strategies (alphas). 

---

## **Research Acknowledgments**
We are grateful for the foundational research papers that inspired and guided this project:

- [Alpha-GPT: Human-AI Interactive Alpha Mining for Quantitative Investment](https://arxiv.org/pdf/2308.00016)
- [Alpha-GPT 2.0: Human-in-the-Loop AI for Quantitative Investment](https://arxiv.org/pdf/2402.09746v1)

These papers have significantly influenced the system's development, especially in leveraging **Genetic Programming**, **LLM-guided Alpha Discovery**, and **Backtesting Pipelines**.

---

## **What It Does**
1. **Alpha Generation:** Custom alphas generated using symbolic expressions through **LangGraph Orchestration**.
2. **Evaluation and Backtesting:** Backtest performance using **Zipline** and evaluate factors with **Alphalens**.
3. **Genetic Programming:** Evolve optimal alphas using **PyGAD** through selection, mutation, and crossover.
4. **Data Pipeline Automation:** Modular design supports real-time updates and evaluations using LangGraph workflows.

---

## **How to Run**
1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   # Set up environment variables:
   cp .env.example .env  # Then add your OpenAI API key

2. **Run the Project:**
   ```bash
   python main.py
   ```
   This will:
   - Load the trading idea from user input
   - Generate seed alphas using GPT-4
   - Evaluate and backtest the alphas
   - Optimize using genetic programming
   - Output the best performing strategies
