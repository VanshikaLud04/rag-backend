# RAG Backend — Semantic Retrieval & Grounded LLM API

A production-style Retrieval Augmented Generation (RAG) backend built with a backend-engineering mindset.
The system performs semantic document indexing, similarity retrieval, context construction, and grounded LLM answer generation through a modular async API.

Unlike notebook-centric AI projects, this repository focuses on **scalable backend architecture**, service separation, and real-time inference workflows.

---

##  What This Project Does

This backend allows users to:

* Upload documents for semantic indexing
* Retrieve relevant text chunks using embeddings
* Build contextual prompts dynamically
* Generate grounded answers using an LLM
* Stream responses in real time through an API

Pipeline:

Upload → Extract → Chunk → Embed → Retrieve → Context → Generate

---

##  Architecture Overview

```plaintext
app/
 ├── routes/
 │     └── search.py              # API orchestration
 ├── services/
 │     ├── retriever.py           # ranking engine
 │     ├── context_builder.py     # builds grounded context
 │     ├── generator.py           # streaming LLM layer
 │     └── embeddings.py
 ├── schemas/
 │     └── query.py
data/
 ├── raw/
 └── chunks/
```

### Design Philosophy

* Clear separation between orchestration and logic layers
* Retrieval-first architecture (not blind LLM calls)
* Async-ready backend design
* Debug observability for system understanding

---

## Features

*  Document ingestion + chunking pipeline
*  Semantic similarity search with embeddings
*  Context-aware prompt construction
*  Streaming LLM responses
*  Async FastAPI backend
*  Dockerized deployment
*  Retrieval metadata + debug signals

---

##  Tech Stack

* FastAPI
* Python Async APIs
* Sentence Transformers
* Cosine Similarity Retrieval
* StreamingResponse
* Docker

---

##  Local Setup

```bash
git clone <repo_url>
cd rag-backend

python -m venv myvenv
source myvenv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

##  Docker Usage

Build image:

```bash
docker build -t rag-backend .
```

Run container with persistent storage:

```bash
docker run -p 8000:8000 -v $(pwd)/data:/app/data rag-backend
```

Volume mount ensures indexed chunks remain available after restarts.

---

##  API Endpoints

### POST /ingest

Uploads and indexes a document.

### POST /search

```json
{
  "query": "your question",
  "filename": "indexed_file"
}
```

Returns:

* retrieval metadata
* ranked chunks
* streamed LLM response

---

##  Engineering Highlights

* Service-based modular backend
* Async orchestration layer
* Streaming generator implementation
* Retrieval-grounded generation design
* Docker-ready inference backend

---

## Research Motivation

This system explores:

* Retrieval-based grounding for LLM reliability
* Semantic similarity ranking pipelines
* Scalable AI backend design beyond notebooks

