
from typing import Any, Dict
import re
from sqlalchemy import text

async def validate_sql(state: Dict[str, Any], service: Any) -> Dict[str, Any]:
    sql = state["generated_sql"].strip()
    
    # 去除末尾的分号（SQL 末尾分号是合法的）
    sql = sql.rstrip(";").strip()
    
    # 检查是否包含多条语句（SQL 注入风险）
    if ";" in sql:
        return {"error": "SQL 包含多条语句（分号），疑似 SQL 注入", "validated_sql": None, "progress": ["SQL 校验失败"]}
    
    # 使用词边界检查危险关键字，避免误判（如 update_time 列名）
    dangerous_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "SLEEP"]
    sql_upper = sql.upper()
    for keyword in dangerous_keywords:
        # \b 表示词边界，确保匹配的是完整单词
        if re.search(rf"\b{keyword}\b", sql_upper):
            return {"error": f"SQL 包含危险操作: {keyword}", "validated_sql": None, "progress": ["SQL 校验失败"]}
    
    # 检查 SQL 注释（可能用于注入）
    if "--" in sql or "/*" in sql:
        return {"error": "SQL 包含注释，疑似 SQL 注入", "validated_sql": None, "progress": ["SQL 校验失败"]}
    
    try:
        async for session in service.dw_mysql.get_session():
            await session.execute(text(f"EXPLAIN {sql}"))
        return {"validated_sql": sql, "progress": ["SQL 校验通过"]}
    except Exception as e:
        return {"error": str(e), "validated_sql": None, "progress": ["SQL 校验失败"]}
