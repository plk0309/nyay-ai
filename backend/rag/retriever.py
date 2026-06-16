# backend/rag/retriever.py
import faiss
import numpy as np
import cohere
import os
from sentence_transformers import SentenceTransformer
from rag.embedder import load_index
from config import EMBEDDING_MODEL

embedder = SentenceTransformer(EMBEDDING_MODEL)
index, chunks = load_index()

def retrieve(query: str, top_k: int = 10) -> list[dict]:
    """Retrieve top_k chunks using FAISS similarity search"""
    query_embedding = embedder.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(query_embedding)
    scores, indices = index.search(query_embedding, top_k)
    
    results = []
    for score, idx in zip(scores[0], indices[0]):
        chunk = chunks[idx].copy()
        chunk["score"] = float(score)
        results.append(chunk)
    return results

def rerank(query: str, retrieved: list[dict], top_n: int = 3) -> list[dict]:
    """Rerank retrieved chunks using Cohere reranker"""
    cohere_key = os.getenv("COHERE_API_KEY")
    
    if not cohere_key:
        # No Cohere key — just return top_n from FAISS
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