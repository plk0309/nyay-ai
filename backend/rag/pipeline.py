# backend/rag/pipeline.py
import os
from google import genai
from rag.retriever import retrieve, rerank

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in environment")
    return genai.Client(api_key=api_key)

def build_prompt(query: str, context_chunks: list[dict], history: list[dict]) -> str:
    context = "\n\n---\n\n".join([
        f"Source: {c['metadata']['source']} (Page {c['metadata']['page']})\n{c['text']}"
        for c in context_chunks
    ])

    history_text = ""
    if history:
        history_text = "\n".join([
            f"User: {h['user']}\nAssistant: {h['assistant']}"
            for h in history[-3:]
        ])

    prompt = f"""You are Nyay AI, a helpful Indian legal assistant.
Answer the user's question based ONLY on the legal context provided below.
Be clear, simple, and practical. Mention specific acts and section numbers when relevant.
If the context does not contain enough information to answer, say so honestly.
Do not make up laws or sections that are not in the context.

Legal Context:
{context}

{"Previous conversation:" + history_text if history_text else ""}

User Question: {query}

Answer:"""
    return prompt

def answer_query(query: str, history: list[dict] = []) -> dict:
    """Full RAG pipeline: retrieve → rerank → generate"""

    # Step 1: Retrieve
    retrieved = retrieve(query, top_k=10)

    # Step 2: Rerank
    reranked = rerank(query, retrieved, top_n=3)

    # Step 3: Generate
    client = get_gemini_client()
    prompt = build_prompt(query, reranked, history)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    # Step 4: Build response
    sources = list(set([
        f"{c['metadata']['source']} (Page {c['metadata']['page']})"
        for c in reranked
    ]))

    return {
        "answer": response.text,
        "sources": sources,
        "category": reranked[0]["metadata"]["category"] if reranked else "unknown",
        "chunks_used": len(reranked)
    }