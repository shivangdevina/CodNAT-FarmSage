
CodNAT_Farm_Sage
RAG Chatbot API
This project implements a Retrieval-Augmented Generation (RAG) powered chatbot with a FastAPI backend.
It allows users to ask domain-specific questions (e.g., agriculture, research documents, or any dataset you index) and get AI-generated answers grounded in uploaded documents.

🚀 Features
FastAPI Backend with REST endpoints for chat sessions and queries
Retrieval-Augmented Generation (RAG) pipeline for context-aware answers
Vector Indexing from local documents (./data) with configurable chunk size & overlap
Supabase Integration for persistent chat history storage
CORS Enabled for frontend integration
📂 Project Structure
├── rag_pipeline.ipynb # Notebook implementing RAG pipeline (build_index, ask) ├── main.py # FastAPI app with endpoints └── data/ # Folder to place your documents for indexing

⚙ Tech Stack
FastAPI – backend framework
Supabase – database for chat history
LangChain / Chroma / Embeddings – powering RAG (in rag_pipeline.ipynb)
Python-dotenv – environment variable management
UUID – session management for chats
🔑 API Endpoints
Chat Management
POST /chats/new → create a new chat session
GET /chats → list all unique chat sessions
GET /chats/{session_id} → fetch chat history for a session
Indexing
POST /index → build/rebuild vector index from ./data
Params: collection_name, chunk_size, overlap
Messaging
POST /chats/{session_id}/message → add a user message and get AI response
Example request:

{
  "sender": "user",
  "text": "What are the best practices for sustainable farming?"
}
Response:

{
  "reply": {
    "sender": "ai",
    "text": "Here are some sustainable farming practices..."
  }
}
1. Clone the repo
git clone https://github.com/yourusername/your-repo.git
cd your-repo

2. Install dependencies
pip install -r requirements.txt

3. Set up environment variables

Create a .env file with:

SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_role_key

4. Run FastAPI
uvicorn main:app --reload
