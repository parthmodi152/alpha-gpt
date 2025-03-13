# src/agent/graph.py
from langgraph.graph import StateGraph
from agent.configuration import Configuration
from agent.state import State
from agent.agents.user_input_agent import user_input_agent
from agent.agents.hypothesis_agent import hypothesis_agent
from agent.agents.alpha_generator_agent import alpha_generator_agent
from agent.agents.alpha_coder_agent import alpha_coder_agent

# Define the graph workflow
workflow = StateGraph(State, config_schema=Configuration)

# Add agents to the graph
workflow.add_node("user_input", user_input_agent)
workflow.add_node("hypothesis_generator", hypothesis_agent)
workflow.add_node("alpha_generator", alpha_generator_agent)
workflow.add_node("alpha_coder", alpha_coder_agent)

# Connect the agents
workflow.add_edge("__start__", "user_input")
workflow.add_edge("user_input", "hypothesis_generator")
workflow.add_edge("hypothesis_generator", "alpha_generator")
workflow.add_edge("alpha_generator", "alpha_coder")
workflow.add_edge("alpha_coder", "__end__")

# Compile the graph
graph = workflow.compile()
graph.name = "Alpha Generation and Coding Workflow"
