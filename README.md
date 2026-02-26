# Semantic RAG Backend — Vector Database Retrieval with Chroma

An async backend system implementing **embedding-based semantic retrieval** using a persistent vector database (Chroma) combined with grounded LLM generation.

This project demonstrates how modern AI backends move beyond keyword search by operating entirely in **vector space**.

---

##  Architecture Overview

Pipeline:

```id="ragflow"
Upload → Extract → Chunk → Embed → Store in Chroma → Vector Search → Context → Generate
```

Core idea:

Natural language → Embedding vectors → Similarity search → Grounded answer generation.

---

##  Vector Database Integration

### Text → Embeddings

Each chunk is transformed into a high-dimensional vector:

```id="vec"
[0.12, -0.33, 0.89, ...]
```

Embeddings are stored inside **ChromaDB**.

---

### Query → Vector Search

Instead of manual similarity loops, the backend performs:

```id="chromasearch"
collection.query(query_embeddings=[vector], n_results=3)
```

Chroma handles:

* cosine similarity
* ranking
* nearest neighbour retrieval

---

##  Backend Structure

```id="structure"
app/
 ├── routes/
 │     └── search.py
 ├── services/
 │     ├── embeddings.py
 │     ├── vector_store.py     # NEW (Chroma integration)
 │     ├── context_builder.py
 │     └── generator.py
 ├── schemas/
 │     └── query.py
data/
 └── chroma_db/
```

Design philosophy:

* Routes = orchestration
* Services = isolated backend logic

---

##  Tech Stack

* FastAPI (async APIs)
* Sentence Transformers (embeddings)
* ChromaDB (vector database)
* Streaming LLM responses
* Docker deployment

---

##  API Flow

### POST /ingest

* Extract text
* Chunk documents
* Generate embeddings
* Store vectors inside Chroma collection

---

### POST /search

Steps executed:

1. Convert query into embedding vector
2. Perform nearest-neighbour search in Chroma
3. Build grounded context from retrieved documents
4. Generate response using LLM

---

## Engineering Highlights

* Persistent vector database
* Retrieval-first architecture
* Modular backend services
* Streaming grounded generation
* Dockerized deployment

