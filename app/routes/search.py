from fastapi import APIRouter
import json, os,time


from app.services.embeddings import get_embeddings
from app.services.similarity import cosine_similarity
from app.services.explainer import explain_similarity
from app.services.retriever import retrieve
from app.services.generator import generate_answer
from app.services.context_builder import build_context
from app.schemas.query import   Query
start_time =time.time()

router = APIRouter()
CHUNK_DIR = "data/chunks"



@router.post("/search")
async def search(data: Query):

    file_path = os.path.join(CHUNK_DIR, f"{data.filename}.json")

    if not os.path.exists(file_path):
        return { "error" : "File not indexed yet."}

    with open(file_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    t_embed= time.time()

    query_embedding = get_embeddings([data.query])[0]
    print("Embedding time:", time.time() - t_embed)

    t_retrieve= time.time()
    top_chunks = retrieve(query_embedding, chunks)
    print("Retrieved chunks:", len(top_chunks))
    print("Retrieval time:", time.time() - t_retrieve)


    top_results = []
    threshold = 0.6

    scores = [c["score"] for c in top_chunks]
    max_score = max(scores) if scores else 0
    avg_score = sum(scores) / len(scores) if scores else 0

    print("Top score:", max_score)
    print("Average score:", avg_score)

    for c in top_chunks:
        explanation = explain_similarity(data.query, c["text"])

        if c["score"] > threshold:
            top_results.append({
                "id": c["id"],
                "text": c["text"],
                "score": c["score"],
                "explanation": explanation
            })

    context =  build_context(top_results)
    answer= generate_answer(data.query, context)

    print("Chunks checked:", len(top_chunks))
    print("Passing threshold:", len(top_results))
    print("Total request time:", time.time() - start_time)

    if not top_results:
        return {"results": "no similar object found."}

    return {
        "query": data.query,

        "retrieval_meta" :{
            "chunks_checked": len(top_chunks),
            "results_after_threshold": len(top_results),
            "max_score": max_score,
            "avg_score": avg_score
      },

        "context_preview": context[:200],
        "answer" :answer,

        "results": top_results

    }

    



   
