# backend/rag/retriever.py
import os
import faiss
import numpy as np
import cohere
from fastembed import TextEmbedding
from rag.embedder import load_index

# Same model as the index was built with, run through ONNX instead of torch
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_CACHE = os.getenv(
    "FASTEMBED_CACHE",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fastembed_cache"),
)

_embedder = None

def get_query_embedder():
    global _embedder
    if _embedder is None:
        _embedder = TextEmbedding(model_name=MODEL_NAME, cache_dir=MODEL_CACHE)
    return _embedder

index, chunks = load_index()

def embed_query(query: str) -> np.ndarray:
    vec = np.array(list(get_query_embedder().embed([query])), dtype="float32")
    faiss.normalize_L2(vec)
    return vec

def retrieve(query: str, top_k: int = 10) -> list[dict]:
    """Retrieve top_k chunks using FAISS similarity search"""
    query_embedding = embed_query(query)
    scores, indices = index.search(query_embedding, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue
        chunk = chunks[idx].copy()
        chunk["score"] = float(score)
        results.append(chunk)
    return results

def rerank(query: str, retrieved: list[dict], top_n: int = 3) -> list[dict]:
    """Rerank retrieved chunks using Cohere reranker"""
    cohere_key = os.getenv("COHERE_API_KEY")

    if not cohere_key:
        # No Cohere key: just return top_n from FAISS
        print("No COHERE_API_KEY found, skipping reranking")
        return retrieved[:top_n]

    try:
        co = cohere.Client(cohere_key)
        texts = [r["text"] for r in retrieved]
        response = co.rerank(
            query=query,
            documents=texts,
            top_n=top_n,
            model="rerank-english-v3.0"
        )
        reranked = [retrieved[r.index] for r in response.results]
        return reranked
    except Exception as e:
        print(f"Reranking failed: {e}, falling back to FAISS order")
        return retrieved[:top_n]