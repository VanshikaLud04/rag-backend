from fastapi import APIRouter, File, UploadFile
from app.services.chunker import chunk_text
from app.services.extract import extract_text
from app.services.embeddings import get_embeddings
import json
import os, uuid

router = APIRouter()

UPLOAD_DIR = "data/raw"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):

    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    path = os.path.join(UPLOAD_DIR, filename)

    content = await file.read()
    with open(path, "wb") as f:
        f.write(content)

    text = extract_text(path)
    chunks = chunk_text(text)

    print("Chunks created:", len(chunks))

    structured_chunks = []

    for idx, chunk in enumerate(chunks):
        structured_chunks.append({
            "id": idx,
            "text": chunk
        })

    CHUNK_DIR = "data/chunks"
    os.makedirs(CHUNK_DIR, exist_ok=True)

    chunk_file = os.path.join(CHUNK_DIR, f"{filename}.json")

    

    texts=[]

    for c in structured_chunks:
        texts.append(c["texts"])

        
    embeddings= get_embeddings(texts)

    for i , emb in enumerate(embeddings):
        structured_chunks[i]["embedding"]=emb 

    with open(chunk_file, "w", encoding="utf-8") as f:
        json.dump(structured_chunks, f, indent=2)

    return {"saved_as": filename}



