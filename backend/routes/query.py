# backend/routes/query.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.user import ChatHistory
from rag.pipeline import answer_query
from auth_utils import get_current_user
import json

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    language: str = "en"
    history: list = []

@router.post("/ask")
def ask(req: QueryRequest, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        result = answer_query(req.question, req.history)

        # Save to chat history
        chat = ChatHistory(
            user_id=int(current_user["sub"]),
            question=req.question,
            answer=result["answer"],
            sources=json.dumps(result["sources"]),
            category=result["category"],
            language=req.language
        )
        db.add(chat)
        db.commit()

        return {
            "answer": result["answer"],
            "sources": result["sources"],
            "category": result["category"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
def get_history(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    chats = db.query(ChatHistory).filter(
        ChatHistory.user_id == int(current_user["sub"])
    ).order_by(ChatHistory.created_at.desc()).limit(50).all()

    return [
        {
            "id": c.id,
            "question": c.question,
            "answer": c.answer,
            "sources": json.loads(c.sources) if c.sources else [],
            "category": c.category,
            "created_at": str(c.created_at)
        }
        for c in chats
    ]

@router.post("/ask/guest")
def ask_guest(req: QueryRequest):
    """Public endpoint — no auth required, history not saved"""
    try:
        result = answer_query(req.question, req.history)
        return {
            "answer": result["answer"],
            "sources": result["sources"],
            "category": result["category"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))