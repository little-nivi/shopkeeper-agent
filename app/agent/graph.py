from langgraph.graph import StateGraph, END
from app.agent.state import QueryState
from app.agent.nodes.extract_keywords import extract_keywords
from app.agent.nodes.recall_column import recall_column
from app.agent.nodes.recall_metric import recall_metric
from app.agent.nodes.recall_value import recall_value
from app.agent.nodes.merge_retrieved_info import merge_retrieved_info
from app.agent.nodes.filter_context import filter_context
from app.agent.nodes.generate_sql import generate_sql
from app.agent.nodes.validate_sql import validate_sql
from app.agent.nodes.execute_sql import execute_sql
from typing import Any
"""
本次未添加任何东西，仅为测试pr
"""
def build_query_graph(service: Any = None):
    workflow = StateGraph(QueryState)
    
    def wrap_node(node_func):
        if service is None:
            return node_func
        def wrapped(state: QueryState):
            return node_func(state, service)
        wrapped.__name__ = node_func.__name__
        return wrapped
    
    def wrap_node_async(node_func):
        if service is None:
            return node_func
        async def wrapped(state: QueryState):
            return await node_func(state, service)
        wrapped.__name__ = node_func.__name__
        return wrapped
    
    workflow.add_node("extract_keywords", extract_keywords)
    workflow.add_node("recall_column", wrap_node_async(recall_column))
    workflow.add_node("recall_metric", wrap_node_async(recall_metric))
    workflow.add_node("recall_value", wrap_node_async(recall_value))
    workflow.add_node("merge_retrieved_info", merge_retrieved_info)
    workflow.add_node("filter_context", filter_context)
    workflow.add_node("generate_sql", wrap_node_async(generate_sql))
    workflow.add_node("validate_sql", wrap_node_async(validate_sql))
    workflow.add_node("execute_sql", wrap_node_async(execute_sql))
    
    workflow.set_entry_point("extract_keywords")
    
    workflow.add_edge("extract_keywords", "recall_column")
    workflow.add_edge("extract_keywords", "recall_metric")
    workflow.add_edge("extract_keywords", "recall_value")
    
    workflow.add_edge("recall_column", "merge_retrieved_info")
    workflow.add_edge("recall_metric", "merge_retrieved_info")
    workflow.add_edge("recall_value", "merge_retrieved_info")
    
    workflow.add_edge("merge_retrieved_info", "filter_context")
    workflow.add_edge("filter_context", "generate_sql")
    workflow.add_edge("generate_sql", "validate_sql")
    
    def validate_router(state: QueryState):
        if state["validated_sql"]:
            return "execute_sql"
        else:
            return END
    
    workflow.add_conditional_edges("validate_sql", validate_router)
    workflow.add_edge("execute_sql", END)
    
    return workflow.compile()
