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

    prompt = f"""You are Nyay AI, a helpful Indian legal assistant for common citizens.

Answer the user's question based on the legal context provided below.
Follow these rules:
1. Be specific and practical — tell the user what they can actually DO
2. Mention specific section numbers and act names
3. If the exact answer isn't in the context, say what IS there and suggest what to search for
4. Use simple language — assume the user is not a lawyer
5. Structure your answer with clear steps when applicable
6. If context is from wrong document, say so honestly

Legal Context:
{context}

{"Previous conversation:" + history_text if history_text else ""}

User Question: {query}

Practical Answer:"""
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