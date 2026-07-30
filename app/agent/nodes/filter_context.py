
from typing import Any, Dict

async def filter_context(state: Dict[str, Any]) -> Dict[str, Any]:
    merged = state["merged_context"]
    
    filtered_columns = []
    for col in merged["columns"]:
        if col.get("relevance", 0.5) > 0.3:
            filtered_columns.append(col)
    
    filtered_metrics = []
    for metric in merged["metrics"]:
        if metric.get("relevance", 0.5) > 0.3:
            filtered_metrics.append(metric)
    
    filtered = {
        "columns": filtered_columns,
        "metrics": filtered_metrics,
        "values": merged["values"]
    }
    
    return {"filtered_context": filtered, "progress": ["已过滤上下文"]}
