import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR / "scripts"))
from search_baseline import baseline_search  # now Python finds it

query = "machine safety rules"
results = baseline_search(query, top_k=5)

print("Top chunks:")
for r in results:
    print(f"Score: {r['score']:.4f} | Doc: {r['doc_name']} | Chunk: {r['chunk_index']}")
