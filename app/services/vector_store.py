import chromadb
from chromadb.config import Settings

client= chromadb.Client(
    Settings(
        persist_directory= "data/chromadb"
    )
)

collection= client.get_or_create_collection( name="rag_collection")

def add_to_vectorstore(ids, documents, embeddings):
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings
    )

def search_vectorstore(query_embeddings, TOP_K):
    results=collection.query(
        query_embeddings=[query_embeddings],
        n_results=TOP_K
    )
    return results["documents"][0]