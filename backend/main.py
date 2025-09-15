from fastapi import FastAPI, Query
from semantic_search import SemanticSearch
from synapse_query import SynapseQuery, nl_to_sql

app = FastAPI(title="Argo Conversational API")

search_engine = SemanticSearch(df_file="../data/argo_profiles.pkl")

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
    results = {"message": f"Would run SQL: {sql}"}  # Dhyan dijiye
    return {"query": q, "sql": sql, "results": results}