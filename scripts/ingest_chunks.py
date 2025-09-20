import sqlite3, os
from pathlib import Path
from PyPDF2 import PdfReader
from tqdm import tqdm

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "db"
DB_DIR.mkdir(parents=True, exist_ok=True)   # ensure db/ folder exists
DB_PATH = DB_DIR / "chunks.db"

PDF_FOLDER = BASE_DIR / "data" / "industrial-safety-pdfs"

conn = sqlite3.connect(DB_PATH)
c.execute("DROP TABLE IF EXISTS chunks")   # clean start
c.execute("""
CREATE TABLE chunks(
    id INTEGER PRIMARY KEY,
    doc_name TEXT,
    chunk_index INTEGER,
    text TEXT
)
""")

for fname in tqdm(os.listdir(PDF_FOLDER)):
    if fname.endswith(".pdf"):
        reader = PdfReader(PDF_FOLDER / fname)
        text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
        paragraphs = [p for p in text.split("\n\n") if len(p.split()) > 50]
        for i, p in enumerate(paragraphs):
            c.execute(
                "INSERT INTO chunks(doc_name, chunk_index, text) VALUES (?, ?, ?)",
                (fname, i, p)
            )

conn.commit()
conn.close()
