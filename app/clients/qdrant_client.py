
from qdrant_client import QdrantClient
from app.conf.config import QdrantConfig

class QdrantClientWrapper:
    def __init__(self, config: QdrantConfig):
        self.client = QdrantClient(host=config.host, port=config.port)
        self.embedding_size = config.embedding_size
