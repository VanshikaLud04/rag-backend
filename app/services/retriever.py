from app.services.vector_store import search_vectorstore
 
 
async def retrieve(query_embedding, top_k=3):
    """
    query_embedding: list[float]
    returns: list of dicts with keys: text, score, id
    """
    return search_vectorstore(query_embedding, top_k)