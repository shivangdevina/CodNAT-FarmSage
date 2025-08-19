from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4, UUID
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from rag_backend import rag_pipeline
from rag_backend import vectorstore
load_dotenv()
# -----------------------------
# Supabase connection
# -----------------------------
SUPABASE_URL ="https://pysflltbiyglnwyxdrkp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB5c2ZsbHRiaXlnbG53eXhkcmtwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTUxMjE4OSwiZXhwIjoyMDcxMDg4MTg5fQ.qO2bKg0qptka2CRYjLAKE7j5Aa_O2PdJxZrXI5hI-_c"
  # Use service role key for writes
print(SUPABASE_URL , SUPABASE_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------
# FastAPI app
# -----------------------------
app = FastAPI()

# Minimal CORS setup for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # set to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Models
# -----------------------------
class Message(BaseModel):
    sender: str  # "user" or "ai"
    text: str

# -----------------------------
# Endpoints
# -----------------------------

# Create a new chat
@app.post("/chats/new")
def create_chat():
    session_id = str(uuid4())
    return {"session_id": session_id}

# List all unique chats
@app.get("/chats")
def list_chats():
    response = supabase.table("chat_history").select("session_id").execute()
    sessions = list({row["session_id"] for row in response.data})  # unique sessions
    return {"chats": [{"session_id": sid} for sid in sessions]}

# Get full chat by session_id
@app.get("/chats/{session_id}")
def get_chat(session_id: UUID):
    response = supabase.table("chat_history").select("*").eq("session_id", str(session_id)).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Chat not found")

    messages = []
    for row in response.data:
        if row.get("user_query"):
            messages.append({"sender": "user", "text": row["user_query"]})
        if row.get("ai_answer"):
            messages.append({"sender": "ai", "text": row["ai_answer"]})

    return {"session_id": str(session_id), "messages": messages}

# Add a message and store user + AI reply
@app.post("/chats/{session_id}/message")
def add_message(session_id: UUID, user_message: Message):
    if user_message.sender != "user":
        raise HTTPException(status_code=400, detail="Only user can initiate message")

    # Save user message
    supabase.table("chat_history").insert({
        "session_id": str(session_id),
        "user_query": user_message.text,
        "ai_answer": None
    }).execute()

    # Generate AI reply (replace with your AI model later)
    result = rag_pipeline("hello", vectorstore=vectorstore , session_id=str(session_id), threshold=0.65)
    ai_response_text=result['answer']
    print("\n\nAi respone is " ,ai_response_text)

    # Save AI message
    supabase.table("chat_history").insert({
        "session_id": str(session_id),
        "user_query": None,
        "ai_answer": ai_response_text
    }).execute()

    return {"reply": {"sender": "ai", "text": ai_response_text}}
# ans=rag_pipeline("hello", vectorstore=vectorstore , session_id="8b700d42-261e-4d39-bd36-58c62d1bca7a", threshold=0.65)
# print("ans" , ans)

