CONFIDENCE_THRESHOLD = 0.7

def confidence_gate_tool(extracted_fields: dict):
    confirmed_fields = {}
    pending_confirmation = {}

    for field, payload in extracted_fields.items():
        if payload["confidence"] >= CONFIDENCE_THRESHOLD:
            confirmed_fields[field] = payload
        else:
            pending_confirmation[field] = payload

    confirmed_fields = confirmed_fields
    pending_confirmation = pending_confirmation
    return confirmed_fields, pending_confirmation
