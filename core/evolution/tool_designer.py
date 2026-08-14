import re
import time
from core.standards import get_standards_for_prompt
from core.llm.llm_client import LLMProviderManager

class ToolDesigner:
    """
    LLM-based component that autonomously generates new Primitive code
    based on user requests. It ensures the code follows the registry format.
    """
    def __init__(self, model_name: str = "qwen3.5:9b", endpoint: str = "http://localhost:11434/api/chat"):
        self.model_name = model_name
        self.endpoint = endpoint
        self.max_retries = 3
        
        standards = get_standards_for_prompt()
        self.system_prompt = f"""Napisz kod Python definiujacy nowy Atom dla systemu GraphMindOS.

Zasady:
1. Import: from core.engine.primitives import PrimitiveRegistry
2. Dekorator: @PrimitiveRegistry.register("nazwa_atoma", "Krotki opis. Przyjmuje: klucz1, klucz2.")
3. Funkcja: def nazwa(payload: dict) -> dict
4. Obsluga bledow: raise ValueError z czytelnym komunikatem (NIE zwracaj dict z error).
5. Zwroc TYLKO blok ```python ... ``` bez innego tekstu.

{standards}

Atom MUSI:
- Szukac danych pod wieloma kluczami: payload.get("filepath") or payload.get("filename") or payload.get("path")
- Rzucac ValueError na bledy, nie zwracac w dict np: {{"error": "zly"}}.
- Zwracac wynik pod standardowym kluczem"""

    def design_tool(self, description: str) -> str:
        for attempt in range(1, self.max_retries + 1):
            try:
                timeout = 60 * attempt
                print(f"[TOOL DESIGNER] Projektowanie kodu przez {self.model_name} (próba {attempt}/{self.max_retries}, timeout: {timeout}s)...")
                
                raw_code = LLMProviderManager.chat_completion(
                    model_info=self.model_name,
                    system_prompt=self.system_prompt,
                    user_prompt=f"Napisz Atom: {description}",
                    timeout=timeout
                )
                
                # Ekstrakcja kodu z blokow markdown
                match = re.search(r'```(?:python)?\s*(.*?)\s*```', raw_code, re.DOTALL)
                if match:
                    code = match.group(1).strip()
                else:
                    code = raw_code.strip()
                
                if code and "def " in code:
                    return code
                else:
                    print(f"[TOOL DESIGNER] Model nie zwrocil poprawnego kodu. Ponawiam...")
                    continue
                        
            except Exception as e:
                print(f"[TOOL DESIGNER] Błąd podczas projektowania (próba {attempt}/{self.max_retries}): {e}")
                if attempt < self.max_retries:
                    time.sleep(2 * attempt)
        
        print(f"[TOOL DESIGNER] Nie udalo sie wygenerowac kodu po {self.max_retries} probach.")
        return ""

    def validate_code(self, source_code: str) -> bool:
        """
        Walidacja bezpieczenstwa z systemem ostrzezen Human-in-the-Loop.
        Zamiast slepego blokowania, edukuje uzytkownika i pyta o decyzje.
        """
        dangerous_patterns = {
            "os.system": "Uruchamia dowolna komende systemowa bez kontroli.",
            "subprocess": "Daje pelny dostep do konsoli (CMD/PowerShell).",
            "eval(": "Wykonuje dowolny kod Python podany jako tekst.",
            "exec(": "Wykonuje dynamicznie wygenerowany kod Python.",
            "__import__": "Pozwala na dynamiczne ladowanie dowolnych modulow Pythona."
        }
        
        if "@PrimitiveRegistry.register" not in source_code:
            print("[JUDGE] Kod odrzucony: Brak wymaganego dekoratora @PrimitiveRegistry.register.")
            return False
        if "def " not in source_code:
            print("[JUDGE] Kod odrzucony: Brak definicji funkcji (def).")
            return False
        
        found_dangers = []
        for pattern, explanation in dangerous_patterns.items():
            if pattern in source_code:
                found_dangers.append((pattern, explanation))
        
        if found_dangers:
            print("\n" + "!" * 50)
            print("[JUDGE] UWAGA! WYKRYTO ELEMENTY WYMAGAJACE SWIADOMEJ DECYZJI!")
            print("!" * 50)
            for i, (pattern, explanation) in enumerate(found_dangers, 1):
                print(f"\n  {i}. '{pattern}': -> {explanation}")
            
            while True:
                choice = input("\nCzy zatwierdzasz instalacje tego kodu? [Y/N]: ").strip().lower()
                if choice in ['y', 'yes']:
                    print("[JUDGE] Uzytkownik swiadomie zatwierdzil kod.")
                    return True
                elif choice in ['n', 'no']:
                    print("[JUDGE] Uzytkownik odmowil. Kod zostal odrzucony.")
                    return False
                else:
                    print("[!] Wpisz Y lub N.")
        
        return True
