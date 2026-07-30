
from typing import Any, Dict

async def recall_column(state: Dict[str, Any], service: Any) -> Dict[str, Any]:
    keywords = state["keywords"]
    if not keywords:
        return {"column_info": [], "progress": ["字段召回：无关键词"]}
    
    try:
        query_vector = service.embedding.embed([" ".join(keywords)])[0]
        
        results = service.qdrant.client.query_points(
            collection_name="columns",
            query=query_vector,
            limit=10
        )
        
        column_info = [hit.payload for hit in results.points]
        progress_msg = "已召回字段信息"
    except Exception as e:
        column_info = []
        progress_msg = f"字段召回失败：{str(e)}"
    
    return {"column_info": column_info, "progress": [progress_msg]}
