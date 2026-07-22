from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware # <--- NEW IMPORT
from semantic_search import SemanticSearch
from synapse_query import SynapseQuery, nl_to_sql
from typing import Dict, Any

app = FastAPI(title="Argo Conversational API")

# --- CORS FIX: Add Middleware ---
origins = [
    "*",  # For a local POC, allow all origins (local file system, localhost, etc.)
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow GET, POST, etc.
    allow_headers=["*"],  # Allow all headers
)
# --- END CORS FIX ---

search_engine = SemanticSearch(df_file="../data/argo_profiles.pkl")

synapse = SynapseQuery(server="mock-server", database="argo", username="user", password="pass")

@app.get("/query")
def intelligent_query(q: str = Query(...)) -> Dict[str, Any]:
    """
    The intelligent endpoint that routes the query to the correct system:
    1. NL-to-SQL (for quantitative questions like MAX/AVG)
    2. Semantic Search (for contextual/similarity questions)
    """
    q_lower = q.lower()
    
    if any(keyword in q_lower for keyword in ["max", "min", "average", "avg", "highest", "lowest", "mean", "count"]):
        nl_sql_map = nl_to_sql(q)
        sql = nl_sql_map["sql"]
        
        results = synapse.run_query(sql)
        
        return {
            "query": q, 
            "mode": "NL_TO_SQL", 
            "sql_intent": nl_sql_map["type"],
            "sql": sql, 
            "results": results
        }
    else:
        results = search_engine.search(q)
        return {
            "query": q, 
            "mode": "SEMANTIC_SEARCH", 
            "results": results
        }

# Mount static files for the frontend
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")