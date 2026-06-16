# backend/rag/index_builder.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.loader import load_all_documents
from rag.chunker import chunk_documents
from rag.embedder import build_and_save_index

def main():
    print("=" * 50)
    print("NYAY AI — Building Legal Document Index")
    print("=" * 50)

    # Step 1: Load all PDFs
    print("\n[1/3] Loading documents...")
    pages = load_all_documents()

    if not pages:
        print("ERROR: No pages loaded. Check your legal_docs directory path.")
        return

    # Step 2: Chunk documents
    print("\n[2/3] Chunking documents...")
    chunks = chunk_documents(pages)

    if not chunks:
        print("ERROR: No chunks created.")
        return

    # Step 3: Build and save FAISS index
    print("\n[3/3] Building FAISS index...")
    build_and_save_index(chunks)

    print("\n" + "=" * 50)
    print("Index built successfully!")
    print("You can now start Phase 4 (RAG pipeline)")
    print("=" * 50)

if __name__ == "__main__":
    main()