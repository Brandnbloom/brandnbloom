# services/local_plagiarism.py

import os
import faiss
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer

"""
Local plagiarism checker using:
- SentenceTransformer embeddings
- FAISS similarity search

You can load your dataset from DB or local text files.
"""


# -----------------------------
# Load Model Once
# -----------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")  # Fast & accurate


# -----------------------------
# Corpus Management
# -----------------------------

_docs: List[str] = []      # in-memory corpus
_index = None              # FAISS index
_emb_dim = None            # embedding dimension


def load_corpus(docs: List[str]):
    """
    Load or reload the plagiarism corpus.
    Call this when server starts, or after DB update.
    """
    global _docs, _index, _emb_dim

    _docs = docs
    if not docs:
        raise ValueError("Corpus is empty. Provide at least one document.")

    embeddings = model.encode(docs, convert_to_numpy=True)

    _emb_dim = embeddings.shape[1]
    _index = faiss.IndexFlatL2(_emb_dim)
    _index.add(embeddings)

    return {"status": "loaded", "documents": len(docs)}


def add_document(doc: str):
    """
    Add one document dynamically to the existing FAISS index.
    """
    global _docs, _index

    if _index is None:
        raise RuntimeError("Index not initialized. Run load_corpus() first.")

    emb = model.encode([doc], convert_to_numpy=True)
    _index.add(emb)
    _docs.append(doc)

    return {"status": "added", "total_docs": len(_docs)}


# -----------------------------
# Similarity Search
# -----------------------------

def find_similar(text: str, top_k: int = 3) -> List[Dict]:
    """
    Returns the top-k most similar documents from the local corpus.
    """
    if _index is None:
        raise RuntimeError("Index not ready. Call load_corpus() first.")

    query_emb = model.encode([text], convert_to_numpy=True)
    distances, indices = _index.search(query_emb, top_k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        results.append({
            "doc": _docs[idx],
            "score": float(dist)  # Smaller = more similar
        })

    return results
