# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

from database import engine
from models.user import Base
from routes.auth import router as auth_router
from routes.query import router as query_router

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Nyay AI",
    description="Vernacular AI Legal Aid Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(query_router, prefix="/query", tags=["Legal Query"])

@app.get("/")
def root():
    return {"message": "Nyay AI backend is running", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}