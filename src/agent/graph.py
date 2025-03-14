# src/agent/graph.py
import os

from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver


from agent.state import State
from agent.agents.user_input_agent import user_input_agent
from agent.agents.hypothesis_agent import hypothesis_agent
from agent.agents.alpha_generator_agent import alpha_generator_agent
from agent.agents.alpha_coder_agent import alpha_coder_agent
from agent.database.checkpointer_api import get_checkpoint_manager


def create_graph():
    """Create and configure the LangGraph workflow."""

    # Define the graph workflow
    workflow = StateGraph(State)

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

    # Configure checkpointing
    use_postgres = os.environ.get("USE_POSTGRES_CHECKPOINT", "true").lower() == "true"

    if use_postgres:
        # Use PostgreSQL checkpointer
        checkpointer = get_checkpoint_manager()
        # Create the graph with checkpointing
        graph = workflow.compile(checkpointer=checkpointer)
    else:
        # Fallback to memory checkpointer for development
        checkpointer = None
        graph = workflow.compile(checkpointer=MemorySaver())

    graph.name = "Alpha Generation and Coding Workflow"
    return graph


# Create the graph
graph = create_graph()
