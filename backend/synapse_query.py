import pandas as pd
import re
from typing import Dict, Any, List

# Load the CSV data once when the script starts for fast local execution simulation
try:
    df_data = pd.read_csv("../data/argo_profiles.csv")
    df_data['date'] = '2021-07-14'
except FileNotFoundError:
    print("Warning: argo_profiles.csv not found. Using mock data for SynapseQuery.")
    df_data = pd.DataFrame({
        'pres': [10.0, 50.0, 100.0, 200.0, 300.0],
        'temp': [3.738, 2.933, 2.256, 1.853, 1.297],
        'psal': [34.256, 34.922, 34.934, 34.933, 34.916],
        'date': ['2021-07-14'] * 5
    })

class SynapseQuery:
    """Mock class to simulate a Synapse query runner using a local Pandas DataFrame."""
    def __init__(self, *args, **kwargs):
        pass # Mocking connection

    def run_query(self, sql: str) -> List[Dict[str, Any]]:
        """Executes a simple mocked aggregation query (MAX or AVG)."""
        match_max = re.search(r"MAX\((\w+)\)", sql, re.IGNORECASE)
        match_avg = re.search(r"AVG\((\w+)\)", sql, re.IGNORECASE)
        
        if match_max:
            col = match_max.group(1).lower()
            if col in df_data.columns:
                max_val = df_data[col].max()
                return [{"value": round(max_val, 3), "parameter": col, "aggregation": "MAX"}]
        
        if match_avg:
            col = match_avg.group(1).lower()
            if col in df_data.columns:
                avg_val = df_data[col].mean()
                return [{"value": round(avg_val, 3), "parameter": col, "aggregation": "AVG"}]
        
        # Fallback for general SELECT
        cols = ['pres', 'temp', 'psal']
        return df_data[cols].head(5).to_dict(orient="records")


# Enhanced NL→SQL mapping for the router (simulates LLM translation)
def nl_to_sql(query: str) -> Dict[str, str]:
    q_lower = query.lower()
    
    if "max temperature" in q_lower or "highest temperature" in q_lower:
        return {"sql": "SELECT MAX(temp) FROM argo_profiles WHERE pres < 100;", "type": "max_temp"}
    
    if "average salinity" in q_lower or "mean salinity" in q_lower or "avg salinity" in q_lower:
        return {"sql": "SELECT AVG(psal) FROM argo_profiles WHERE pres BETWEEN 10 AND 300;", "type": "avg_salinity"}
    
    if "max salinity" in q_lower or "highest salinity" in q_lower:
        return {"sql": "SELECT MAX(psal) FROM argo_profiles;", "type": "max_salinity"}
    
    return {"sql": "SELECT TOP 5 * FROM argo_profiles;", "type": "select_all"}