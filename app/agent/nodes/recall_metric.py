
from typing import Any, Dict

async def recall_metric(state: Dict[str, Any], service: Any) -> Dict[str, Any]:
    keywords = state["keywords"]
    if not keywords:
        return {"metric_info": [], "progress": ["指标召回：无关键词"]}
    
    try:
        query_vector = service.embedding.embed([" ".join(keywords)])[0]
        
        results = service.qdrant.client.query_points(
            collection_name="metrics",
            query=query_vector,
            limit=5
        )
        
        metric_info = [hit.payload for hit in results.points]
        progress_msg = "已召回指标信息"
    except Exception as e:
        metric_info = []
        progress_msg = f"指标召回失败：{str(e)}"
    
    return {"metric_info": metric_info, "progress": [progress_msg]}
