import re

class IntentPreProcessor:
    """
    Warstwa tlumaczenia potocznego jezyka na precyzyjny cel techniczny.
    Posiada smart-bypass: jesli intencja jest juz precyzyjna, nie traci czasu na LLM.
    """
    def __init__(self, model_name: str = "qwen3.5:9b", endpoint: str = "http://localhost:11434/api/chat"):
        self.model_name = model_name
        self.endpoint = endpoint
        self.system_prompt = """Przetlumacz potoczna prosbe na krotki, precyzyjny plan techniczny.
Jesli prosba jest juz konkretna, zwroc ja bez zmian.
Zwroc TYLKO tekst instrukcji, bez JSON."""

    def _is_already_precise(self, intent: str) -> bool:
        """Sprawdza czy intencja jest juz wystarczajaco precyzyjna (nie wymaga LLM)."""
        # Sciezki plikow (Windows/Linux)
        if re.search(r'[A-Za-z]:\\|/home/|/usr/|\\\\|workspace/', intent):
            return True
        # Nazwy istniejacych narzedzi
        from core.engine.primitives import PrimitiveRegistry
        for tool_name in PrimitiveRegistry._registry.keys():
            if tool_name.lower() in intent.lower():
                return True
        # Komendy techniczne
        tech_keywords = ["odczytaj", "zapisz", "usun", "skopiuj", "przenies", 
                         "spakuj", "wylistuj", "uruchom", "pobierz", "wyslij",
                         "read_file", "write_file", "cmd_executor", "zip_archiver"]
        if any(kw in intent.lower() for kw in tech_keywords):
            return True
        return False

    def process(self, raw_intent: str) -> str:
        # Smart bypass - nie traci 30s na LLM dla precyzyjnych polecen
        if self._is_already_precise(raw_intent):
            print(f"[PRE-PROCESSOR] Intencja jest precyzyjna - przekazuje bez tlumaczenia.")
            return raw_intent
        
        from core.llm.llm_client import LLMProviderManager
        
        try:
            print(f"[PRE-PROCESSOR] Interpretowanie potocznego języka za pomocą {self.model_name}...")
            processed = LLMProviderManager.chat_completion(
                model_info=self.model_name,
                system_prompt=self.system_prompt,
                user_prompt=raw_intent,
                timeout=30
            )
            if processed:
                print(f"[PRE-PROCESSOR] Przetłumaczono na: '{processed[:100]}...'")
                return processed
            return raw_intent
        except Exception as e:
            print(f"[PRE-PROCESSOR] Fallback z powodu błędu: {e}")
            return raw_intent

