from langgraph.graph import StateGraph
from agent.configuration import Configuration
from agent.state import State
from agent.nodes.user_input_node import user_input_node
from agent.nodes.knowledge_retrieval_node import knowledge_retrieval_node
from agent.nodes.generate_seed_alphas_node import generate_seed_alphas_node
from agent.nodes.thought_decompiler_node import thought_decompiler_node

# Define the graph workflow
workflow = StateGraph(State, config_schema=Configuration)

# Add nodes to the graph
workflow.add_node("user_input", user_input_node)
workflow.add_node("knowledge_retrieval", knowledge_retrieval_node)
workflow.add_node("generate_seed_alphas", generate_seed_alphas_node)
workflow.add_node("thought_decompiler", thought_decompiler_node)

# Connect the nodes
workflow.add_edge("__start__", "user_input")
workflow.add_edge("user_input", "knowledge_retrieval")
workflow.add_edge("knowledge_retrieval", "generate_seed_alphas")
workflow.add_edge("generate_seed_alphas", "thought_decompiler")

# Compile the graph
graph = workflow.compile()
graph.name = "Alpha Generation Workflow with RAG and Structured Output"
