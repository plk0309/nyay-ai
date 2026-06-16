# backend/rag/chunker.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_documents(pages: list[dict]) -> list[dict]:
    """Split pages into smaller overlapping chunks"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = []
    for page in pages:
        splits = splitter.split_text(page["text"])
        for j, split in enumerate(splits):
            split = split.strip()
            if len(split) < 30:  # skip very short chunks
                continue
            chunks.append({
                "text": split,
                "metadata": {
                    **page["metadata"],
                    "chunk_id": f"{page['metadata']['source']}_p{page['metadata']['page']}_c{j}"
                }
            })

    print(f"Total chunks created: {len(chunks)}")
    return chunks