from agents.state import InteractionState
from tools.confidence_gate import confidence_gate_tool
from tools.confirm_question import build_confirmation_question

def classify_fields(state: InteractionState):

    confirmed, pending = confidence_gate_tool(state['extracted_fields'])
    state['confirmed_fields'], state['pending_confirmation'] = confirmed, pending

    if pending:
        state['confirmation_question'] = build_confirmation_question(pending)
    
    return state
