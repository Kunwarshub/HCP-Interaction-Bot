from langgraph.graph import StateGraph, END
from .state import InteractionState 

# import nodes
from agents.nodes.extracted_field_node import extract_fields_node
from agents.nodes.intent_node import intent
from agents.nodes.confidence_node import classify_fields
from agents.nodes.import_values import apply_patch_node
from agents.nodes.database_node import persist_confirmed_fields_node


graph = StateGraph(InteractionState)

graph.add_node("intent", intent)
graph.add_node("extract", extract_fields_node)
graph.add_node("confidence", classify_fields)
graph.add_node("apply_patch", apply_patch_node)
graph.add_node("persist", persist_confirmed_fields_node)

graph.set_entry_point("intent")

graph.add_edge("intent", "extract")
graph.add_edge("extract", "confidence")
graph.add_edge("confidence", "apply_patch")
graph.add_edge("apply_patch", "persist")
graph.add_edge("persist", END)

interaction_graph = graph.compile()