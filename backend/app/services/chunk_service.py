import re

def chunk_text_by_paragraph(doc_id, text):
    # Split on double newlines or [Page X] markers
    paragraphs = re.split(r'\n\s*\n|\[Page \d+\]', text)
    chunks = []
    for i, para in enumerate(paragraphs):
        clean_para = para.strip()
        if clean_para:
            chunks.append({
                'doc_id': doc_id,
                'chunk_id': f'{doc_id}_chunk_{i+1}',
                'text': clean_para,
                'location': f'Paragraph {i+1}'
            })
    return chunks 