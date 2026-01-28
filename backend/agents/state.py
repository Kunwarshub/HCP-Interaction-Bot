from typing import TypedDict, Optional
from datetime import date, time

class InteractionState(TypedDict):
    user_message: str

    # flow control
    is_active: bool
    interaction_id: Optional[int]

    # LLM output (one-turn patch)
    extracted_fields: dict[str, dict]

    # accumulated local state (single source for DB + UI)
    hcpName: Optional[str]
    interaction_type: Optional[str]
    date: Optional[date]
    time: Optional[time]
    attendees: Optional[list[str]]
    topics_discussed: Optional[str]
    materials_shared: Optional[list[str]]
    samples_distributed: Optional[list[str]]
    sentiment: Optional[str]
    outcome: Optional[str]
    follow_up_actions: Optional[str]
    pending_confirmation: dict
    confirmed_fields: dict
    confirmation_question: str | None

    # control
    intent: Optional[str]
    errors: list[str]