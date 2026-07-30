
import requests
from app.conf.config import EmbeddingConfig

class EmbeddingClient:
    def __init__(self, config: EmbeddingConfig):
        self.base_url = f"http://{config.host}:{config.port}"
        self.model = config.model

    def embed(self, texts: list[str]) -> list[list[float]]:
        response = requests.post(
            f"{self.base_url}/embed",
            json={"inputs": texts, "model": self.model}
        )
        return response.json()
