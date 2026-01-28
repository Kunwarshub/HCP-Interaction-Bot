from sqlalchemy import text
from database.deps import get_db
from agents.state import InteractionState

def persist_confirmed_fields_node(state: InteractionState) -> InteractionState:
    confirmed = state.get("confirmed_fields", {})
    if not confirmed:
        return state

    db_gen = get_db()
    db = next(db_gen)

    try:
        if state["intent"] == "INSERT":
            db.execute(
                text("""
                    INSERT INTO hcp_interactions (
                        hcp_name,
                        interaction_type,
                        interaction_date,
                        interaction_time,
                        attendees,
                        topics_discussed,
                        materials_shared,
                        samples_distributed,
                        sentiment,
                        outcome,
                        follow_up_actions
                    ) VALUES (
                        :hcp_name,
                        :interaction_type,
                        :interaction_date,
                        :interaction_time,
                        :attendees,
                        :topics_discussed,
                        :materials_shared,
                        :samples_distributed,
                        :sentiment,
                        :outcome,
                        :follow_up_actions
                    )
                """),
                {
                    "hcp_name": state.get("hcpName"),
                    "interaction_type": state.get("interaction_type"),
                    "interaction_date": state.get("date"),
                    "interaction_time": state.get("time"),
                    "attendees": state.get("attendees"),
                    "topics_discussed": state.get("topics_discussed"),
                    "materials_shared": state.get("materials_shared"),
                    "samples_distributed": state.get("samples_distributed"),
                    "sentiment": state.get("sentiment"),
                    "outcome": state.get("outcome"),
                    "follow_up_actions": state.get("follow_up_actions"),
                }
            )

        else:  # UPDATE
            db.execute(
                text("""
                    UPDATE hcp_interactions
                    SET
                        hcp_name = :hcp_name,
                        interaction_type = :interaction_type,
                        interaction_date = :interaction_date,
                        interaction_time = :interaction_time,
                        attendees = :attendees,
                        topics_discussed = :topics_discussed,
                        materials_shared = :materials_shared,
                        samples_distributed = :samples_distributed,
                        sentiment = :sentiment,
                        outcome = :outcome,
                        follow_up_actions = :follow_up_actions
                    WHERE id = :interaction_id
                """),
                {
                    "hcp_name": state.get("hcpName"),
                    "interaction_type": state.get("interaction_type"),
                    "interaction_date": state.get("date"),
                    "interaction_time": state.get("time"),
                    "attendees": state.get("attendees"),
                    "topics_discussed": state.get("topics_discussed"),
                    "materials_shared": state.get("materials_shared"),
                    "samples_distributed": state.get("samples_distributed"),
                    "sentiment": state.get("sentiment"),
                    "outcome": state.get("outcome"),
                    "follow_up_actions": state.get("follow_up_actions"),
                    "interaction_id": state.get("interaction_id"),
                }
            )

        db.commit()

    finally:
        db.close()

    return state
