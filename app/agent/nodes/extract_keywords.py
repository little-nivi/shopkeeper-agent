
import jieba
from typing import Any, Dict

async def extract_keywords(state: Dict[str, Any]) -> Dict[str, Any]:
    query = state["user_query"]
    keywords = list(jieba.cut_for_search(query))
    keywords = [kw.strip() for kw in keywords if kw.strip() and len(kw) > 1]
    
    stop_words = ["统计", "查询", "的", "是", "在", "和", "与", "或", "有", "了", "我", "你", "他"]
    keywords = [kw for kw in keywords if kw not in stop_words]
    
    return {"keywords": keywords, "progress": ["已抽取关键词"]}
