# src/api/main.py
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List
import uvicorn
from dotenv import load_dotenv
import os
import sys

# Add parent directory to import path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Local imports
from retriever import answer_query
from utils import summarize_contexts  # 👈 NEW: import summarizer

# Load environment variables
load_dotenv()

app = FastAPI(
    title="RAG Medical QA API",
    description="Retrieval-Augmented Generation for medical document queries",
    version="1.0.0"
)

# ----- Request & Response Schemas -----
class QueryRequest(BaseModel):
    query: str
    top_k: int | None = 5

class QueryResponse(BaseModel):
    answer: str
    contexts: List[str]


# ----- ROUTES -----
@app.get("/")
def root():
    """Root endpoint - API info"""
    return {"message": "RAG Medical QA API", "docs": "/docs"}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

# 👇 MAIN POST ENDPOINT
@app.post("/query", response_model=QueryResponse)
def query_route(req: QueryRequest):
    """
    Main query endpoint - uses the CODER model via retriever.py
    """
    try:
        result = answer_query(req.query, req.top_k)
        return QueryResponse(
            answer=result["answer"],
            contexts=result["contexts"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 👇 Optional fallback: handles evaluator calling "/" directly
@app.post("/", response_model=QueryResponse)
def fallback_root(req: QueryRequest):
    """Redirect POST / to /query for compatibility with evaluators"""
    return query_route(req)


# ----- RUN SERVER -----
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

