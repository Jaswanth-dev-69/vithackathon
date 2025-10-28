#!/usr/bin/env python3
"""Quick test to verify CODER pipeline works correctly"""

from transformers import pipeline
import numpy as np

print("🧪 Testing CODER pipeline...")

# Use a pipeline as a high-level helper
pipe = pipeline("feature-extraction", model="GanjinZero/coder_eng")

# Test with a medical query
test_text = "What is Tdap booster?"
print(f"\n📝 Test text: {test_text}")

# Get embeddings
print("⚙️ Generating embedding...")
embedding = pipe(test_text)

# Convert to numpy and apply mean pooling
embedding_array = np.array(embedding[0])
print(f"📊 Raw shape: {embedding_array.shape}")

# Mean pooling across sequence dimension
pooled_embedding = embedding_array.mean(axis=0)
print(f"📊 Pooled shape: {pooled_embedding.shape}")
print(f"✅ Embedding dimension: {len(pooled_embedding)}")

print(f"\n✅ Pipeline test successful!")
print(f"Sample values: {pooled_embedding[:5]}")
