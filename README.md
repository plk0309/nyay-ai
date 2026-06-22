Here's the complete updated README for Nyay AI:

```markdown
# ⚖️ Nyay AI — Vernacular Legal Aid Platform

<div align="center">

![Nyay AI](https://img.shields.io/badge/Nyay%20AI-Legal%20Aid-c9a84c?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React-18.3-61dafb?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**AI-powered Indian legal aid chatbot with multilingual voice support**

[🌐 Live Demo](https://nyay-ai-one.vercel.app) • [📖 Documentation](#) • [🐛 Issues](https://github.com/plk0309/nyay-ai/issues)

</div>

---

## 📌 Overview

Nyay AI makes Indian law accessible to every citizen — in their own language. Ask any legal question by typing or speaking in **Hindi or English**, and get an instant answer citing the exact **act name and section number** from verified Indian legal documents.

> *"1.4 billion people. Fewer than 2 million lawyers. Nyay AI bridges the gap."*

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎙️ **Voice Input** | Speak in Hindi or English — transcribed locally using faster-whisper |
| 🔊 **Voice Output** | Answers read aloud in your language via gTTS |
| 📚 **28 Legal Documents** | BNS, BNSS, RERA, RTI, Consumer Protection, POCSO, and more |
| 🌐 **9 Languages** | Hindi, English, Tamil, Telugu, Marathi, Bengali, Gujarati, Kannada, Punjabi |
| 📎 **Source Citations** | Every answer cites exact PDF and page number |
| 💬 **Session Memory** | Follow-up questions understand previous context |
| 🔐 **Authentication** | JWT-based login with guest mode for instant access |
| 📱 **Mobile Responsive** | Works on phone browsers |

---

## 🏗️ Architecture

```
User (Voice/Text)
      │
      ▼
React Frontend (Vercel)
      │ HTTPS
      ▼
FastAPI Backend (Railway)
      │
   ┌──┴──────────────────┐
   │                     │
   ▼                     ▼
Auth (JWT)          RAG Pipeline
PostgreSQL          │
                    ├── FAISS Retrieval (top-10)
                    ├── Cohere Reranking (top-3)
                    └── Groq LLaMA 3.1-8B (answer)
                    │
              Voice Pipeline
              ├── faster-whisper (STT)
              ├── deep-translator (Hindi↔English)
              └── gTTS (TTS)
```

---

## 🤖 RAG Pipeline

```
Query → Embed (MiniLM-L6-v2) → FAISS Search (top-10)
      → Cohere Rerank (top-3) → Groq LLaMA 3.1-8B
      → Answer + Source Citations
```

| Parameter | Value |
|---|---|
| Chunk Size | 512 tokens |
| Chunk Overlap | 50 tokens |
| Embedding Model | all-MiniLM-L6-v2 (384 dims) |
| Vector Index | FAISS IndexFlatIP |
| Initial Retrieval | Top-10 chunks |
| After Reranking | Top-3 chunks |
| LLM | LLaMA 3.1-8B-Instant via Groq |
| Total Chunks | 9,615 |

---

## 📊 Evaluation Results

Evaluated on **25 domain-specific test questions** across 7 legal categories:

| Metric | Score |
|---|---|
| ✅ Answer Relevancy | **73.8%** |
| ✅ Retrieval Accuracy | **81.6%** |
| ⚡ Avg Response Latency | **~1.8 seconds** |
| 📝 Test Questions | **25/25 successful** |

*Custom evaluation framework using cosine similarity (MiniLM) and category-matching metrics.*

---

## 📚 Legal Knowledge Base

| Category | Documents | Chunks |
|---|---|---|
| Criminal Laws | BNS 2023, BNSS 2023, BSA 2023, POCSO Act | 3,415 |
| Housing Laws | RERA Act, Motor Vehicles Act | 1,166 |
| Financial Laws | IBC 2016, Negotiable Instruments Act | 1,164 |
| Employment Laws | Industrial Disputes Act, Gratuity Act, Maternity Benefit Act | 876 |
| Labour Laws | Minimum Wages Act, EPF Act, POSH Act, Shops & Establishments | 753 |
| Property Laws | Transfer of Property Act, Land Acquisition Act, Registration Act | 630 |
| Family Laws | Hindu Marriage Act, Domestic Violence Act, Maintenance Act, Special Marriage Act | 509 |
| Consumer Laws | Consumer Protection Act 2019 | 293 |
| Cyber Laws | IT Act 2000 | 292 |
| Central Laws | RTI Act 2005 | 287 |
| Personal Laws | Hindu Succession Act, Muslim Personal Law | 118 |
| SC/ST Laws | SC/ST Atrocities Act 1989 | 112 |
| **Total** | **28 documents** | **9,615** |

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** — REST API with auto-documentation
- **SQLAlchemy + PostgreSQL** — User data and chat history
- **python-jose + bcrypt** — JWT authentication and password hashing
- **LangChain** — RAG pipeline orchestration
- **FAISS** — Vector similarity search
- **sentence-transformers** — MiniLM-L6-v2 embeddings
- **Cohere** — Cross-encoder reranking
- **Groq** — LLaMA 3.1-8B-Instant inference
- **faster-whisper** — Local speech-to-text
- **gTTS** — Text-to-speech
- **deep-translator** — Hindi-English translation
- **PyMuPDF** — PDF text extraction

### Frontend
- **React 18** — Component-based UI
- **React Router** — Client-side routing
- **Axios** — HTTP client
- **Lucide React** — Icons
- **React Hot Toast** — Notifications

### Infrastructure
- **Vercel** — Frontend hosting
- **Railway** — Backend + PostgreSQL hosting
- **Docker** — Containerization
- **GitHub Actions** — Auto-deployment on push

---

## 🚀 Local Setup

### Prerequisites
- Python 3.12+
- Node.js 20+
- PostgreSQL

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/plk0309/nyay-ai.git
cd nyay-ai/backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install torch==2.2.0 --index-url https://download.pytorch.org/whl/cpu
pip install sentence-transformers==3.4.1
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Fill in your API keys

# Build FAISS index (first time only)
python rag/index_builder.py

# Run the server
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd nyay-ai/frontend
npm install
npm run dev
```

