from typing import Any, Dict
from decimal import Decimal
from datetime import datetime, date
from sqlalchemy import text


def convert_value(v):
    """将 MySQL 返回的不支持 JSON 序列化的类型转换为兼容类型"""
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, (datetime, date)):
        return v.isoformat()
    return v


async def execute_sql(state: Dict[str, Any], service: Any) -> Dict[str, Any]:
    sql = state["validated_sql"]

    try:
        async for session in service.dw_mysql.get_session():
            result = await session.execute(text(sql))
            rows = result.fetchall()
            columns = result.keys()

        return {
            "execution_result": {
                "columns": list(columns),
                "data": [
                    {col: convert_value(val) for col, val in row._mapping.items()}
                    for row in rows
                ],
            },
            "progress": ["SQL 执行完成"],
        }
    except Exception as e:
        return {"error": str(e), "execution_result": None, "progress": ["SQL 执行失败"]}
