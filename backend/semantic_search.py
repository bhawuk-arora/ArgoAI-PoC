import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticSearch:
    def __init__(self, index_file: str = "../data/faiss_index.idx", df_file: str = "../data/argo_profiles.pkl"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.read_index(index_file)
        self.df = pd.read_pickle(df_file)

    def search(self, query: str, top_k: int = 5):
        query_vec = self.model.encode([query]).astype('float32')
        D, I = self.index.search(query_vec, top_k)
        results = self.df.iloc[I[0]].to_dict(orient="records")
        return results

if __name__ == "__main__":
    engine = SemanticSearch()
    query = "high salinity near surface"
    results = engine.search(query)
    print(results)
