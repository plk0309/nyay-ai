# backend/rag/loader.py
import fitz  # PyMuPDF
import os
import json
from config import LEGAL_DOCS_DIR

def get_category_from_path(filepath: str) -> str:
    """Extract category from folder structure"""
    rel_path = os.path.relpath(filepath, LEGAL_DOCS_DIR)
    parts = rel_path.split(os.sep)
    # parts[0] = top category (criminal_laws, housing_laws etc)
    return parts[0] if len(parts) > 1 else "general"

def get_subcategory_from_path(filepath: str) -> str:
    """Extract subcategory from folder structure"""
    rel_path = os.path.relpath(filepath, LEGAL_DOCS_DIR)
    parts = rel_path.split(os.sep)
    return parts[1] if len(parts) > 2 else parts[0]

def load_pdf(filepath: str) -> list[dict]:
    """Load a single PDF and return list of pages with metadata"""
    pages = []
    try:
        doc = fitz.open(filepath)
        filename = os.path.basename(filepath)
        category = get_category_from_path(filepath)
        subcategory = get_subcategory_from_path(filepath)

        for i, page in enumerate(doc):
            text = page.get_text().strip()
            if len(text) < 50:  # skip empty or near-empty pages
                continue
            pages.append({
                "text": text,
                "metadata": {
                    "source": filename,
                    "filepath": filepath,
                    "page": i + 1,
                    "total_pages": len(doc),
                    "category": category,
                    "subcategory": subcategory,
                }
            })
        doc.close()
        print(f"  Loaded {len(pages)} pages from {filename}")
    except Exception as e:
        print(f"  ERROR loading {filepath}: {e}")
    return pages

def load_all_documents() -> list[dict]:
    """Recursively load all PDFs from legal_docs directory"""
    all_pages = []
    pdf_files = []

    # Walk entire legal_docs directory
    for root, dirs, files in os.walk(LEGAL_DOCS_DIR):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))

    print(f"\nFound {len(pdf_files)} PDF files\n")

    for filepath in pdf_files:
        rel_path = os.path.relpath(filepath, LEGAL_DOCS_DIR)
        print(f"Loading: {rel_path}")
        pages = load_pdf(filepath)
        all_pages.extend(pages)

    print(f"\nTotal pages loaded: {len(all_pages)}")
    return all_pages