from fastapi import APIRouter
from pydantic import BaseModel
import json, os

from app.services.embeddings import get_embeddings
from app.services.similarity import cosine_similarity
from app.services.explainer import explain_similarity
from app.services.retriever import retrieve


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

    top_chunks = retrieve(query_embedding, chunks)

    ''' for c in chunks:
        c["score"] = cosine_similarity(query_embedding, c["embedding"])
    
    chunks = sorted(chunks, key=lambda x: x["score"], reverse=True)
    '''
    top_results=[]
    threshold =0.6
    scores= [c["score"] for c in chunks]
    max_score= max(scores) if scores else 0
    avg_score= sum(scores) / len(scores) if scores else 0

    print("Top score:", max_score)
    print("Average score:", avg_score)



    for c in chunks[:3]:
        explanation= explain_similarity(data.query ,c["text"])
        if c["score"]> threshold :
                top_results.append ({
                "id" : c["id"],
                "text" : c["text"],
                "score" : c["score"],
                "explanation" : c["explanation"]
            })
                
        

    if not top_results :
        
         return {"results" : "no similar object found."}

    else :
        return {"results" : top_results}
    

         

        
    



   
