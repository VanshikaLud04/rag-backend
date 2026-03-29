import chromadb

client = chromadb.PersistentClient(path="data/chromadb")

collection = client.get_or_create_collection(name="rag_collection")


def add_to_vectorstore(ids, documents, embeddings):
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings
    )


def search_vectorstore(query_embedding, top_k=3):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    docs = results["documents"][0]
    distances = results["distances"][0]

    return [
        {"text": doc, "score": 1 - dist, "id": i}
        for i, (doc, dist) in enumerate(zip(docs, distances))
    ]