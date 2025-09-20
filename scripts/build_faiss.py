import sqlite3, json
from pathlib import Path
from tqdm import tqdm
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "chunks.db"
INDEX_PATH = BASE_DIR / "db" / "index.faiss"
META_PATH = BASE_DIR / "db" / "chunk_meta.json"

# Load model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Load chunks
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("SELECT id, doc_name, chunk_index, text FROM chunks")
rows = c.fetchall()
conn.close()

texts = [r[3] for r in rows]
meta = [{"id": r[0], "doc_name": r[1], "chunk_index": r[2]} for r in rows]

# Compute embeddings
print("🔎 Computing embeddings...")
embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True)

# Build FAISS index
dim = embeddings.shape[1]
index = faiss.IndexFlatIP(dim)  # cosine similarity (vectors normalized)
index.add(embeddings)

# Save index and metadata
faiss.write_index(index, str(INDEX_PATH))
with open(META_PATH, "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2)

print(f"✅ FAISS index saved at {INDEX_PATH}")
print(f"✅ Metadata saved at {META_PATH}")
