from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# import your graph + tools
from agents.graph import interaction_graph
from tools.connect_frontend import state_to_form_payload

app = FastAPI()

# CORS (frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# request schema
class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(req: ChatRequest):
    # 1. build initial state
    initial_state = {
        "user_message": req.message,
        "is_active": False,
        "interaction_id": None,
        "extracted_fields": {},
        "confirmed_fields": {},
        "pending_confirmation": {},
        "confirmation_question": None,
        "errors": [],
    }

    # 2. run langgraph
    final_state = interaction_graph.invoke(initial_state)

    # 3. prepare frontend-safe response
    return {
        "form_data": state_to_form_payload(final_state),
        "confirmation_question": final_state.get("confirmation_question"),
    }
