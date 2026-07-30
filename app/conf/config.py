
from dataclasses import dataclass, field
from omegaconf import OmegaConf
from typing import Dict, Any

@dataclass
class LoggingConfig:
    file: Dict[str, Any] = field(default_factory=dict)
    console: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 3306
    user: str = ""
    password: str = ""
    database: str = ""

@dataclass
class QdrantConfig:
    host: str = "localhost"
    port: int = 6333
    embedding_size: int = 1024

@dataclass
class EmbeddingConfig:
    host: str = "localhost"
    port: int = 8081
    model: str = ""

@dataclass
class ElasticsearchConfig:
    host: str = "localhost"
    port: int = 9200

@dataclass
class LLMConfig:
    provider: str = ""
    api_key: str = ""
    model: str = ""
    base_url: str = ""
    temperature: float = 0.1

@dataclass
class AppConfig:
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    db_meta: DatabaseConfig = field(default_factory=DatabaseConfig)
    db_dw: DatabaseConfig = field(default_factory=DatabaseConfig)
    qdrant: QdrantConfig = field(default_factory=QdrantConfig)
    embedding: EmbeddingConfig = field(default_factory=EmbeddingConfig)
    elasticsearch: ElasticsearchConfig = field(default_factory=ElasticsearchConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)

def load_config(path: str = "conf/app_config.yaml") -> AppConfig:
    conf = OmegaConf.load(path)
    return conf #OmegaConf.to_object(conf)
