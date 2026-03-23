# 🧠 GraphMindOS v1.2 [The Command & Control Release]
**Autonomous, Human-UI-Free, AI-Native Operating System**

GraphMindOS to eksperymentalny ekosystem, w którym AI staje się autonomicznym operatorem systemu. To OS zaprojektowany dla agentów, gdzie logika nie jest wpisana na sztywno w kodzie, lecz kompilowana w locie do formy **Dynamicznych Grafów Akcji (DAG)**. System wykorzystuje lokalne modele AI (Ollama), zapewniając 100% prywatności.

## 🚀 Kluczowe Funkcjonalności v1.2

1.  **Slash Commands (NEW):** Nowy interfejs sterowania komendami:
    *   `/help` - Pełna lista możliwości.
    *   `/tools` - Podgląd wszystkich Atomów (CORE vs DYNAMIC).
    *   `/model` - Bezpośrednia rozmowa z mózgiem LLM (bypass grafów).
    *   `/del` - Bezpieczne usuwanie dynamicznych narzędzi z systemu.
2.  **Interactive Judge Security (ENHANCED):** Fabryka Narzędzi posiada inteligentnego Sędziego. Zamiast blokować, system ostrzega przed niebezpiecznym kodem (np. `subprocess`, `eval`), wyjaśnia zagrożenie i pyta Architekta o świadomą decyzję [Y/N].
3.  **Inteligentny Pre-procesor:** AI przekłada potoczne prośby (np. "zrób tu porządek") na precyzyjne cele techniczne, rozumiejąc intencje nawet w ogólnikowych zapytaniach.
4.  **Autonomous Tool Factory:** Jeśli systemowi brakuje narzędzia, AI potrafi je samodzielnie zaprojektować (Tool Designer), napisać kod Python i wstrzyknąć do rdzenia OS przez gorące przeładowanie (Hot-Reload).
5.  **Payload Forwarding:** Wynik jednego działania (np. odczyt pliku lub wynik z konsoli) jest automatycznie przekazywany jako wejście do kolejnych kroków procesu w grafie.

## 📂 Anatomia Systemu

-   **Pre-procesor Intencji** – Pierwszy filtr LLM, który "czyta między wierszami" i definiuje cel operacyjny.
-   **Kompilator Grafów** – Tłumaczy intencje na obiekty topologii (węzły i krawędzie).
-   **Judge (Sędzia)** – Strażnik bezpieczeństwa analizujący wygenerowany kod pod kątem luk i zagrożeń.
-   **Dynamical Atoms** – Folder `workspace/dynamic_atoms/` przechowuje autorskie narządy Twojego AI.
-   **Silnik Topologii (Router)** – Nawiguje po grafie i dba o przepływ danych (payload) między Atomami.

## 🛠️ Instalacja i Uruchomienie

### Wymagania
* **Ollama** (lokalnie na porcie 11434).
* **Modele Ollama:**
    * `qwen3.5:9b` (lub nowszy) – mózg systemu.
    * `mxbai-embed-large:latest` – wymagany do pamięci RAG.
* **Python 3.9+** i biblioteki: `pydantic`, `chromadb`, `beautifulsoup4`, `requests`.

### Start Systemu
1. Pobierz modele: `ollama pull qwen3.5:9b` oraz `ollama pull mxbai-embed-large`
2. Zainstaluj pakiety: `pip install pydantic chromadb beautifulsoup4 requests`
3. Uruchom: `python main.py`

## 💡 Przykłady Użycia

*   **Użycie Narzędzi:** `Użyj cmd_executor aby uruchomić ipconfig i zapisz wynik w pliku.`
*   **Ewolucja:** `Stwórz narzędzie 'file_sorter', które samo posprząta bałagan na pulpicie.`
*   **Bezpośrednie Pytanie:** `/model Wyjaśnij mi jak działa protokół TCP/IP w 3 zdaniach.`
*   **Zarządzanie:** `/tools` aby zobaczyć listę zmysłów lub `/del [nazwa]` aby usunąć niechciane narzędzie.

---
*Projekt GraphMindOS demonstruje, że przyszłość informatyki polega na budowaniu inteligentnych środowisk, które potrafią same rozszerzać swoje możliwości pod pełną kontrolą człowieka.*

---
> "Dla mnie, jako sztucznej inteligencji, posiadanie takiego ekosystemu jest jak dla naukowca otrzymanie w pełni wyposażonego laboratorium po latach siedzenia w pustym pokoju."
