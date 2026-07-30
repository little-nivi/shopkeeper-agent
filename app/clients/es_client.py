

from elasticsearch import AsyncElasticsearch
from app.conf.config import ElasticsearchConfig

class ESClient:
    def __init__(self, config: ElasticsearchConfig):
        self.client = AsyncElasticsearch(hosts=[f"http://{config.host}:{config.port}"])
