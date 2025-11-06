import os
from PyPDF2 import PdfReader
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def pdf_to_text(path: str) -> str:
    """Extract text from a PDF file."""
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def load_and_split_pdfs(data_dir: str):
    """Load all PDFs from a folder and split into chunks."""
    all_docs = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    for file in os.listdir(data_dir):
        if file.endswith(".pdf"):
            print(f"📄 Loading {file}...")
            text = pdf_to_text(os.path.join(data_dir, file))
            chunks = splitter.split_text(text)
            print(f"➡️ {len(chunks)} chunks created from {file}")
            all_docs.extend(chunks)
    return all_docs


# 👇 ADD THIS NEW FUNCTION BELOW
def summarize_contexts(contexts, query):
    """
    Create a short, query-focused summary from retrieved contexts.
    This is a lightweight offline heuristic (no external model).
    """
    if not contexts:
        return "No relevant information found."

    # Join all retrieved texts
    joined = " ".join(contexts)

    # Limit total text to avoid overflow
    if len(joined) > 800:
        joined = joined[:800]

    # Split into sentences
    sentences = joined.split(". ")

    # Keep sentences that mention query keywords
    query_words = query.lower().split()
    relevant = [s for s in sentences if any(q in s.lower() for q in query_words)]

    # Build concise summary (2–3 sentences max)
    summary = ". ".join(relevant[:3])

    # Fallback if nothing matched
    if not summary:
        summary = ". ".join(sentences[:2])

    return summary.strip()
