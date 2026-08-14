import urllib.request
import json
from typing import List

class OllamaEmbedder:
    """
    Klient do pobierania w locie wektorów osadzających (embeddings) 
    z lokalnego modelu (np. mxbai-embed-large).
    """
    def __init__(self, model_name: str = "mxbai-embed-large:latest", endpoint: str = "http://localhost:11434/api/embeddings"):
        self.model_name = model_name
        self.endpoint = endpoint

    def get_embedding(self, text: str) -> List[float]:
        if not text or not text.strip():
            return []
            
        payload = {
            "model": self.model_name,
            "prompt": text
        }
        
        try:
            req = urllib.request.Request(
                self.endpoint,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get("embedding", [])
        except Exception as e:
            print(f"[EMBEDDER] Błąd pobierania wektora: {e}")
            return []
