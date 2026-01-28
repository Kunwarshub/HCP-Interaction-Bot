def classify_intent(is_active: bool) -> str:
    return "INSERT" if not is_active else "UPDATE"
