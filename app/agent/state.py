
from typing import TypedDict, List, Optional, Dict, Any, Annotated
import operator

class QueryState(TypedDict):
    user_query: str
    keywords: List[str]
    column_info: List[Dict[str, Any]]
    metric_info: List[Dict[str, Any]]
    value_info: List[Dict[str, Any]]
    merged_context: Dict[str, Any]
    filtered_context: Dict[str, Any]
    generated_sql: str
    validated_sql: Optional[str]
    execution_result: Optional[Dict[str, Any]]
    error: Optional[str]
    progress: Annotated[List[str], operator.add]
