import faiss
import pandas as pd
import os
from sentence_transformers import SentenceTransformer, CrossEncoder
from datetime import datetime, timedelta
import numpy as np

# Paths
INDEX_PATH = os.path.expanduser("~/astro-knowledge-assistant/data/processed/faiss.index")
META_PATH = os.path.expanduser("~/astro-knowledge-assistant/data/processed/faiss_meta.pkl")

# Load models
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
reranker_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
index = faiss.read_index(INDEX_PATH)
documents = pd.read_pickle(META_PATH)

def is_recent(date_str, days=14, is_sep=False):
    window = 30 if is_sep else days
    if not date_str or date_str in ["N/A", "0000-00-00"]: 
        return True 
    try:
        clean_date = str(date_str).split('T')[0]
        doc_date = datetime.strptime(clean_date, "%Y-%m-%d")
        # STRICT FILTER: Must be within the window relative to 'today' (2026-03-16)
        # For testing, we use 2026-03-16 as 'now'
        simulated_now = datetime(2026, 3, 16) 
        return doc_date >= simulated_now - timedelta(days=window)
    except:
        return False

def detect_event_type(query):
    q = query.lower()
    if "flare" in q: return "FLR"
    if "cme" in q or "coronal" in q: return "CME"
    if "sep" in q or "radiation" in q or "particle" in q: return "SEP"
    if "storm" in q or "geomagnetic" in q or "kp" in q: return "GST"
    return None

def get_confidence_label(score):
    if score >= 0.8: return "HIGH"
    if score >= 0.6: return "MEDIUM"
    return "LOW"

def rerank(query, candidates):
    if not candidates: return []
    pairs = [[query, c["text"]] for c in candidates]
    scores = reranker_model.predict(pairs)
    
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    for i, score in enumerate(scores):
        candidates[i]["rerank_score"] = float(sigmoid(score))
    
    return sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)

def retrieve(query, k=5):
    event_type = detect_event_type(query)
    use_recent_filter = any(w in query.lower() for w in ["recent", "latest", "today", "briefing", "active"])

    query_embedding = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(query_embedding)

    # Search candidates
    distances, indices = index.search(query_embedding, 40)
    candidates = []

    for i, idx in enumerate(indices[0]):
        if idx >= len(documents): continue
        doc = documents[idx]
        meta = doc["metadata"]
        
        is_sep = meta.get("event_type") == "SEP"
        if event_type and meta.get("event_type") != event_type:
            continue
            
        if use_recent_filter and not is_recent(meta.get("date"), is_sep=is_sep):
            continue

        candidates.append({
            "text": doc["text"],
            "metadata": meta,
            "date": meta.get("date", "0000-00-00")
        })

    if not candidates:
        return "⚠️ No relevant recent results found."

    # Rerank top candidates
    results = rerank(query, candidates)
    
    top_score = results[0]["rerank_score"]
    confidence = get_confidence_label(top_score)

    formatted = [f"--- Found {len(results)} relevant events ---\n"]
    for r in results[:k]:
        # Cleaned up format to avoid double-printing source/date
        formatted.append(f"[Score: {r['rerank_score']:.2f}] {r['text']}")
    
    formatted.append(f"\n🔎 Retrieval confidence: {confidence}")
    return "\n".join(formatted)