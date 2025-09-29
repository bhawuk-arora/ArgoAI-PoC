from fastapi import FastAPI, Query
from semantic_search import SemanticSearch
from synapse_query import SynapseQuery, nl_to_sql
from typing import Dict, Any

app = FastAPI(title="Argo Conversational API")

search_engine = SemanticSearch(df_file="../data/argo_profiles.pkl")

# Setup Synapse connection (mocked for the POC video, uses local CSV internally)
synapse = SynapseQuery(server="mock-server", database="argo", username="user", password="pass")

# --- Intelligent Hybrid Endpoint (New Focus) ---

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
        
        # Execute the (mocked) SQL
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

# --- Legacy Endpoints (Kept for completeness, but should be ignored in the demo) ---

@app.get("/semantic")
def semantic_search(q: str = Query(...)):
    results = search_engine.search(q)
    return {"query": q, "mode": "SEMANTIC_SEARCH", "results": results}

@app.get("/sql")
def sql_query(q: str = Query(...)):
    nl_sql_map = nl_to_sql(q)
    sql = nl_sql_map["sql"]
    results = synapse.run_query(sql)
    return {"query": q, "mode": "NL_TO_SQL", "sql": sql, "results": results}