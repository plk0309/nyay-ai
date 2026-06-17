# backend/rag/pipeline.py
import os
from groq import Groq
from rag.retriever import retrieve, rerank

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not set in environment")
    return Groq(api_key=api_key)

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
    client = get_groq_client()
    prompt = build_prompt(query, reranked, history)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )

    answer = response.choices[0].message.content

    # Step 4: Build response
    sources = list(set([
        f"{c['metadata']['source']} (Page {c['metadata']['page']})"
        for c in reranked
    ]))

    return {
        "answer": answer,
        "sources": sources,
        "category": reranked[0]["metadata"]["category"] if reranked else "unknown",
        "chunks_used": len(reranked)
    }