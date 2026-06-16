import numpy as np
import faiss
import os
import pandas as pd
from sentence_transformers import SentenceTransformer

DOC_PATH = os.path.expanduser(
    "~/astro-knowledge-assistant/data/processed/documents.pkl"
)

INDEX_PATH = os.path.expanduser(
    "~/astro-knowledge-assistant/data/processed/faiss.index"
)

META_PATH = os.path.expanduser(
    "~/astro-knowledge-assistant/data/processed/faiss_meta.pkl"
)


def build_vector_store():
    documents = pd.read_pickle(DOC_PATH)

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    texts = [doc["text"] for doc in documents]

    embeddings = model.encode(texts, convert_to_numpy=True)

    #normalize for cosine similarity
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)
    pd.to_pickle(documents, META_PATH)

    print("✅ Vector DB created")


if __name__ == "__main__":
    build_vector_store()