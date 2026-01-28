from agents.state import InteractionState
from tools.intent_classifier import classify_intent

def intent(state: InteractionState):
    state['intent'] = classify_intent(state['is_active'])
    return state