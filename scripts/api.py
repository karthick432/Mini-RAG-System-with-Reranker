from flask import Flask, request, jsonify
from scripts.search_baseline import baseline_search
from scripts.reranker import hybrid_reranker
import sqlite3

app = Flask(__name__)

# Load chunks once
conn = sqlite3.connect("db/chunks.db")
c = conn.cursor()
c.execute("SELECT doc_name, chunk_index, text FROM chunks")
chunks = {(doc, idx): text for doc, idx, text in c.fetchall()}
conn.close()

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    print("Received JSON:", data)   # <-- debug
    if not data or "q" not in data:
        return {"error": "Missing 'q' in request"}, 400

    query = data.get("query") or data.get("q")
    k = data.get("k", 5)
    mode = data.get("mode", "baseline")

    # Baseline search
    baseline_results = baseline_search(query, top_k=k)

    # Optional rerank
    if mode == "rerank":
        results = hybrid_reranker(query, baseline_results, chunks)
    else:
        results = baseline_results

    enriched_results = []
    for r in results:
        doc_name = r["doc_name"]
        idx = r["chunk_index"]
        enriched_results.append({
            **r,
            "text": chunks.get((doc_name, idx), "")   # add the actual snippet
        })

    return {
        "query": query,
        "results": enriched_results,
        "reranker_used": mode
    }



if __name__ == "__main__":
    app.run(debug=True)
