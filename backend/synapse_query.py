import pyodbc

class SynapseQuery:
    def __init__(self, server, database, username, password):
        self.conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};DATABASE={database};UID={username};PWD={password}"
        )

    def run_query(self, sql: str):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cols = [col[0] for col in cursor.description]
        return [dict(zip(cols, row)) for row in rows]

# Simple NL→SQL mapping (prototype only)
def nl_to_sql(query: str):
    if "temperature" in query.lower():
        return "SELECT TOP 5 lat, lon, depth, temperature, date FROM argo_profiles;"
    if "salinity" in query.lower():
        return "SELECT TOP 5 lat, lon, depth, salinity, date FROM argo_profiles;"
    return "SELECT TOP 5 * FROM argo_profiles;"