Open `http://localhost:3000`

### Environment Variables

```env
GROQ_API_KEY=your_groq_key
COHERE_API_KEY=your_cohere_key
DATABASE_URL=postgresql://user:password@localhost/nyayai
JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
```

---

## 📁 Project Structure

```
nyay-ai/
├── backend/
│   ├── main.py                 # FastAPI app entry point
│   ├── database.py             # SQLAlchemy setup
│   ├── auth_utils.py           # JWT + bcrypt
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── railway.json
│   ├── rag/
│   │   ├── loader.py           # PDF extraction
│   │   ├── chunker.py          # Text splitting
│   │   ├── embedder.py         # FAISS indexing
│   │   ├── retriever.py        # FAISS + Cohere reranking
│   │   ├── pipeline.py         # End-to-end RAG
│   │   ├── evaluator.py        # Custom evaluation
│   │   └── index_builder.py    # Build script
│   ├── routes/
│   │   ├── auth.py             # Register, login, /me
│   │   ├── query.py            # /ask, /history, /ask/guest
│   │   └── voice.py            # /transcribe, /speak, /ask-voice
│   ├── services/
│   │   ├── voice_in.py         # faster-whisper
│   │   ├── voice_out.py        # gTTS
│   │   └── translation.py      # deep-translator
│   └── models/
│       └── user.py             # SQLAlchemy models
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Auth.jsx
│   │   │   └── Chat.jsx
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   └── api/
│   │       └── axios.js
│   ├── vercel.json
│   └── package.json
├── legal_docs/                 # 28 Indian legal PDFs
│   ├── criminal_laws/
│   ├── housing_laws/
│   ├── labour_laws/
│   ├── family_laws/
│   ├── financial_laws/
│   ├── employment_laws/
│   ├── property_laws/
│   ├── consumer_laws/
│   ├── cyber_laws/
│   ├── central_laws/
│   ├── personal_laws/
│   └── sc_st_laws/
└── faiss_index/                # Pre-built vector index
    ├── legal.index
    └── chunks.pkl
```

---

## 🔌 API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/auth/register` | ❌ | Create account |
| POST | `/auth/login` | ❌ | Login, get JWT |
| GET | `/auth/me` | ✅ | Get profile |
| POST | `/query/ask` | ✅ | Ask legal question |
| POST | `/query/ask/guest` | ❌ | Ask without login |
| GET | `/query/history` | ✅ | Chat history |
| POST | `/voice/transcribe` | ❌ | Audio → text |
| POST | `/voice/speak` | ❌ | Text → audio |
| POST | `/voice/ask-voice` | ❌ | Full voice pipeline |
| GET | `/health` | ❌ | Health check |
| GET | `/docs` | ❌ | Swagger UI |

---

## 🎯 What Makes This Different

1. **Updated 2023 Indian Criminal Laws** — Uses BNS, BNSS, BSA (not outdated IPC/CrPC)
2. **Local Voice Processing** — faster-whisper runs on-server, zero API cost
3. **Three-Stage Retrieval** — FAISS → Cohere reranker → LLaMA generation
4. **Vernacular-First Design** — Hindi as a first-class citizen, not an afterthought
5. **Source-Cited Answers** — Every answer links to exact PDF page
6. **Custom Evaluation** — 25 hand-crafted Indian legal test questions

---

## 🗺️ Roadmap

- [ ] Chat History page in frontend
- [ ] Explore Laws section
- [ ] Legal document summarizer (upload PDF → plain language summary)
- [ ] Indian Kanoon API integration for court judgments
- [ ] IndicTrans2 for better Hindi translation quality
- [ ] WhatsApp bot integration
- [ ] Jurisdiction-aware answers (state-specific laws)
- [ ] Legal notice generator

---


## 👩‍💻 Author

**Palak Verma**
- GitHub: [@plk0309](https://github.com/plk0309)
- Bennett University, B.Tech CSE (3rd Year)

---

<div align="center">

**⭐ Star this repo if you found it useful!**

Built with ❤️ for making Indian law accessible to everyone

</div>
```

