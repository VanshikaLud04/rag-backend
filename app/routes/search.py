from fastapi import APIRouter
from pydantic import BaseModel
import json, os

from app.services.embeddings import get_embeddings
from app.services.similarity import cosine_similarity

router= APIRouter()
CHUNK_DIR="data/chunks"

class Query(BaseModel):
    query: str
    filename: str

@router.post("/search")
async def search (data:Query) :

    file_path = os.path.join(CHUNK_DIR, f"{data.filename}.json")
    with open(file_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    query_embedding = get_embeddings([data.query])[0]

    for c in chunks:
        c["score"] = cosine_similarity(query_embedding, c["embedding"])

    chunks.sort(key=lambda x: x["score"], reverse=True)
    return {"results": chunks[:3]}
