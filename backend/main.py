from fastapi import FastAPI, Query
from semantic_search import SemanticSearch
from synapse_query import SynapseQuery, nl_to_sql
from typing import Dict, Any

app = FastAPI(title="Argo Conversational API")

# Initialize Semantic Search Engine
search_engine = SemanticSearch(df_file="../data/argo_profiles.pkl")

# Setup Synapse connection (Mocked for POC, uses local CSV inside SynapseQuery)
synapse = SynapseQuery(server="mock-server", database="argo", username="user", password="pass")

# --- Intelligent Hybrid Endpoint (This is the new endpoint the frontend calls) ---

@app.get("/query")
def intelligent_query(q: str = Query(...)) -> Dict[str, Any]:
    """
    The intelligent endpoint that routes the query to the correct system:
    1. NL-to-SQL (for quantitative questions like MAX/AVG)
    2. Semantic Search (for contextual/similarity questions)
    """
    q_lower = q.lower()
    
    # 1. Routing Logic (Simulating LLM's Function Calling/Tool Use)
    if any(keyword in q_lower for keyword in ["max", "min", "average", "avg", "highest", "lowest", "mean", "count"]):
        # Route to NL-to-SQL (Quantitative Question)
        nl_sql_map = nl_to_sql(q)
        sql = nl_sql_map["sql"]
        
        # Execute the (mocked but locally running) SQL
        results = synapse.run_query(sql)
        
        return {
            "query": q, 
            "mode": "NL_TO_SQL", 
            "sql_intent": nl_sql_map["type"],
            "sql": sql, 
            "results": results
        }
    else:
        # Route to Semantic Search (Contextual/Similarity Question)
        results = search_engine.search(q)
        return {
            "query": q, 
            "mode": "SEMANTIC_SEARCH", 
            "results": results
        }

# The old /semantic and /sql endpoints are removed to focus on the new /query endpoint.