import os
import faiss
from typing import List, Dict
from transformers import pipeline
import numpy as np
from dotenv import load_dotenv
from utils import summarize_contexts

load_dotenv()

# Load FAISS index and texts
INDEX_PATH = "src/vectorstore/faiss.index"
TEXTS_PATH = "src/vectorstore/texts.txt"

print("🧠 Loading FAISS index and CODER model...")
index = faiss.read_index(INDEX_PATH)

with open(TEXTS_PATH, "r") as f:
    texts = [line.strip() for line in f.readlines()]

# Use a pipeline as a high-level helper
pipe = pipeline("feature-extraction", model="GanjinZero/coder_eng")
print("✅ CODER model and index loaded successfully!")


def encode_query(query: str) -> np.ndarray:
    """Encode a query using CODER model pipeline"""
    # Get embeddings and average across tokens (mean pooling)
    embedding = pipe(query)
    # Convert to numpy and apply mean pooling across sequence dimension
    query_vec = np.array(embedding[0]).mean(axis=0, keepdims=True)
    return query_vec


def answer_query(query: str, top_k: int = 5) -> Dict[str, any]:
    """
    Answer a query using the RAG system.
    
    Args:
        query: The user's question
        top_k: Number of relevant contexts to retrieve
        
    Returns:
        Dictionary containing the answer and contexts
    """
    # Encode the query
    query_vec = encode_query(query)
    
    # Search the index
    D, I = index.search(query_vec, top_k)
    
    # Get the relevant contexts
    contexts = [texts[i] for i in I[0] if i < len(texts)]
    
    # Generate a summarized answer from the contexts
    answer = summarize_contexts(contexts, query) if contexts else "No relevant context found."
    
    return {
        "answer": answer,
        "contexts": contexts
    }
