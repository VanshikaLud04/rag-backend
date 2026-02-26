'''
import numpy as np

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


async def retrieve (query_embeddings,chunks, top_k=3):
    for c in chunks:
        c["score"]= cosine_similarity(query_embeddings,c["embeddings"])

    chunks = sorted(chunks, key= lambda x: x["score"], reverse=True)
    return chunks[:top_k]
'''
from app.services.vector_store import search_vectorstore

def retrieve(query_embedding, top_k=3):
    """
    query_embedding: list[float]
    returns: list[str] (top chunk texts)
    """
    return search_vectorstore(query_embedding, top_k)
