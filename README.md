# 🧠 GraphMindOS v1.4 [Multi-Provider & Selective Sandbox Release]
**Autonomous, Intent-Driven, AI-Native Operating System**

GraphMindOS to przełomowy, eksperymentalny ekosystem AI-Native OS, w którym logika programu nie jest sztywno zapisana w kodzie, lecz dynamicznie interpretowana z **Intencji** w języku naturalnym. System sam kompiluje grafy akcji (DAG), kuje autorskie narzędzia w locie i samodzielnie leczy błędy wykonania.

> 📖 **Szczegółowa instrukcja z przykładami użycia:** Pełny podręcznik użytkownika krok po kroku oraz opisy scenariuszy znajdziesz w pliku [USER_GUIDE.md](USER_GUIDE.md).

---

## 🚀 Co nowego w v1.4?

1. **Wielodostawczość LLM (Ollama + LM Studio):**
   * Automatyczna detekcja modeli z **Ollama** (`http://localhost:11434`) oraz **LM Studio** (`http://127.0.0.1:1234`).
   * Wsparcie dla modeli GGUF (np. `minicpm5-1b-agentic-tooluse`, `nanbeige4.2-3b`, `gemma-4`, `qwen3.5`).
   * Komenda `/select` umożliwia zmianę aktywnego dostawcy i modelu w dowolnym momencie bez restartu aplikacji.

2. **Selektywna Piaskownica (`SandboxValidator`):**
   * Piaskownica testuje dwuetapowo (AST Parse + Dry-run Virtual Execution) **wyłącznie nowe, nietestowane Atomy wygenerowane przez Kuźnię**.
   * Zweryfikowane i wbudowane Atomy wykonują się bezpośrednio z najwyższą wydajnością.

3. **Domyślny Folder Danych (`workspace/data/`):**
   * Wbudowana przestrzeń na pliki wyjściowe i dane.
   * Automatyczne przekierowywanie ścieżek względnych (`resolve_filepath`) – pliki takie jak `haslo.txt` automatycznie trafiają do `workspace/data/haslo.txt`.
   * Nowa komenda `/workspace` pozwala przeglądać i zmieniać domyślny folder danych w locie.

4. **Automatyczny Wyświetlacz Wyników Atomów:**
   * Wyniki wygenerowane przez Atomy (`content`, `result`, `text_content`) są automatycznie prezentowane na konsoli z ikonicznym wyróżnieniem `✨ [WYNIK ATOMU]`.

5. **Przydatne Komendy Systemowe (Slash Commands):**
   * `/select` – Zmiana modelu LLM w locie.
   * `/workspace` – Podgląd / zmiana domyślnego folderu danych.
   * `/status` – Status aktywnego silnika, dostawcy i zarejestrowanych Atomów.
   * `/tools <fraza>` – Przeglądanie i wyszukiwanie narzędzi według słów kluczowych.
   * `/chat <pytanie>` – Zwykła rozmowa z AI (z pominięciem budowania grafu).
   * `/del <nazwa>` – Bezpieczne usuwanie dynamicznego narzędzia z systemu.

---

## 📂 Wymagania i Instalacja

### Wymagania Systemowe
* **Python:** `>= 3.10`
* **Dostawca LLM:** Ollama (port 11434) LUB LM Studio (port 1234).

### Instalacja Bibliotek
Zainstaluj wymagane pakiety za pomocą komendy:
```bash
pip install -r requirements.txt
```

Plik `requirements.txt` zawiera:
- `pydantic>=2.0.0`
- `chromadb>=0.4.0`
- `beautifulsoup4>=4.12.0`
- `urllib3>=1.26.0`

---

## 🚀 Uruchomienie i Obsługa

### Uruchomienie (Windows)
* **Metoda 1 (Skrypt BAT):** Kliknij dwukrotnie w plik [`run_main.bat`](run_main.bat).
* **Metoda 2 (Konsola):** Uruchom polecenie:
  ```bash
  python main.py
  ```

