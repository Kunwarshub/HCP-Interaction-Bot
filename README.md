# HCP Interaction Log

An AI-assisted system to log Healthcare Professional (HCP) interactions using a conversational chat interface.  
Users describe interactions in natural language, and the system automatically extracts, validates, and logs structured data into a read-only form.

This project was built as an internship assignment and focuses on **AI orchestration, state management, and backend–frontend integration**, rather than UI-heavy design.

---

## ✨ Key Features

- Conversational chat interface for logging HCP interactions
- Read-only structured form auto-filled by AI
- Incremental updates (PATCH-style, no data loss)
- Confidence-based field validation with follow-up questions
- Backend-driven single source of truth
- Clean separation between tools, nodes, and orchestration logic

---

## 🧠 Architecture Overview

### Frontend
- **React (Vite)**
- Stateless UI for form display
- Chat-driven interaction
- Incremental form updates (merge-based state updates)

### Backend
- **FastAPI**
- **LangGraph** for AI workflow orchestration
- **Groq LLM (Gemma2-9B-IT)** for extraction and reasoning
- **PostgreSQL** for persistence

---

## 🔁 AI Flow (LangGraph)

1. User sends a chat message
2. LangGraph pipeline runs:
   - Intent classification (insert / update)
   - Field extraction (LLM tool)
   - Confidence gating
   - Confirmation question generation (if needed)
   - Patch application to local state
   - Database persistence
3. Backend returns **only confirmed fields from the current turn**
4. Frontend merges updates into existing form state

---


---

## 🚀 Running the Project Locally

### 1️⃣ Backend


cd backend
pip install -r requirements.txt
uvicorn main:app --reload

### 2️⃣ Frontend

cd frontend
npm install
npm run dev


🧪 Example Interaction

User input:

Met Dr. Sarah Thompson at City General Hospital on Jan 12 around 2:30 PM. We discussed Product X’s efficacy and she requested follow-up materials.