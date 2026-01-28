from agents.state import InteractionState
from tools.field_extraction import extract_fields

def extract_fields_node(state: InteractionState)->InteractionState:
    state['extracted_fields'] = extract_fields(state['user_message'])
    return state