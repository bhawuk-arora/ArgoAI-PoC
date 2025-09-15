import os
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Ensure data directory exists
os.makedirs("./data", exist_ok=True)

# Load CSV
df = pd.read_csv("./data/argo_profiles.csv")

# Create summary column
df['summary'] = df.apply(
    lambda row: f"Salinity {row['psal']} at depth {row['pres']} and temperature {row['temp']}",
    axis=1
)

# Create embeddings with batching (safer for large files)
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(
    df['summary'].tolist(),
    batch_size=64,
    show_progress_bar=True
)

# Create FAISS index
d = embeddings.shape[1]
index = faiss.IndexFlatL2(d)
index.add(np.array(embeddings).astype('float32'))

# Save index and dataframe in ./data folder
faiss.write_index(index, "./data/faiss_index.idx")
df.to_pickle("./data/argo_profiles.pkl")

# Verify save
print("FAISS index created with", len(df), "rows")
print("Files saved in ./data:", os.listdir("./data"))
