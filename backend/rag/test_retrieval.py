# backend/rag/test_retrieval.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from rag.embedder import load_index
from config import EMBEDDING_MODEL

def test_retrieval(query: str, top_k: int = 5):
    print(f"\nQuery: {query}")
    print("-" * 40)

    model = SentenceTransformer(EMBEDDING_MODEL)
    index, chunks = load_index()

    query_embedding = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(query_embedding)

    scores, indices = index.search(query_embedding, top_k)

    for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
        chunk = chunks[idx]
        print(f"\nResult {i+1} (score: {score:.4f})")
        print(f"  Source: {chunk['metadata']['source']}")
        print(f"  Category: {chunk['metadata']['category']}")
        print(f"  Page: {chunk['metadata']['page']}")
        print(f"  Text: {chunk['text'][:200]}...")

if __name__ == "__main__":
    # Test with different types of queries
    test_queries = [
        "what are my rights as a tenant",
        "how to file RTI application",
        "consumer complaint against company",
        "minimum wages for workers",
        "POCSO act child protection"
    ]

    for query in test_queries:
        test_retrieval(query)
        print("\n" + "=" * 50)