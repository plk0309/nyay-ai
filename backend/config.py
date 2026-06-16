# backend/config.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEGAL_DOCS_DIR = os.path.join(BASE_DIR, "..", "legal_docs")
FAISS_INDEX_DIR = os.path.join(BASE_DIR, "..", "faiss_index")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50