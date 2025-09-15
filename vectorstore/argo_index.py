import os
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Ensure data directory exists
os.makedirs("./data", exist_ok=True)

# Load CSV
df = pd.read_csv("./data/argo_profiles.csv")

# Use correct column names from ETL (they are lowercase)
df['summary'] = df.apply(
    lambda row: f"Salinity {row['psal']} at depth {row['pres']} and temperature {row['temp']}",
    axis=1
)

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
