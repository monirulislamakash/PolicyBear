import os, json
from dataclasses import dataclass
from typing import List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer

# Optional FAISS for speed on big FAQ sets
try:
    import faiss
    USE_FAISS = True
except Exception:
    USE_FAISS = False

BOT_NAME = os.getenv("BOT_NAME", "Ray Assistant")
BOT_TONE = os.getenv("BOT_TONE", "Friendly, concise, simple English.")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.78"))
TOP_K = 5
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

@dataclass
class FAQ:
    q: str
    a: str
    tags: List[str]

def load_faqs(path: str) -> List[FAQ]:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    out = []
    for r in raw:
        q = (r.get("question") or "").strip()
        a = (r.get("answer") or "").strip()
        tags = r.get("tags", [])
        if q and a:
            out.append(FAQ(q, a, tags))
    return out

def build_corpus(faqs: List[FAQ]) -> List[str]:
    corpus = []
    for f in faqs:
        text = f.q
        if f.tags:
            text += " | " + " | ".join(f.tags)
        corpus.append(text)
    return corpus

class Embedder:
    def __init__(self, model_name: str = MODEL_NAME):
        self.model = SentenceTransformer(model_name)
    def encode(self, texts: List[str]) -> np.ndarray:
        return np.asarray(self.model.encode(texts, normalize_embeddings=True), dtype="float32")

class SearchIndex:
    def __init__(self, embeddings: np.ndarray):
        self.emb = embeddings
        self.n, self.d = embeddings.shape
        if USE_FAISS:
            self.index = faiss.IndexFlatIP(self.d)
            self.index.add(self.emb)
        else:
            self.index = None
    def query(self, vec: np.ndarray, top_k: int = 5) -> Tuple[List[int], List[float]]:
        if vec.ndim == 1:
            vec = vec.reshape(1, -1)
        if USE_FAISS:
            scores, idx = self.index.search(vec, top_k)
            return idx[0].tolist(), scores[0].tolist()
        sims = (self.emb @ vec.T).ravel()
        idx = np.argsort(-sims)[:top_k]
        return idx.tolist(), sims[idx].tolist()
