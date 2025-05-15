# Research Chatbot with Theme Identification

A web-based AI chatbot that performs research across a large set of documents, identifies common themes, and provides detailed, cited responses to user queries. Built with FastAPI, Streamlit, ChromaDB, and Groq's free Llama-3 API.

---

## Features
- **Document Upload:** Upload 75+ documents (PDF, images, or text). OCR is used for scanned files.
- **Knowledge Base:** Extracts and stores text, chunks by paragraph, and embeds for semantic search.
- **Semantic Search:** Finds the most relevant document chunks for any user query.
- **Theme Synthesis:** Uses LLM (Groq Llama-3) to group answers into themes and provide cited summaries.
- **Citations:** Every answer is cited with document ID and location (paragraph).
- **Frontend:** Simple Streamlit UI for uploads, queries, and results.

---

## Tech Stack
- **Backend:** FastAPI (Python)
- **Frontend:** Streamlit
- **Vector DB:** ChromaDB
- **OCR:** Tesseract (via pytesseract)
- **LLM:** Groq (Llama-3, free API)

---

## Setup Instructions

### 1. Clone the Repository
```bash
# Clone this repo and enter the directory
cd chatbot_theme_identifier
```

### 2. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 3. Set Your Groq API Key
Get a free API key from [Groq Console](https://console.groq.com/keys).

**On Windows (CMD):**
```cmd
set GROQ_API_KEY=your-groq-api-key-here
```
**On PowerShell:**
```powershell
$env:GROQ_API_KEY="your-groq-api-key-here"
```
**On Mac/Linux:**
```bash
export GROQ_API_KEY=your-groq-api-key-here
```

### 4. Start the Backend
```bash
cd backend
uvicorn app.main:app --reload
```

### 5. Start the Frontend
In a new terminal:
```bash
streamlit run frontend/app.py
```

### 6. Use the App
- Open [http://localhost:8501](http://localhost:8501) in your browser.
- Upload documents, ask questions, and view cited, theme-based answers!

---

## Folder Structure
```
chatbot_theme_identifier/
├── backend/
│   ├── app/
│   ├── data/
│   └── requirements.txt
├── frontend/
│   └── app.py
├── README.md
```

---

## Credits
- [Groq](https://groq.com/) for free Llama-3 API
- [ChromaDB](https://www.trychroma.com/)
- [Streamlit](https://streamlit.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

---

