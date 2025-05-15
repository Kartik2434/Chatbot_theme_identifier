import chromadb
from chromadb.config import Settings

# Initialize ChromaDB client and collection
client = chromadb.Client(Settings(
    persist_directory="backend/data/chroma_db"
))
collection = client.get_or_create_collection("doc_chunks")

def add_chunks_to_vectordb(chunks, embeddings):
    # Each chunk should have a unique chunk_id
    ids = [chunk['chunk_id'] for chunk in chunks]
    metadatas = [{k: v for k, v in chunk.items() if k != 'text'} for chunk in chunks]
    documents = [chunk['text'] for chunk in chunks]
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=documents
    )

def query_vectordb(query_embedding, n_results=5):
    # Returns the top n_results most similar chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results 