import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "chunks.db"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Count total rows
c.execute("SELECT COUNT(*) FROM chunks")
total = c.fetchone()[0]

# Count unique rows (by all three columns)
c.execute("""
SELECT COUNT(*) FROM (
    SELECT DISTINCT doc_name, chunk_index, text
    FROM chunks
)
""")
unique = c.fetchone()[0]

duplicates = total - unique

print(f"Total rows     : {total}")
print(f"Unique rows    : {unique}")
print(f"Duplicate rows : {duplicates}")

if duplicates > 0:
    print("⚠️ Duplicates exist in chunks.db")
else:
    print("✅ No duplicates found")

conn.close()
