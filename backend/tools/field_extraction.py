import groq
import os
from dotenv import load_dotenv
import json, re

load_dotenv()

def extract_fields(user_message: str):

    client = groq.Client(api_key=os.getenv("FIELD_EXTRACTOR_KEY"))
    chat_completions = client.chat.completions.create(
        messages= [
            {
                "role": "system",
                "content": '''You are an AI assistant extracting structured fields from user messages
                about healthcare professional (HCP) interactions.

                Extract ONLY the fields explicitly mentioned by the user.
                Do not guess missing fields.
                Do not include none or null fields.
                You may extract ONLY the following fields.
                Each field has a fixed type and allowed values.

                Return STRICT JSON. Do not include fields not mentioned.
                Do NOT guess or hallucinate missing values.

                Schema:

                hcpName: string
                interaction_type: enum["Meeting","Call","Email","Virtual","Conference"]

                date: string (YYYY-MM-DD)
                time: string (HH:MM)
                attendees: array[string]

                topics_iscussed: string
                materials_shared: array[string]
                samples_distributed: array[string]

                outcome: string
                follow_up_actions: string

                sentiment: enum["Positive","Neutral","Negative"]

                complianceNotes: string
                flags: array[string]
                
                For each extracted field, give an estimate of overall confidence score between 0 and 1
                based on how clearly the user mentioned the information.


                If the user wants to delete any field, in the JSON do:
                "field": "delete"    

                Return JSON with field names as keys strictly in the exact format as below:
                "field" : {"value", "confidence"}
                '''
            },
            {
                "role": "user",
                "content": user_message,
            }
        ],
        model="llama-3.3-70b-versatile"
    )

    raw = chat_completions.choices[0].message.content.strip()

    print("🔴 RAW LLM OUTPUT START")
    print(raw)
    print("🔴 RAW LLM OUTPUT END")

    if raw.startswith("json"):
        raw = raw.strip("json")

    if raw.startswith("```"):
        raw = raw.strip("`")      # removes all backticks
        raw = raw.strip()

    print("🔴 RAW LLM OUTPUT START")
    print(raw)
    print("🔴 RAW LLM OUTPUT END")
    
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM did not return a valid Json: {raw}") from e
    
    return parsed