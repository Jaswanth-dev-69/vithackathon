from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# === Load FAISS index and texts ===
INDEX_PATH = "src/vectorstore/faiss.index"
TEXTS_PATH = "src/vectorstore/texts.txt"

print("🧠 Loading FAISS index and model...")
index = faiss.read_index(INDEX_PATH)
with open(TEXTS_PATH, "r") as f:
    texts = f.readlines()

model = SentenceTransformer("all-MiniLM-L6-v2")

app = FastAPI(title="Local RAG System")

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class QueryResponse(BaseModel):
    answer: str
    contexts: List[str]

@app.post("/query", response_model=QueryResponse)
def query_route(req: QueryRequest):
    query_vec = model.encode([req.query], convert_to_numpy=True)
    D, I = index.search(query_vec, req.top_k)
    contexts = [texts[i].strip() for i in I[0] if i < len(texts)]

    # simple "answer" = top context summary
    answer = contexts[0] if contexts else "No relevant context found."

    return QueryResponse(answer=answer, contexts=contexts)
