from pydantic import BaseModel
from typing import Any, List

class ResultResponse(BaseModel):
    query: str
    results: List[Any]
