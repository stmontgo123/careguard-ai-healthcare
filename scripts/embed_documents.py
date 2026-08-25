from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import os
import json
from pathlib import Path

from sentence_transformers import SentenceTransformer
from src.rag import SYNTHETIC_DOCUMENTS

MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L12-v2")

def main():
    model = SentenceTransformer(MODEL)
    rows = []
    for doc in SYNTHETIC_DOCUMENTS:
        vector = model.encode(doc["text"], normalize_embeddings=True).tolist()
        rows.append({"doc_id": doc["doc_id"], "embedding": vector})
    out = Path("demo/synthetic_embeddings.json")
    out.write_text(json.dumps(rows), encoding="utf-8")
    print(f"Wrote {len(rows)} synthetic embeddings to {out}")

if __name__ == "__main__":
    main()
