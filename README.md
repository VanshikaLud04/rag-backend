# Semantic RAG Backend 

An async backend implementing embedding-based semantic retrieval using ChromaDB as a persistent vector store, combined with grounded LLM generation via Google Gemini. Includes a minimal HTML frontend for document ingestion and querying.

---

## Pipeline

```
Upload → Extract → Chunk → Embed → Store in Chroma → Vector Search → Context → Generate
```

---

## Project Structure

```
rag-backend/
 ├── app/
 │     ├── routes/
 │     │     └── search.py
 │     ├── services/
 │     │     ├── embeddings.py
 │     │     ├── vector_store.py
 │     │     ├── context_builder.py
 │     │     └── generator.py
 │     └── schemas/
 │           └── query.py
 ├── data/
 │     └── chroma_db/
 ├── rag-ui-minimal.html
 ├── Dockerfile
 ├── requirements.txt
 └── README.md
```

---

## Prerequisites

- Python 3.10+
- A Google Gemini API key

---

## Getting Started

**1. Clone the repo**

```bash
git clone https://github.com/VanshikaLud04/rag-backend.git
cd rag-backend
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

> First run will download the sentence-transformer model (~90MB). This is automatic.

**4. Set up environment variables**

Create a `.env` file in the root:

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

**5. Run the backend**

```bash
uvicorn app.main:app --reload --port 8000
```

Backend will be live at `http://localhost:8000`.

**6. Open the frontend**

With the backend running, open `rag-ui-minimal.html` directly in your browser:

```bash
open rag-ui-minimal.html        # macOS
# or just double-click the file
```

---

## Using Docker

```bash
docker build -t rag-backend .
docker run -p 8000:8000 --env GOOGLE_API_KEY=your_key rag-backend
```

---

## API Reference

### `POST /ingest`

Upload a `.pdf` or `.txt` file. The backend extracts text, chunks it, generates embeddings, and stores them in ChromaDB.

**Request:** `multipart/form-data` with a `file` field.

**Response:**
```json
{
  "saved_as": "document.pdf",
  "chunks": 42
}
```

---

### `POST /search`

Query the ingested document. Returns a streamed LLM response grounded in retrieved chunks.

**Request:**
```json
{
  "query": "What is the refund policy?",
  "filename": "document"
}
```

**Response:** Streaming plain text.

---

## Tech Stack

| Layer | Technology |
|---|---|
| API framework | FastAPI |
| Embeddings | Sentence Transformers |
| Vector database | ChromaDB |
| LLM | Google Gemini (via `google-generativeai`) |
| Streaming | FastAPI `StreamingResponse` |
| Deployment | Docker |

---

## How Vector Search Works

Each text chunk is converted into a high-dimensional embedding vector and stored in ChromaDB. At query time:

1. The query is embedded using the same model
2. ChromaDB performs cosine similarity search to find the top-k nearest chunks
3. Retrieved chunks are assembled into a context prompt
4. Gemini generates a grounded response, streamed back to the client