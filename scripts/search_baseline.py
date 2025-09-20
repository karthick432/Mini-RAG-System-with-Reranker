import faiss, json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_PATH = BASE_DIR / "db" / "index.faiss"
META_PATH = BASE_DIR / "db" / "chunk_meta.json"

# Load FAISS index and metadata
embed_index = faiss.read_index(str(INDEX_PATH))
with open(META_PATH, "r", encoding="utf-8") as f:
    meta = json.load(f)

# Load model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def baseline_search(query, top_k=5):
    q_emb = model.encode([query], normalize_embeddings=True)
    scores, ids = embed_index.search(np.array(q_emb, dtype=np.float32), top_k)
    results = []
    for score, idx in zip(scores[0], ids[0]):
        results.append({
            "score": float(score),
            "doc_name": meta[idx]["doc_name"],
            "chunk_index": meta[idx]["chunk_index"]
        })
    return results
