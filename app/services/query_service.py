
from app.agent.graph import build_query_graph
from app.clients.mysql_client import MySQLClient
from app.clients.qdrant_client import QdrantClientWrapper
from app.clients.es_client import ESClient
from app.clients.embedding_client import EmbeddingClient
from app.conf.config import load_config
from langchain_deepseek import ChatDeepSeek

class QueryService:
    def __init__(self):
        config = load_config()
        
        self.meta_mysql = MySQLClient(config.db_meta)
        self.dw_mysql = MySQLClient(config.db_dw)
        self.qdrant = QdrantClientWrapper(config.qdrant)
        self.es = ESClient(config.elasticsearch)
        self.embedding = EmbeddingClient(config.embedding)
        
        self.llm = ChatDeepSeek(
            model=config.llm.model,
            api_key=config.llm.api_key,
            base_url=config.llm.base_url
        )
        
        self.graph = build_query_graph(self)
    
    async def run_query(self, query: str):
        initial_state = {
            "user_query": query,
            "keywords": [],
            "column_info": [],
            "metric_info": [],
            "value_info": [],
            "merged_context": {},
            "filtered_context": {},
            "generated_sql": "",
            "validated_sql": None,
            "execution_result": None,
            "error": None,
            "progress": []
        }
        
        async for state in self.graph.astream(initial_state, stream_mode="values"):
            yield state
