# ⚖️ Nyay AI — Vernacular Legal Aid Platform

<div align="center">

![Nyay AI](https://img.shields.io/badge/Nyay%20AI-Legal%20Aid-c9a84c?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge\&logo=python)
![React](https://img.shields.io/badge/React-18.3-61dafb?style=for-the-badge\&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge\&logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**AI-powered Indian legal aid chatbot with multilingual voice support**

[Live Demo](https://nyay-ai-one.vercel.app) • Documentation • [Issues](https://github.com/plk0309/nyay-ai/issues)

</div>

---

## Overview

Nyay AI makes Indian law accessible to every citizen in their own language. Ask any legal question by typing or speaking in Hindi or English and get an instant answer citing the exact act name and section number from verified Indian legal documents.

> "1.4 billion people. Fewer than 2 million lawyers. Nyay AI bridges the gap."

---

## Features

| Feature            | Description                                                                 |
| ------------------ | --------------------------------------------------------------------------- |
| Voice Input        | Speak in Hindi or English — transcribed locally using faster-whisper        |
| Voice Output       | Answers read aloud in your language via gTTS                                |
| 28 Legal Documents | BNS, BNSS, RERA, RTI, Consumer Protection, POCSO, and more                  |
| 9 Languages        | Hindi, English, Tamil, Telugu, Marathi, Bengali, Gujarati, Kannada, Punjabi |
| Source Citations   | Every answer cites exact PDF and page number                                |
| Session Memory     | Follow-up questions understand previous context                             |
| Authentication     | JWT-based login with guest mode for instant access                          |
| Mobile Responsive  | Works on phone browsers                                                     |

---

## Architecture

```text
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

## RAG Pipeline

```text
Query → Embed (MiniLM-L6-v2) → FAISS Search (top-10)
      → Cohere Rerank (top-3) → Groq LLaMA 3.1-8B
      → Answer + Source Citations
```

| Parameter         | Value                         |
| ----------------- | ----------------------------- |
| Chunk Size        | 512 tokens                    |
| Chunk Overlap     | 50 tokens                     |
| Embedding Model   | all-MiniLM-L6-v2 (384 dims)   |
| Vector Index      | FAISS IndexFlatIP             |
| Initial Retrieval | Top-10 chunks                 |
| After Reranking   | Top-3 chunks                  |
| LLM               | LLaMA 3.1-8B-Instant via Groq |
| Total Chunks      | 9,615                         |

---

## Evaluation Results

Evaluated on **25 domain-specific test questions** across 7 legal categories:

| Metric               | Score                |
| -------------------- | -------------------- |
| Answer Relevancy     | **73.8%**            |
| Retrieval Accuracy   | **81.6%**            |
| Avg Response Latency | **~1.8 seconds**     |
| Test Questions       | **25/25 successful** |

Custom evaluation framework using cosine similarity (MiniLM) and category-matching metrics.

---

## Legal Knowledge Base

| Category        | Documents                                                                        | Chunks    |
| --------------- | -------------------------------------------------------------------------------- | --------- |
| Criminal Laws   | BNS 2023, BNSS 2023, BSA 2023, POCSO Act                                         | 3,415     |
| Housing Laws    | RERA Act, Motor Vehicles Act                                                     | 1,166     |
| Financial Laws  | IBC 2016, Negotiable Instruments Act                                             | 1,164     |
| Employment Laws | Industrial Disputes Act, Gratuity Act, Maternity Benefit Act                     | 876       |
| Labour Laws     | Minimum Wages Act, EPF Act, POSH Act, Shops & Establishments                     | 753       |
| Property Laws   | Transfer of Property Act, Land Acquisition Act, Registration Act                 | 630       |
| Family Laws     | Hindu Marriage Act, Domestic Violence Act, Maintenance Act, Special Marriage Act | 509       |
| Consumer Laws   | Consumer Protection Act 2019                                                     | 293       |
| Cyber Laws      | IT Act 2000                                                                      | 292       |
| Central Laws    | RTI Act 2005                                                                     | 287       |
| Personal Laws   | Hindu Succession Act, Muslim Personal Law                                        | 118       |
| SC/ST Laws      | SC/ST Atrocities Act 1989                                                        | 112       |
| **Total**       | **28 documents**                                                                 | **9,615** |

---

## Tech Stack

### Backend

* FastAPI
* SQLAlchemy + PostgreSQL
* python-jose + bcrypt
* LangChain
* FAISS
* sentence-transformers
* Cohere
* Groq
* faster-whisper
* gTTS
* deep-translator
* PyMuPDF

### Frontend

* React 18
* React Router
* Axios
* Lucide React
* React Hot Toast

### Infrastructure

* Vercel
* Railway
* Docker
* GitHub Actions

---

## Local Setup

### Prerequisites

* Python 3.12+
* Node.js 20+
* PostgreSQL

### Backend Setup

```bash
git clone https://github.com/plk0309/nyay-ai.git

cd nyay-ai/backend

python -m venv venv

venv\Scripts\activate

pip install torch==2.2.0 --index-url https://download.pytorch.org/whl/cpu

pip install sentence-transformers==3.4.1

pip install -r requirements.txt

cp .env.example .env

python rag/index_builder.py

uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd nyay-ai/frontend

npm install

npm run dev
```

Open:

```text
http://localhost:3000
```

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

## Project Structure

```text
nyay-ai/

├── backend/
│   ├── main.py
│   ├── database.py
│   ├── auth_utils.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── railway.json
│   ├── rag/
│   │   ├── loader.py
│   │   ├── chunker.py
│   │   ├── embedder.py
│   │   ├── retriever.py
│   │   ├── pipeline.py
│   │   ├── evaluator.py
│   │   └── index_builder.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── query.py
│   │   └── voice.py
│   ├── services/
│   │   ├── voice_in.py
│   │   ├── voice_out.py
│   │   └── translation.py
│   └── models/
│       └── user.py

├── frontend/

├── legal_docs/

└── faiss_index/
```

---

## API Endpoints

| Method | Endpoint            | Auth | Description         |
| ------ | ------------------- | ---- | ------------------- |
| POST   | `/auth/register`    | No   | Create account      |
| POST   | `/auth/login`       | No   | Login, get JWT      |
| GET    | `/auth/me`          | Yes  | Get profile         |
| POST   | `/query/ask`        | Yes  | Ask legal question  |
| POST   | `/query/ask/guest`  | No   | Ask without login   |
| GET    | `/query/history`    | Yes  | Chat history        |
| POST   | `/voice/transcribe` | No   | Audio to text       |
| POST   | `/voice/speak`      | No   | Text to audio       |
| POST   | `/voice/ask-voice`  | No   | Full voice pipeline |
| GET    | `/health`           | No   | Health check        |
| GET    | `/docs`             | No   | Swagger UI          |

---

## What Makes This Different

1. Updated 2023 Indian Criminal Laws using BNS, BNSS and BSA.
2. Local Voice Processing using faster-whisper.
3. Three-stage retrieval: FAISS → Cohere → LLaMA.
4. Vernacular-first design.
5. Source-cited answers.
6. Custom evaluation with Indian legal test questions.

---

## Roadmap

* [ ] Chat History page
* [ ] Explore Laws section
* [ ] Legal document summarizer
* [ ] Indian Kanoon API integration
* [ ] IndicTrans2 integration
* [ ] WhatsApp bot integration
* [ ] Jurisdiction-aware answers
* [ ] Legal notice generator

---

## Author

**Palak Verma**

* GitHub: https://github.com/plk0309
* Bennett University, B.Tech CSE

---

<div align="center">

**Star this repository if you found it useful.**

Built for making Indian law accessible to everyone.

</div>
