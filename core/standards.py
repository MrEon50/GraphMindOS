import os

# Domyślny folder danych i plików wyjściowych dla GraphMindOS
DEFAULT_DATA_DIR = os.path.abspath(os.path.join(os.getcwd(), "workspace", "data"))
os.makedirs(DEFAULT_DATA_DIR, exist_ok=True)

def resolve_filepath(path_str: str) -> str:
    """
    Rozwiązuje ścieżkę do pliku. Jeśli użytkownik podał samą nazwę (np. 'haslo.txt'),
    kieruje plik do domyślnego folderu workspace/data/haslo.txt.
    """
    if not path_str:
        return os.path.join(DEFAULT_DATA_DIR, "output.txt")
    if os.path.isabs(path_str) or ":" in path_str or path_str.startswith("/") or path_str.startswith("\\"):
        return os.path.abspath(path_str)
    return os.path.join(DEFAULT_DATA_DIR, path_str)

# === OPERACJE NA PLIKACH ===
# filepath  - sciezka do pojedynczego pliku (odczyt/zapis/modyfikacja)
# filename  - alias dla filepath (akceptowany, ale ZWRACAJ filepath)
# path      - sciezka do folderu/katalogu
# source    - sciezka zrodlowa (kopiowanie/przenoszenie)
# target    - sciezka docelowa (kopiowanie/przenoszenie)
# mode      - tryb operacji na pliku: "w" (write), "a" (append), "r" (read)

# === DANE TEKSTOWE ===
# text          - tekst wejsciowy do przetwarzania
# text_content  - alias dla text (akceptowany)
# content       - tresc do zapisania/wyslania
# cleaned_text  - wynik po czyszczeniu tekstu

# === LISTY I KOLEKCJE ===
# items     - lista elementow (plikow, wynikow, linkow)
# files     - lista plikow w folderze
# count     - ilosc elementow
# index     - numer/pozycja elementu

# === SIEC I HTTP ===
# url           - adres URL strony/API
# headers       - naglowki HTTP (dict)
# response      - tresc odpowiedzi HTTP
# status_code   - kod statusu HTTP (200, 404, 500)
# data          - dane do wyslania (POST)

# === SYSTEM I KONSOLA ===
# command        - komenda systemowa do wykonania (CMD/PowerShell)
# console_output - wynik wykonania komendy
# exit_code      - kod wyjscia programu

# === BEZPIECZENSTWO (Human-in-the-Loop) ===
# action_description  - opis planowanej akcji
# consequences        - przewidywane konsekwencje
# permission_granted  - True/False po decyzji uzytkownika

# === METADANE I STATUS ===
# status    - status operacji: "success", "error", "pending"
# message   - komunikat/wiadomosc do zalogowania
# error     - opis bledu (jesli wystapil)
# timestamp - znacznik czasu operacji

# === ARCHIWIZACJA ===
# source_folder  - folder zrodlowy do spakowania
# output_path    - sciezka docelowa archiwum

# === RAG I WIEDZA ===
# query       - zapytanie do bazy wiedzy
# documents   - lista dokumentow z bazy
# embeddings  - wektory embeddingu
# collection  - nazwa kolekcji w bazie

# ============================================================
# Slownik aliasow - uzywany przez Router (Smart Key Mapper)
# Format: klucz_docelowy -> [lista aliasow do przeszukania]
# ============================================================
KEY_ALIASES = {
    # Pliki
    "text": ["text_content", "cleaned_text", "merged_context", "console_output", "response"],
    "content": ["text_content", "cleaned_text", "text", "merged_context", "console_output", "response"],
    "filepath": ["filename", "path", "output_path", "file_path"],
    "filename": ["filepath", "path", "file_path"],
    "path": ["filepath", "filename", "source_folder", "target_folder"],
    "source": ["filepath", "filename", "path"],
    "target": ["output_path", "filepath"],
    # System
    "message": ["text_content", "cleaned_text", "console_output", "text", "response"],
    "command": ["text_content", "text"],
    # Siec
    "url": ["endpoint", "address", "link"],
    "data": ["content", "text", "payload_data"],
    # Listy
    "items": ["files", "documents", "results", "links"],
}

# ============================================================
# Tekst standardow do wstrzykniecia w prompty LLM
# ============================================================
def get_standards_for_prompt() -> str:
    """Zwraca skrocony opis standardow do wstawienia w system prompt LLM."""
    return """STANDARD KLUCZY GraphMindOS (ZAWSZE uzywaj tych nazw):

PLIKI:
- filepath: sciezka do pliku (NIE: file_path, file, sciezka) - podanie samej nazwy np. 'haslo.txt' trafia do domyslnego folderu workspace/data/haslo.txt
- path: sciezka do folderu (NIE: directory, folder, katalog)
- source: sciezka zrodlowa | target: sciezka docelowa
- mode: tryb zapisu ("w"=nadpisz, "a"=dopisz)

DANE:
- text: tekst wejsciowy do przetwarzania
- content: tresc do zapisania/wyslania
- items: lista elementow (plikow, wynikow)
- count: ilosc elementow

SIEC:
- url: adres strony/API
- data: dane do wyslania (POST)
- response: odpowiedz HTTP

SYSTEM:
- command: komenda CMD/PowerShell
- console_output: wynik komendy

BEZPIECZENSTWO:
- action_description: opis akcji
- consequences: konsekwencje
- permission_granted: True/False

STATUS:
- status: "success" lub "error"
- message: komunikat do zalogowania"""
