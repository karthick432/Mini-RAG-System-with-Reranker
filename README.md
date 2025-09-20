# 📚 Mini RAG System with Reranker

This project implements a **lightweight Retrieval-Augmented Generation (RAG) system** with a reranker for improving search quality. It allows you to ask questions against your documents, retrieve relevant chunks, and re-rank them for better responses.

---

## 🚀 Features
- Upload and index your documents.
- Retrieve top relevant chunks using similarity search.
- Rerank results for improved accuracy.
- Simple REST API built with **Flask** (`/ask` endpoint).
- Easily extendable to integrate LLMs for final answer generation.

---

## 🛠️ Tech Stack
- **Backend:** Python 3, Flask
- **Vector Search:** FAISS 
- **Reranking:** Baseline / Custom reranker
- **Frontend:** streamlit

---

## 📂 Project Structure

.
- ├── scripts/
- │ ├── api.py # Flask backend
- │ ├── retriever.py # Document retrieval logic
- │ └── reranker.py # Reranking logic
- ├── app.py # Streamlit frontend
- ├── requirements.txt # Python dependencies
- └── README.md # Project documentation

- ▶️ Running the Project
- 1️⃣ Start the backend
- python -m scripts.api
- The backend runs on http://127.0.0.1:5000 by default.
- streamlit run app.py
- This opens a browser where you can type queries and see results.

## 📡 API Usage
Endpoint: POST /ask

### Request JSON:
{
  "q": "What are machine safety rules?"
}
### Response JSON:
{
  "query": "What are machine safety rules?",
  "reranker_used": "baseline",
  "results": [
    {
      "chunk_index": 0,
      "doc_name": "safety_manual.pdf",
      "score": 0.84,
      "text": "Always wear protective gear when operating heavy machinery..."
    }
  ]
}

