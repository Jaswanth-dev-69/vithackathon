import os
from tqdm import tqdm
from transformers import pipeline
import numpy as np

import faiss
from utils import load_and_split_pdfs

VECTOR_DIR = "src/vectorstore"
os.makedirs(VECTOR_DIR, exist_ok=True)

def ingest_dir(data_dir="data"):
    docs = load_and_split_pdfs(data_dir)
    print(f"\n📚 Total chunks: {len(docs)}")
    
    if len(docs) == 0:
        print("⚠️  No documents found! Please add PDF files to the data/ directory.")
        return

    # Use a pipeline as a high-level helper
    print("⚙️ Loading CODER biomedical model...")
    pipe = pipeline("feature-extraction", model="GanjinZero/coder_eng")
    
    print("⚙️ Generating embeddings with CODER model...")
    embeddings = []
    batch_size = 32

    for i in tqdm(range(0, len(docs), batch_size)):
        batch = docs[i:i + batch_size]
        # Get embeddings and average across tokens (mean pooling)
        batch_embeddings = pipe(batch)
        # Convert to numpy and apply mean pooling across sequence dimension
        batch_embeddings = [np.array(emb).mean(axis=0) for emb in batch_embeddings]
        embeddings.extend(batch_embeddings)
    
    embeddings = np.vstack(embeddings)

    print("💾 Saving FAISS index...")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, os.path.join(VECTOR_DIR, "faiss.index"))

    # save the text chunks for retrieval
    with open(os.path.join(VECTOR_DIR, "texts.txt"), "w") as f:
        for line in docs:
            f.write(line.replace("\n", " ") + "\n")

    print("✅ Ingestion complete!")

if __name__ == "__main__":
    ingest_dir("data/")
