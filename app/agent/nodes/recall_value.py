from typing import Any, Dict

async def recall_value(state: Dict[str, Any], service: Any) -> Dict[str, Any]:
    keywords = state["keywords"]
    if not keywords:
        return {"value_info": [], "progress": ["取值召回：无关键词"]}
    
    body = {
        "query": {
            "multi_match": {
                "query": " ".join(keywords),
                "fields": ["value"]
            }
        },
        "size": 10
    }
    
    try:
        results = await service.es.client.search(index="value_info", body=body)
        value_info = [hit["_source"] for hit in results["hits"]["hits"]]
    except Exception:
        value_info = []
    
    return {"value_info": value_info, "progress": ["已召回字段取值"]}
