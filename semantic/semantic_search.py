import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np

# Load index and data
index = faiss.read_index("../data/faiss_index.idx")
df = pd.read_pickle("../data/argo_profiles.pkl")

# Model
model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_search(query, k=5):
    query_vec = model.encode([query]).astype('float32')
    D, I = index.search(query_vec, k)
    results = df.iloc[I[0]]
    return results

# Demo
query = "high salinity near surface"
results = semantic_search(query)
print(results)
