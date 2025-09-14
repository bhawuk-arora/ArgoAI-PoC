from fastapi import FastAPI, Query
from semantic_search import SemanticSearch
from synapse_query import SynapseQuery, nl_to_sql

app = FastAPI(title="Argo Conversational API")

# Load semantic search
search_engine = SemanticSearch("data/argo_profiles.csv")

# Setup Synapse connection (dummy for now, replace creds)
# synapse = SynapseQuery(server="your-server", database="argo", username="user", password="pass")

@app.get("/semantic")
def semantic_search(q: str = Query(...)):
    results = search_engine.search(q)
    return {"query": q, "results": results}

@app.get("/sql")
def sql_query(q: str = Query(...)):
    sql = nl_to_sql(q)
    # results = synapse.run_query(sql)
    results = {"message": f"Would run SQL: {sql}"}  # Mocked for demo
    return {"query": q, "sql": sql, "results": results}
