import os
import uuid
import json
from datetime import datetime
from app.services.ocr_service import extract_text_from_file
from app.services.chunk_service import chunk_text_by_paragraph

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
DOCS_JSON = os.path.join(DATA_DIR, 'documents.json')
os.makedirs(DATA_DIR, exist_ok=True)

# Ensure documents.json exists
if not os.path.exists(DOCS_JSON):
    with open(DOCS_JSON, 'w') as f:
        json.dump([], f)

async def handle_upload(file):
    doc_id = str(uuid.uuid4())
    filename = f"{doc_id}_{file.filename}"
    file_path = os.path.join(DATA_DIR, filename)
    with open(file_path, "wb") as f_out:
        content = await file.read()
        f_out.write(content)
    # Extract text
    extracted_text = extract_text_from_file(file_path)
    # Save extracted text to a .txt file
    text_path = os.path.join(DATA_DIR, f"{doc_id}.txt")
    with open(text_path, 'w', encoding='utf-8') as f_txt:
        f_txt.write(extracted_text)
    # Chunk the text
    chunks = chunk_text_by_paragraph(doc_id, extracted_text)
    chunks_path = os.path.join(DATA_DIR, f"{doc_id}_chunks.json")
    with open(chunks_path, 'w', encoding='utf-8') as f_chunks:
        json.dump(chunks, f_chunks, indent=2)
    # Prepare metadata
    metadata = {
        "doc_id": doc_id,
        "filename": file.filename,
        "upload_time": datetime.utcnow().isoformat(),
        "text_path": text_path,
        "chunks_path": chunks_path
    }
    # Append metadata to documents.json
    with open(DOCS_JSON, 'r+', encoding='utf-8') as f_json:
        docs = json.load(f_json)
        docs.append(metadata)
        f_json.seek(0)
        json.dump(docs, f_json, indent=2)
        f_json.truncate()
    return metadata

def list_documents():
    with open(DOCS_JSON, 'r', encoding='utf-8') as f_json:
        docs = json.load(f_json)
    # Don't return text_path or chunks_path in the listing for brevity
    return {"documents": [
        {k: v for k, v in doc.items() if k not in ("text_path", "chunks_path")} for doc in docs
    ]} 