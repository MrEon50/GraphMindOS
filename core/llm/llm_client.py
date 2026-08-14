import urllib.request
import json
import os
from typing import List, Dict

class LLMProviderManager:
    """
    Ujednolicony menedżer dostawców LLM (Ollama + LM Studio + Google Gemini API).
    Wykrywa zainstalowane modele i dostarcza uniwersalny interfejs do wysyłania zapytania chat.
    """
    
    OLLAMA_DEFAULT_TAGS = "http://localhost:11434/api/tags"
    OLLAMA_DEFAULT_CHAT = "http://localhost:11434/api/chat"
    LMSTUDIO_DEFAULT_MODELS = "http://127.0.0.1:1234/v1/models"
    LMSTUDIO_DEFAULT_CHAT = "http://127.0.0.1:1234/v1/chat/completions"
    GEMINI_DEFAULT_CHAT = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
    GEMINI_MODELS = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"]

    def __init__(self):
        self.role_models: Dict[str, Dict[str, str]] = {}
        
    @classmethod
    def fetch_all_models(cls) -> List[Dict[str, str]]:
        """
        Pobiera listę połączonych modeli z serwerów Ollama, LM Studio oraz Google Gemini.
        Zwraca listę słowników: [{'name': '...', 'provider': 'ollama'|'lmstudio'|'gemini', 'endpoint': '...'}]
        """
        available_models = []
        
        # 1. Sprawdź Ollama (port 11434)
        try:
            req = urllib.request.Request(cls.OLLAMA_DEFAULT_TAGS, headers={'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=3) as response:
                result = json.loads(response.read().decode('utf-8'))
                for m in result.get('models', []):
                    m_name = m['name']
                    available_models.append({
                        "name": m_name,
                        "provider": "ollama",
                        "endpoint": cls.OLLAMA_DEFAULT_CHAT,
                        "is_cloud": ":cloud" in m_name
                    })
        except Exception:
            pass
            
        # 2. Sprawdź LM Studio (port 1234)
        try:
            req = urllib.request.Request(cls.LMSTUDIO_DEFAULT_MODELS, headers={'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=3) as response:
                result = json.loads(response.read().decode('utf-8'))
                for m in result.get('data', []):
                    model_id = m.get('id', 'lmstudio-model')
                    available_models.append({
                        "name": f"lmstudio:{model_id}",
                        "provider": "lmstudio",
                        "model_id": model_id,
                        "endpoint": cls.LMSTUDIO_DEFAULT_CHAT,
                        "is_cloud": False
                    })
        except Exception:
            pass

        # 3. Google Gemini API Models
        gemini_key = os.environ.get("GEMINI_API_KEY")
        for g_model in cls.GEMINI_MODELS:
            available_models.append({
                "name": f"gemini:{g_model}",
                "provider": "gemini",
                "model_id": g_model,
                "endpoint": cls.GEMINI_DEFAULT_CHAT,
                "is_cloud": True,
                "has_key": bool(gemini_key)
            })
            
        # Sortuj: modele lokalne na początku, chmurowe (:cloud / gemini) na końcu
        available_models.sort(key=lambda x: x.get('is_cloud', False))
        return available_models

    @classmethod
    def chat_completion(
        cls, 
        model_info: str | Dict[str, str], 
        system_prompt: str, 
        user_prompt: str, 
        timeout: int = 60
    ) -> str:
        """
        Wysyła zapytanie chat completion do Ollama, LM Studio lub Google Gemini i zwraca wygenerowany tekst.
        """
        if isinstance(model_info, dict):
            provider = model_info.get("provider", "ollama")
            model_name = model_info.get("model_id", model_info.get("name", "qwen3.5:9b"))
            endpoint = model_info.get("endpoint", cls.OLLAMA_DEFAULT_CHAT)
        else:
            if model_info.startswith("lmstudio:"):
                provider = "lmstudio"
                model_name = model_info.replace("lmstudio:", "")
                endpoint = cls.LMSTUDIO_DEFAULT_CHAT
            elif model_info.startswith("gemini:"):
                provider = "gemini"
                model_name = model_info.replace("gemini:", "")
                endpoint = cls.GEMINI_DEFAULT_CHAT
            else:
                provider = "ollama"
                model_name = model_info
                endpoint = cls.OLLAMA_DEFAULT_CHAT

        headers = {'Content-Type': 'application/json'}

        if provider in ["lmstudio", "gemini"]:
            if provider == "gemini":
                api_key = os.environ.get("GEMINI_API_KEY", "")
                if not api_key:
                    raise ValueError("Brak klucza API w zmiennej środowiskowej GEMINI_API_KEY.")
                headers['Authorization'] = f"Bearer {api_key}"

            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.2,
                "stream": False
            }
        else:
            # Standard Ollama API
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "stream": False
            }

        req = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers
        )

        with urllib.request.urlopen(req, timeout=timeout) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            
        if provider in ["lmstudio", "gemini"]:
            choices = res_data.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "").strip()
            return ""
        else:
            return res_data.get("message", {}).get("content", "").strip()
