def build_confirmation_question(pending_fields: dict) -> str:
    fields = ", ".join(pending_fields.keys())
    return (
        f"I’m not fully confident about the following fields: {fields}. "
        "Could you please clarify or rephrase them?"
    )
