# ⚖️ Nyay AI

Nyay AI is an AI-powered Indian Legal Assistant that helps users understand laws, rights, and legal procedures through Retrieval-Augmented Generation (RAG).

The system retrieves information directly from Indian legal documents and uses Large Language Models (Gemini) to generate accurate, source-grounded answers.

---

# 🚀 Features

## Legal Question Answering
- Ask legal questions in natural language
- Context-aware responses
- Source-backed legal information

## RAG Pipeline
- PDF document ingestion
- Legal text chunking
- Vector embeddings
- FAISS semantic search
- Cohere reranking
- Gemini-powered answer generation

## Legal Domains Covered

### Criminal Laws
- Bharatiya Nyaya Sanhita (BNS) 2023
- Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023
- Bharatiya Sakshya Adhiniyam (BSA) 2023
- POCSO Act

### Consumer Laws
- Consumer Protection Act 2019

### Labour Laws
- Minimum Wages Act
- Shops and Establishments Act
- EPF Act
- POSH Act

### Housing Laws
- RERA Act
- Uttar Pradesh Urban Buildings Act
- Motor Vehicles Act

### Personal Laws
- Hindu Succession Act
- Muslim Personal Law

### Cyber Laws
- Information Technology Act 2000

### Constitutional / Governance
- RTI Act 2005

---

# 🏗️ Architecture

```text
User Query
     │
     ▼
Retriever (FAISS)
     │
     ▼
Cohere Reranker
     │
     ▼
Relevant Legal Chunks
     │
     ▼
Gemini LLM
     │
     ▼
Legal Answer + Sources
```

---

# 📂 Project Structure

```text
nyay-ai/
│
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   │
│   ├── routes/
│   ├── services/
│   ├── models/
│   └── rag/
│       ├── loader.py
│       ├── chunker.py
│       ├── embedder.py
│       ├── retriever.py
│       ├── pipeline.py
│       ├── evaluator.py
│       └── index_builder.py
│
├── frontend/
│
├── legal_docs/
│
├── faiss_index/
│
├── docker-compose.yml
│
└── README.md
```

---

# 🛠️ Tech Stack

## Backend
- Python
- FastAPI
- LangChain

## AI / RAG
- Google Gemini
- Sentence Transformers
- FAISS
- Cohere Rerank

## Database
- PostgreSQL

## Frontend
- React
- Vite

## Voice (Planned)
- Whisper
- gTTS

## Deployment (Planned)
- Docker
- Render / Railway / AWS

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/plk0309/nyay-ai.git
cd nyay-ai
```

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create:

```text
backend/.env
```

Example:

```env
GEMINI_API_KEY=your_gemini_api_key
COHERE_API_KEY=your_cohere_api_key

OPENAI_API_KEY=your_openai_key
DATABASE_URL=postgresql://user:password@localhost/nyayai
JWT_SECRET=your_secret_key
```

---

# 📚 Legal Corpus

Store legal PDFs inside:

```text
legal_docs/
```

Example:

```text
legal_docs/
├── criminal_laws/
├── consumer_laws/
├── labour_laws/
├── housing_laws/
├── personal_laws/
├── cyber_laws/
└── central_laws/
```

---

# 🔍 Build Vector Index

Run:

```bash
cd backend
python rag/index_builder.py
```

This will:

- Load PDFs
- Chunk legal text
- Generate embeddings
- Create FAISS index

Output:

```text
faiss_index/
```

---

# 🧪 Test Retrieval

```bash
python rag/test_retrieval.py
```

Example:

```text
Query:
What protections does POCSO provide?

Retrieved:
POCSO Act Section ...
```

---

# 🧪 Test Complete RAG Pipeline

```bash
python rag/test_pipeline.py
```

Example:

```text
Question:
How do I file an RTI application?

Answer:
...
```

---

# 🎯 Future Roadmap

## Phase 5
- FastAPI endpoints
- Authentication
- Chat APIs

## Phase 6
- Voice input
- Voice output
- Speech-to-text

## Phase 7
- React frontend
- Chat UI
- Source citations

## Phase 8
- Evaluation using RAGAS
- Hallucination detection
- Retrieval metrics

## Phase 9
- Dockerization
- CI/CD
- Cloud deployment

---

# ⚠️ Disclaimer

Nyay AI is an educational and informational legal assistant.

It does not replace a qualified lawyer, advocate, or legal professional.

Users should consult licensed legal practitioners for legal advice and representation.

---

# 👨‍💻 Author

**Palak**

AI/ML • Backend Engineering • Legal AI

GitHub:

https://github.com/plk0309

---
