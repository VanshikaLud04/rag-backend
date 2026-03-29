from fastapi import APIRouter, File, UploadFile
from app.services.chunker import chunk_text
from app.services.extract import extract_text
from app.services.embeddings import get_embeddings
from app.services.vector_store import add_to_vectorstore
import json
import os
import uuid

router = APIRouter()

UPLOAD_DIR = "data/raw"
CHUNK_DIR = "data/chunks"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CHUNK_DIR, exist_ok=True)


@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1].lower()
    filename = f"{uuid.uuid4()}.{ext}"
    path = os.path.join(UPLOAD_DIR, filename)

    content = await file.read()
    with open(path, "wb") as f:
        f.write(content)

    text = extract_text(path)
    chunks = chunk_text(text)
    print(f"Chunks created: {len(chunks)}")

    structured_chunks = [
        {"id": str(idx), "text": chunk}
        for idx, chunk in enumerate(chunks)
    ]

    texts = [c["text"] for c in structured_chunks]
    embeddings = get_embeddings(texts)

    for i, emb in enumerate(embeddings):
        structured_chunks[i]["embedding"] = emb

    add_to_vectorstore(
        ids=[c["id"] for c in structured_chunks],
        documents=texts,
        embeddings=embeddings
    )

    chunk_file = os.path.join(CHUNK_DIR, f"{filename}.json")
    with open(chunk_file, "w", encoding="utf-8") as f:
        json.dump(structured_chunks, f, indent=2)

    return {
        "saved_as": filename,
        "chunks": len(chunks),
        "status": "indexed"
    }



