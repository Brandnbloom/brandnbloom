# services/local_plagiarism.py (example)
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
model = SentenceTransformer('all-MiniLM-L6-v2')  # compact embedder

# build index from your corpus (list_of_docs)
docs = ["your article 1 text", "another article text", ...]
embs = model.encode(docs, convert_to_numpy=True)
dim = embs.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embs)  # add corpus vectors

def find_similar(text, top_k=3):
    q = model.encode([text], convert_to_numpy=True)
    D, I = index.search(q, top_k)
    results = []
    for dist, idx in zip(D[0], I[0]):
        results.append({"doc": docs[idx], "score": float(dist)})
    return results
