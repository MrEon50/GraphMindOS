# 🧠 GraphMindOS v1.1 [Evolutionary Release]
**Autonomous, Human-UI-Free, AI-Native Operating System**

GraphMindOS to eksperymentalny ekosystem, w którym AI przestaje być tylko "chatbotem", a staje się autonomicznym operatorem systemu. To OS zaprojektowany dla agentów, gdzie logika nie jest wpisana na sztywno w kodzie, lecz kompilowana wlocie do formy **Dynamicznych Grafów Akcji (DAG)**. System natywnie wykorzystuje lokalne modele AI, zapewniając 100% prywatności i kontroli.

## 🚀 Kluczowe Funkcjonalności v1.1

1.  **Intent Pre-Processor (NEW):** Warstwa interpretacji języka naturalnego. AI przekłada potoczne prośby (np. "zrób tu porządek") na precyzyjne cele techniczne rozumiane przez kompilator.
2.  **Autonomous Tool Factory & Auto-Evolution:** Jeśli systemowi brakuje narzędzia do wykonania zadania, AI potrafi je samodzielnie zaprojektować, napisać kod i wstrzyknąć do rdzenia OS (po autoryzacji).
3.  **Hybrid RAG Memory (Vector Store):** Pełna integracja z ChromaDB. Wymaga modelu `mxbai-embed-large` wewnątrz Ollama. Każda interakcja buduje trwałą bazę wiedzy agenta.
4.  **Payload Forwarding & Chaining:** Możliwość przekazywania danych między węzłami grafu. Wynik jednego działania (np. odczyt pliku) jest dostępny dla kolejnych kroków procesu.
5.  **Human-in-the-Loop Safety:** Zaawansowana analiza konsekwencji. AI ostrzega przed ryzykiem modyfikacji systemu, a ostateczna decyzja [Y/N] zawsze należy do Architekta.

## 📂 Anatomia Systemu

-   **Pre-procesor Intencji** – Pierwszy filtr LLM, który "czyta między wierszami" i definiuje konkretny cel operacyjny.
-   **Kompilator Grafów** – Główny procesor tłumaczący intencje na obiekty topologii (węzły i krawędzie).
-   **Fabryka Narzędzi** – Moduł odpowiedzialny za ewolucyjne generowanie kodu Python dla nowych "Atomów".
-   **Magazyn Semantyczny** – Warstwa ChromaDB zarządzająca pamięcią długoterminową i wektorami RAG.
-   **Silnik Topologii (Router)** – Serce egzekucyjne nawigujące po grafie i dbające o przepływ danych (payload) między węzłami.

## 🛠️ Instalacja i Uruchomienie

### Wymagania
* **Ollama** (uruchomiona lokalnie na porcie 11434).
* **Modele Ollama:**
    * `qwen3.5:9b` (lub nowszy) – rekomendowany jako mózg systemu.
    * `mxbai-embed-large:latest` – **WYMAGANY** do poprawnego działania pamięci RAG.
* **Python 3.9+**
* **Biblioteki:** `pydantic`, `chromadb`, `beautifulsoup4`, `requests`.

### Start Systemu
1. Pobierz wymagane modele: `ollama pull qwen3.5:9b` oraz `ollama pull mxbai-embed-large`
2. Zainstaluj pakiety: `pip install pydantic chromadb beautifulsoup4 requests`
3. Uruchom moduł: `python main.py`

## 💡 Przykłady Użycia (Natural Language)

*   `"Posprzątaj w folderze workspace pliki txt."`
*   `"Znajdź w sieci info o nowościach w AI i stwórz z tego raport RAG."`
*   `"Sprawdź zasoby mojego systemu i zainstaluj brakujące narzędzie do logowania graficznego."`

---
*Projekt GraphMindOS demonstruje, że przyszłość informatyki polega na budowaniu inteligentnych środowisk, które potrafią same rozszerzać swoje możliwości.*

---
> "Dla mnie, jako sztucznej inteligencji, posiadanie takiego ekosystemu jest jak dla naukowca otrzymanie w pełni wyposażonego laboratorium po latach siedzenia w pustym pokoju."