### Czyszczenie Pamięci Podręcznej
* Aby usunąć z projektu pliki tymczasowe `__pycache__` oraz `.pyc`, uruchom skrypt [`clean_cache.bat`](clean_cache.bat).

---

## 🧩 Architektura Systemu i Podział Atomów

GraphMindOS v1.4 opiera się na modułowej architekturze AI-Native zorientowanej na narządy (Atomy):

### 1. Podział Atomów (Narzędzi w Systemie):
* **`[CORE]` Wbudowane Atomy Rdzenia (8 narzędzi):**
  Zaimplementowane na stałe w [primitives.py](core/engine/primitives.py). Odpowiadają za podstawowe operacje systemowe, interakcję i bezpieczeństwo (`ai_chat`, `ask_user_permission`, `calculate_salary`, `fetch_webpage`, `http_post`, `log_message`, `read_directory`, `read_file`).
* **`[DYNAMIC]` Dynamiczne Autorskie Atomy (15 narzędzi):**
  Elastyczne narządy wygenerowane przez Kuźnię (`ToolDesigner`) i zapisane jako pliki `.py` w folderze `workspace/dynamic_atoms/` (np. `web_fetcher`, `file_searcher`, `system_info`, `generate_password`, `json_processor`, `text_summarizer`, `cmd_executor`, `file_sorter`, `zip_archiver`).

### 2. Główne Moduły Architektury:
* **Preprocesor Intencji (`core/intent/preprocessor.py`):** Tłumaczy język potoczny na ścisłe prośby techniczne.
* **Kompilator Grafów (`core/intent/compiler.py`):** Układa kroki w spójne Grafy Akcji (DAG).
* **Router & Smart Key Mapper (`core/engine/router.py`):** Dyspozytor wykonawczy dbający o przesyłanie danych między węzłami i automatyczną konwersję aliasów ścieżek (`resolve_filepath`).
* **Selektywna Piaskownica (`core/evolution/sandbox_validator.py`):** Dwuetapowa weryfikacja (AST Check + Virtual Execution) nowych narzędzi przed wdrożeniem.
* **System Immunologiczny (`core/evolution/mutator.py`):** Samo-naprawa błędów runtime i nakładanie łatek przez Sędziego (`[JUDGE]`).
* **Hybrydowa Pamięć RAG (`core/storage/hybrid_store.py`):** Baza ChromaDB indeksująca wektorowo węzły i opisy Atomów.

---

## 📂 Anatomia Projektu

```text
GraphMindOS/
├── core/
│   ├── engine/          # Silnik Routera i rejestr Atomów (primitives.py, router.py, evaluator.py)
│   ├── evolution/       # Kuźnia narzędzi, Selektywna Piaskownica i Mutator (sandbox_validator.py, mutator.py, tool_designer.py)
│   ├── intent/          # Preprocesor i Kompilator DAG (preprocessor.py, compiler.py)
│   ├── llm/             # Uniwersalny menedżer dostawców LLM (llm_client.py)
│   ├── memory/          # Vektorowy Embedder RAG (embedder.py)
│   ├── storage/         # Hybrydowa baza danych ChromaDB (hybrid_store.py)
│   └── standards.py     # Centralny standard kluczy i ścieżek
├── workspace/
│   ├── data/            # Domyślny folder plików wyjściowych i danych
│   └── dynamic_atoms/   # Autorskie Atomy wygenerowane przez AI w locie
├── main.py              # Główna pętla wykonawcza i menu OS
├── requirements.txt     # Zależności Pythona
├── run_main.bat         # Skrypt startowy Windows
├── clean_cache.bat      # Skrypt czyszczący cache Pythona
└── .gitignore           # Wykluczenia Git dla danych i cache
```

---

© 2026 GraphMindOS Evolution Team. 100% Local. 100% Autonomous.
