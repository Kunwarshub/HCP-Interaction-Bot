def state_to_form_payload(state) -> dict:
    payload = {}

    for field, meta in state["confirmed_fields"].items():
        payload[field] = meta["value"]

    return payload
