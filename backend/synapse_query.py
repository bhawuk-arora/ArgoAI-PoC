import pandas as pd
import re
from typing import Dict, Any, List

# For prototype simplicity, we load the CSV directly to simulate query execution
try:
    # Load the data, assuming the file path is correct
    df_data = pd.read_csv("../data/argo_profiles.csv")
    # Add a dummy date column for the NL-to-SQL output to be realistic
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
        # Mocking connection setup
        pass

    def run_query(self, sql: str) -> List[Dict[str, Any]]:
        """Executes a simple mocked query (currently only supports MAX on a column)."""
        match = re.search(r"MAX\((\w+)\)", sql, re.IGNORECASE)
        
        if match:
            col = match.group(1).lower()
            if col in df_data.columns:
                # Mock a result for an aggregation query
                max_val = df_data[col].max()
                return [{"max_value": max_val, "parameter": col}]
        
        # Fallback for simple SELECT queries (if routing fails)
        cols = ['pres', 'temp', 'psal', 'date']
        return df_data[cols].head(5).to_dict(orient="records")


# Enhanced NL→SQL mapping (prototype only) to produce a "SQL" query
def nl_to_sql(query: str) -> Dict[str, str]:
    q_lower = query.lower()
    
    # Complex/Quantitative Queries (to show LLM intelligence)
    if "max temperature" in q_lower or "highest temperature" in q_lower:
        return {"sql": "SELECT MAX(temp) FROM argo_profiles WHERE pres < 100;", "type": "max_temp"}
    
    if "average salinity" in q_lower or "mean salinity" in q_lower:
        # Note: run_query is simplified, but this SQL shows the correct intention
        return {"sql": "SELECT AVG(psal) FROM argo_profiles WHERE pres BETWEEN 100 AND 300;", "type": "avg_salinity"}
    
    # Default simple selection query
    return {"sql": "SELECT TOP 5 * FROM argo_profiles;", "type": "select_all"}