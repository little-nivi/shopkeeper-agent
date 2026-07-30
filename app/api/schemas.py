

from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    sql: Optional[str]
    result: Optional[Dict[str, Any]]
    progress: List[str]
    error: Optional[str]
