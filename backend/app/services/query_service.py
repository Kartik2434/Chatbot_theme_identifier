from app.services.embedding_service import embed_texts
from app.services.vectordb_service import query_vectordb
import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY") or "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

async def process_query(query):
    # Embed the query
    query_embedding = embed_texts([query])[0]
    # Search ChromaDB for relevant chunks
    results = query_vectordb(query_embedding, n_results=10)
    # Format results with citations
    answers = []
    for i in range(len(results['ids'][0])):
        chunk_id = results['ids'][0][i]
        metadata = results['metadatas'][0][i]
        text = results['documents'][0][i]
        answers.append({
            'doc_id': metadata.get('doc_id'),
            'location': metadata.get('location'),
            'chunk_id': chunk_id,
            'text': text
        })
    # Synthesize themes using Groq
    synthesized = await synthesize_themes(query, answers)
    return {
        'results': answers,
        'synthesized': synthesized
    }

async def synthesize_themes(query, answers):
    if not GROQ_API_KEY:
        return "[LLM synthesis not available: Set GROQ_API_KEY.]"
    context = "\n\n".join([
        f"Document {a['doc_id']} ({a['location']}): {a['text']}" for a in answers
    ])
    prompt = f'''
You are an expert research assistant. Given the following user query and extracted answers from multiple documents, identify and group common themes. For each theme, provide a concise summary and cite the supporting documents and locations (e.g., Document ID, Paragraph).

User Query: {query}

Extracted Answers:
{context}

Format your response as follows:
Theme 1: <summary>
Supporting: <doc_id, location, ...>
Theme 2: ...
...
'''
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful research assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000,
        "temperature": 0.3
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        return f"[Groq API error: {response.status_code} {response.text}]" 