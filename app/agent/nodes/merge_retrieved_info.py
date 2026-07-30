
from typing import Any, Dict

async def merge_retrieved_info(state: Dict[str, Any]) -> Dict[str, Any]:
    merged = {
        "columns": state["column_info"],
        "metrics": state["metric_info"],
        "values": state["value_info"]
    }
    return {"merged_context": merged, "progress": ["已合并召回信息"]}
