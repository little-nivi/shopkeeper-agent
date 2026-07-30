
from typing import Any, Dict

async def generate_sql(state: Dict[str, Any], service: Any) -> Dict[str, Any]:
    filtered = state["filtered_context"]
    query = state["user_query"]
    
    columns_text = "\n".join([
        f"- {col.get('name', '')}: {col.get('description', '')} (表: {col.get('table_name', '')})"
        for col in filtered["columns"]
    ])
    
    metrics_text = "\n".join([
        f"- {metric.get('name', '')}: {metric.get('description', '')}"
        for metric in filtered["metrics"]
    ])
    
    values_text = "\n".join([
        f"- {val.get('value', '')} (字段: {val.get('column_id', '')})"
        for val in filtered["values"]
    ])
    
    prompt = f"""
你是一个专业的 SQL 生成助手。请根据以下信息，为用户的问题生成正确的 SQL 查询语句。

用户问题：{query}

可用的表和字段：
{columns_text}

可用的指标：
{metrics_text}

字段取值：
{values_text}

数据库是 MySQL，包含以下表：
- fact_order (订单事实表): order_id, customer_id, product_id, region_id, date_id, order_amount, order_quantity
- dim_customer (客户维度表): customer_id, customer_name, gender, member_level
- dim_date (时间维度表): date_id, day, month, quarter, year
- dim_product (商品维度表): product_id, product_name, brand, category
- dim_region (地区维度表): region_id, region_name, province, country

请生成正确的 SQL 查询，只返回 SQL 语句，不要包含任何其他文字。
"""
    
    response = await service.llm.ainvoke(prompt)
    sql = response.content.strip()
    
    if "```sql" in sql:
        sql = sql.split("```sql")[1].split("```")[0].strip()
    elif "```" in sql:
        sql = sql.split("```")[1].split("```")[0].strip()
    
    return {"generated_sql": sql, "progress": ["已生成 SQL"]}
