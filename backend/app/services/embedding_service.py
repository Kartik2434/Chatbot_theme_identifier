from sentence_transformers import SentenceTransformer
import threading

# Use a singleton pattern to avoid reloading the model
_model = None
_model_lock = threading.Lock()

def get_model():
    global _model
    with _model_lock:
        if _model is None:
            _model = SentenceTransformer('all-MiniLM-L6-v2')
        return _model

def embed_texts(texts):
    model = get_model()
    return model.encode(texts, show_progress_bar=False, convert_to_numpy=True).tolist() 