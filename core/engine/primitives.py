from typing import Callable, Dict, Any
import os
import urllib.request
import urllib.error
import json
import importlib.util
import sys
from bs4 import BeautifulSoup

class PrimitiveRegistry:
    """
    Rejestr 'Atomów Wykonawczych' (Execution Primitives).
    Są to gotowe funkcje (czarne skrzynki) przypisywane do węzłów w grafie.
    Węzeł definiuje: execution.processor_ref = 'fetch_weather' a Rejestr go znajduje.
    """
    
    _registry: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}
    _descriptions: Dict[str, str] = {} # UPG-3: Opisy narzedzi dla AI
    _origins: Dict[str, str] = {} # Sledzenie pochodzenia: CORE / DYNAMIC

    @classmethod
    def register(cls, name: str, description: str = "", origin: str = "CORE"):
        def wrapper(func):
            cls._registry[name] = func
            cls._descriptions[name] = description or func.__doc__ or "Brak opisu."
            if name not in cls._origins:
                cls._origins[name] = origin
            return func
        return wrapper

    @classmethod
    def execute(cls, ref: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if ref not in cls._registry:
            raise KeyError(f"Primitive Atom '{ref}' not found in registry!")
            
        print(f"[REJESTR] Executing registered primitive: {ref}")
        try:
            return cls._registry[ref](payload)
        except Exception as e:
            print(f"[REJESTR] Error in '{ref}': {e}")
            raise e

    @classmethod
    def unregister(cls, name: str) -> dict:
        """Usuwa dynamiczny Atom z rejestru i kasuje jego plik zrodlowy."""
        if name not in cls._registry:
            return {"success": False, "reason": f"Atom '{name}' nie istnieje w rejestrze."}
        
        origin = cls._origins.get(name, "CORE")
        if origin == "CORE":
            return {"success": False, "reason": f"Atom '{name}' jest wbudowany [CORE] i nie moze byc usuniety."}
        
        # Usun z rejestru w pamieci
        del cls._registry[name]
        cls._descriptions.pop(name, None)
        cls._origins.pop(name, None)
        
        # Znajdz i usun plik zrodlowy z dynamic_atoms
        dynamic_dir = os.path.abspath(os.path.join(os.getcwd(), "workspace", "dynamic_atoms"))
        deleted_file = None
        if os.path.exists(dynamic_dir):
            for filename in os.listdir(dynamic_dir):
                if filename.endswith(".py"):
                    filepath = os.path.join(dynamic_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        if f'"{name}"' in content or f"'{name}'" in content:
                            os.remove(filepath)
                            deleted_file = filename
                            break
                    except Exception:
                        pass
        
        return {"success": True, "deleted_file": deleted_file}

    @classmethod
    def load_dynamic_atoms(cls):
        """Hot-Swap ładowanie customowych atomów usera."""
        dynamic_dir = os.path.abspath(os.path.join(os.getcwd(), "workspace", "dynamic_atoms"))
        if not os.path.exists(dynamic_dir):
            os.makedirs(dynamic_dir)
            return
            
        count = 0
        for filename in os.listdir(dynamic_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                file_path = os.path.join(dynamic_dir, filename)
                module_name = f"dynamic_atom_{filename[:-3]}"
                
                # Zapamietaj stanu rejestru PRZED ladowaniem
                before_keys = set(cls._registry.keys())
                
                # Dynamiczny load modulu do pythonsys
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    try:
                        spec.loader.exec_module(module)
                        count += 1
                        
                        # Oznacz nowe atomy jako DYNAMIC
                        new_keys = set(cls._registry.keys()) - before_keys
                        for key in new_keys:
                            cls._origins[key] = "DYNAMIC"
                            
                    except Exception as e:
                        print(f"[LOADER ERROR] Nie udalo sie zaladowac Atoma z pliku '{filename}': {e}")
                        
        if count > 0:
            print(f"[TOOL LOADER]: Pomyslnie zaladowano {count} dynamicznych autorskich Atomow do rdzenia OS!")

# --- Przykładowe Atomy dla testów demówki ---

@PrimitiveRegistry.register("calculate_salary", "Oblicza pensję na podstawie godzin i stawki. Wymaga: hours, rate_per_hour.")
def calculate_salary(payload: dict) -> dict:
    hours = payload.get("hours", payload.get("hours_worked"))
    rate = payload.get("rate_per_hour", payload.get("hourly_rate"))
    
    if hours is None or rate is None:
        raise ValueError(f"CRITICAL: Atom 'calculate_salary' wymaga w payloadzie kluczy: 'hours' oraz 'rate_per_hour', otrzymano: {list(payload.keys())}")
        
    salary = hours * rate
    print(f">> [PRIMITIVE PAYROLL]: Calculated Salary: {salary} <<")
    return {"result": salary}

@PrimitiveRegistry.register("log_message", "Loguje wiadomość tekstową do konsoli systemowej. Wymaga: message.")
def log_message(payload: dict) -> dict:
    msg = payload.get("message", "No message provided")
    print(f">> [PRIMITIVE LOG]: {msg} <<")
    return {"logged": True, "message_length": len(msg)}

@PrimitiveRegistry.register("ai_chat", "Zwraca bezpośrednią, przyjazną odpowiedź konwersacyjną AI. Wymaga: message.")
def ai_chat(payload: dict) -> dict:
    msg = payload.get("message") or payload.get("text") or payload.get("content") or "Witaj! W czym mogę Ci dzisiaj pomóc?"
    print(f"\n🤖 [GRAPH MIND OS]: {msg}\n")
    return {"status": "success", "message": msg}

# --- Sensory Atomy dla Bezpiecznego RAG (Chroot & File IO) ---

@PrimitiveRegistry.register("read_directory", "Listuje pliki i foldery w podanej ścieżce. Wymaga: path (np. '.')")
def read_directory(payload: dict) -> dict:
    folder = payload.get("path", ".")
    abs_path = os.path.abspath(folder)
    
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"[ERROR] Katalog nie istnieje: {abs_path}")
        
    try:
        files = os.listdir(abs_path)
    except Exception as e:
        raise PermissionError(f"[OS ERROR] System zabronił czytać tego miejsca: {e}")
        
    print(f"[PRIMITIVE FS]: Przeczytano strukturę: {abs_path} ({len(files)} items)")
    return {"files": files, "path_scanned": abs_path}

@PrimitiveRegistry.register("read_file", "Odczytuje zawartosc pliku tekstowego. Wymaga: filepath (lub filename).")
def read_file(payload: dict) -> dict:
    filename = payload.get("filepath") or payload.get("filename") or payload.get("path", "")
    abs_path = os.path.abspath(filename)
    
    if not os.path.isfile(abs_path):
        raise FileNotFoundError(f"[ERROR] Plik nie istnieje: {abs_path}")
        
    with open(abs_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    print(f"[PRIMITIVE FS]: Przeczytano plik: {abs_path} ({len(content)} znakow)")
    return {"text_content": content, "filepath": abs_path, "filename": abs_path}

@PrimitiveRegistry.register("ask_user_permission", "Zatrzymuje proces i prosi człowieka o zgodę na działanie. Wymaga: action_description, consequences.")
def ask_user_permission(payload: dict) -> dict:
    """
    KRYTYCZNY WĘZEŁ - Human-in-the-loop.
    Zatrzymuje spacer grafu, pyta usera z terminala o zgodę na działanie zagrażające.
    """
    action = payload.get("action_description", "Nieznana ryzykowna akcja")
    consequences = payload.get("consequences", "Brak danych o konsekwencjach. Zachowaj ostrożność!")
    
    print(f"\n" + "="*50)
    print(f"[HUMAN-IN-THE-LOOP] Wymagana Zgoda")
    print(f"Agent próbuje zrealizować pod-graf operacji: '{action}'")
    print(f"PRZEWIDYWANE KONSEKWENCJE: {consequences}")
    
    while True:
        choice = input(f"Zezwolić na wykonanie? [Y]es / [N]o: ").strip().lower()
        if choice in ['y', 'yes']:
            print(f"✅ Zezwolono ręcznie na: '{action}'")
            print("="*50 + "\n")
            return {"permission_granted": True}
        elif choice in ['n', 'no']:
            print(f"[REJECTED] Odmowiono. Wyrzucam bląd zabezpieczenia Autonomii.")
            print("="*50 + "\n")
            raise PermissionError("Użytkownik odmówił wykonania Atoma modyfikującego system.")

# --- Sensory Atomy dla Sieci Internetowej (Web & REST API) ---

@PrimitiveRegistry.register("fetch_webpage", "Pobiera treść strony WWW i wyciąga z niej czysty tekst (GET). Wymaga: url.")
def fetch_webpage(payload: dict) -> dict:
    """Sensoryczne przeczytanie strony internetowej ze świata (bez wysyłania wrażliwych danych)."""
    url = payload.get("url")
    if not url:
        raise ValueError("[ERROR] Atom 'fetch_webpage' wymaga parametru 'url'.")
        
    print(f"[PRIMITIVE NET]: Pobieranie GET z URLa: {url} ...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'GraphMindOS-Spider/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
        # Zabezpieczenie przed ściągnięciem śmieci HTML do RAM:
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator=' ', strip=True)
        print(f"[PRIMITIVE NET]: Wyciągnięto {len(text)} znaków czystego tekstu.")
        
        # Zwracamy text_content by ChromaDB Graph RAG naturalnie zaindeksowała wiedzę
        return {"text_content": text, "url": url}
    except Exception as e:
        raise RuntimeError(f"[PRIMITIVE NET] Sieć odrzuciła uścisk dłoni z {url}: {e}")

@PrimitiveRegistry.register("http_post", "Wysyła dane (JSON) metodą POST pod wskazany adres URL. Wymaga: url, data, permission_granted=True.")
def http_post(payload: dict) -> dict:
    """Niszczycielski lub wrażliwy przekaźnik danych do neta."""
    # BEZWZGLĘDNE ZABEZPIECZENIE (HARD-CODED HARNESS)
    if not payload.get("permission_granted"):
        raise PermissionError(
            "🛑 ZABEZPIECZENIE ANTY-HAKERSKIE 🛑 "
            "Model AI spróbował wysłać POST w otwartą sieć bez węzła Human-in-the-loop "
            "lub nie przekazał logiki permission_granted! Proces ZABITY."
        )

    url = payload.get("url")
    data = payload.get("data", {})
    if not url:
        raise ValueError("[ERROR] Atom 'http_post' wymaga parametru 'url'.")

    print(f"[PRIMITIVE NET]: Bezpieczny Autoryzowany POST do: {url}")
    try:
        encoded_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=encoded_data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as response:
            result = response.read().decode('utf-8', errors='ignore')
            
        print(f"[PRIMITIVE NET]: Wysłano pomyślnie. Odpowiedź z serwera odebrana.")
        return {"response": result}
    except Exception as e:
        raise RuntimeError(f"[PRIMITIVE NET] Wysłanie POST nie powiodło się: {e}")
