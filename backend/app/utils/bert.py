from sentence_transformers import SentenceTransformer
_model = None

def _get():
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _model

def text_to_bert(text: str) -> list[float]:
    m = _get()
    vec = m.encode([text], convert_to_numpy=True, normalize_embeddings=True)[0]
    return vec.astype("float32").tolist()
