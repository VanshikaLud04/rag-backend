from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import time

from app.services.embeddings import get_embeddings
from app.services.retriever import retrieve
from app.services.generator import stream_answer
from app.services.context_builder import build_context
from app.schemas.query import Query

router = APIRouter()


@router.post("/search")
async def search(data: Query):
    start_time = time.time()
    print(f"Query received: {data.query}")

    t_embed = time.time()
    query_embedding = get_embeddings([data.query])[0]
    print(f"Embedding time: {time.time() - t_embed:.3f}s")

    t_retrieve = time.time()
    top_chunks = await retrieve(query_embedding, top_k=5)
    print(f"Retrieval time: {time.time() - t_retrieve:.3f}s")
    print(f"Chunks retrieved: {len(top_chunks)}")

    threshold = 0.3
    top_results = [c for c in top_chunks if c["score"] > threshold]

    if not top_results:
        return {"result": "No relevant content found in the document."}

    context = build_context(top_results)
    MAX_CONTEXT = 6000
    if len(context) > MAX_CONTEXT:
        context = context[:MAX_CONTEXT]
        print("Context trimmed to 6000 chars")
    else:
        print(f"Context length: {len(context)}")

    sources = [c["id"] for c in top_results]

    print(f"Chunks passing threshold: {len(top_results)}")
    print(f"Total time so far: {time.time() - start_time:.3f}s")

    return StreamingResponse(
        stream_answer(data.query, context, sources),
        media_type="text/plain"
    )