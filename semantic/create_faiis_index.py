import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# Load CSV
df = pd.read_csv("../data/argo_profiles.csv")

# Create a text summary for each row
df['summary'] = df.apply(lambda row: f"Salinity {row['salinity']} at depth {row['depth']} and temperature {row['temperature']}", axis=1)

# Create embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(df['summary'].tolist())

# Create FAISS index
d = embeddings.shape[1]
index = faiss.IndexFlatL2(d)
index.add(np.array(embeddings).astype('float32'))

# Save index and dataframe
faiss.write_index(index, "../data/faiss_index.idx")
df.to_pickle("../data/argo_profiles.pkl")

print("FAISS index created with", len(df), "rows")
