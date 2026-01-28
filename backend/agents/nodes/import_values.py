from agents.state import InteractionState


def apply_patch_node(state: InteractionState) -> InteractionState:
    for field, payload in state["confirmed_fields"].items():
        if payload['value'] == "delete":
            state[field] = None
        else:
            state[field] = payload['value']
    return state
