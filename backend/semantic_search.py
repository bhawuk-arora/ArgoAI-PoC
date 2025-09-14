import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer

class SemanticSearch:
    def __init__(self, csv_file: str, index_file: str = "vectorstore/argo_index.faiss"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.csv_file = csv_file
        self.index_file = index_file
        self.df = pd.read_csv(csv_file)

        # Build index if not exists
        self.embeddings = self.model.encode(self.df.astype(str).apply(lambda x: " ".join(x), axis=1))
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(self.embeddings)

    def search(self, query: str, top_k: int = 5):
        q_emb = self.model.encode([query])
        D, I = self.index.search(q_emb, top_k)
        results = self.df.iloc[I[0]].to_dict(orient="records")
        return results
