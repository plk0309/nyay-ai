# backend/rag/embedder.py
import faiss
import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from config import EMBEDDING_MODEL, FAISS_INDEX_DIR

# Absolute path to faiss_index at repo root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAISS_DIR = os.path.join(BASE_DIR, "faiss_index")

def get_embedder():
    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    return SentenceTransformer(EMBEDDING_MODEL)

def build_and_save_index(chunks: list[dict]):
    """Generate embeddings and save FAISS index"""
    os.makedirs(FAISS_DIR, exist_ok=True)

    model = get_embedder()
    texts = [chunk["text"] for chunk in chunks]

    print(f"\nGenerating embeddings for {len(texts)} chunks...")
    embeddings = model.encode(
        texts,
        batch_size=64,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    # Normalize for cosine similarity
    faiss.normalize_L2(embeddings)

    # Build FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # Inner Product = cosine after normalization
    index.add(embeddings)

    # Save index
    index_path = os.path.join(FAISS_DIR, "legal.index")
    chunks_path = os.path.join(FAISS_DIR, "chunks.pkl")
    stats_path = os.path.join(FAISS_DIR, "stats.json")

    faiss.write_index(index, index_path)

    with open(chunks_path, "wb") as f:
        pickle.dump(chunks, f)

    # Save stats for reference
    import json
    categories = {}
    for chunk in chunks:
        cat = chunk["metadata"]["category"]
        categories[cat] = categories.get(cat, 0) + 1

    stats = {
        "total_chunks": len(chunks),
        "embedding_dim": dimension,
        "model": EMBEDDING_MODEL,
        "chunks_per_category": categories
    }
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)

    print(f"\nIndex saved to {index_path}")
    print(f"Chunks saved to {chunks_path}")
    print(f"\nStats:")
    print(f"  Total chunks: {len(chunks)}")
    print(f"  Embedding dim: {dimension}")
    print(f"  Chunks per category: {categories}")

def load_index():
    """Load saved FAISS index and chunks"""
    index_path = os.path.join(FAISS_DIR, "legal.index")
    chunks_path = os.path.join(FAISS_DIR, "chunks.pkl")

    if not os.path.exists(index_path):
        raise FileNotFoundError(f"FAISS index not found at {index_path}. Run index_builder.py first.")

    index = faiss.read_index(index_path)
    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)

    print(f"Index loaded: {index.ntotal} vectors")
    return index, chunks