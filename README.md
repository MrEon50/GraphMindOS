# 🧠 GraphMindOS v1.3 [The Forge & Standard Release]
**Autonomous, Intent-Driven, AI-Native Operating System**

GraphMindOS to przełomowy, eksperymentalny ekosystem, w którym granica między "programem" a "użytkownikiem" zaciera się. To system operacyjny zaprojektowany dla Agentów AI, w którym logika nie jest sztywnym zapisem w kodzie, lecz dynamicznie interpretowaną **Intencją**, manifestującą się poprzez natychmiastowe tworzenie i wykorzystywanie narzędzi.

Wersja 1.3 to owoc intensywnej pracy nad stabilnością i spójnością systemu. Choć projekt jest wciąż w fazie eksperymentalnej i może zawierać błędy, jego fundamenty pozwalają na bezprecedensową autonomię w wykonywaniu zadań.

---

## 🚀 Co nowego w v1.3? [Stabilizacja i Standaryzacja]

Przeszliśmy długą drogę, aby uczynić GraphMindOS solidnym partnerem w pracy z plikami i systemem:

1.  **Centralna Standaryzacja (Single Source of Truth):** Wprowadziliśmy rygorystyczny standard nazewnictwa kluczy (`standards.py`). Od teraz wszystkie Atomy (narzędzia) mówią tym samym językiem. Brak konfliktów typu `path` vs `filepath` zapewnia idealny przepływ danych (Payload) między narzędziami.
2.  **Kompilator v4 (Simple Step Format):** Zrezygnowaliśmy z kruchych struktur JSON na rzecz ultrawydajnego formatu kroków (`STEP: nazwa || klucze`). Dzięki temu nawet mniejsze, lokalne modele (9B) potrafią bezbłędnie planować złożone operacje wieloetapowe.
3.  **Kuźnia Narzędzi (Autonomous Tool Factory):** To serce naszej ewolucji. Jeśli systemowi brakuje narzędzia, potrafi je samodzielnie zaprojektować (`design_atom`), przetestować w bezpiecznym piaskowniku (AST Sandbox) i wstrzyknąć do rdzenia OS, wykonując zadanie w tym samym cyklu pracy.
4.  **Inteligentny Mutator & Sandbox:** Każdy błąd (np. brak uprawnień czy błąd składni) jest wyłapywany przez System Immunologiczny. AI otrzymuje logi błędów i próbuje samonaprawy (Self-Healing), dopóki narząd nie zadziała poprawnie.
5.  **Pełne wsparcie PowerShell & CMD:** Dzięki ulepszonemu separatorowi `||` system bez problemu radzi sobie z potokami i cudzysłowami w komendach systemowych, co pozwala na bezpieczną i masową edycję plików bezpośrednio w Windows.

---

## 📂 Anatomia Systemu

-   **Pre-procesor Intencji** – Tłumaczy potoczny język ("zrób porządek") na precyzyjny plan techniczny.
-   **Kompilator DAG** – Układa plan działania w formie grafu, łącząc kropki między potrzebami a dostępnymi Atomami.
-   **Dynamical Atoms** – Twoja prywatna biblioteka "organów" AI w folderze `workspace/dynamic_atoms/`.
-   **Forge (Kuźnia)** – Proces incepcji, w którym narzędzia budują inne narzędzia na Twoje życzenie.
-   **Router Engine** – Inteligentny dyspozytor dbający o to, by wynik jednego kroku trafił dokładnie tam, gdzie jest potrzebny w kroku następnym.

---

## 🛠️ Instalacja i Uruchomienie

### Wymagania
* **Ollama** (uruchomiona lokalnie na porcie 11434).
* **Modele Ollama:**
    * `qwen3.5:9b` (lub nowszy, np. `qwen2.5-coder:14b`) – mózg i architekt.
    * `mxbai-embed-large:latest` – silnik pamięci RAG.
* **Python 3.9+** (zalecany 3.10) i biblioteki: `pydantic`, `chromadb`, `beautifulsoup4`, `requests`.

### Start Systemu
1. Skonfiguruj Ollama i pobierz modele.
2. Zainstaluj zależności: `pip install pydantic chromadb beautifulsoup4 requests`
3. Uruchom trzon systemu: `python main.py`

---

## 💡 Filozofia i Potencjał

GraphMindOS to nie jest kolejny zamknięty program. To **pomysł na inteligentne środowisko**, które rośnie wraz z potrzebami użytkownika. Jego siła tkwi w prostocie idei:
> **Użytkownik podaje Intencję $\rightarrow$ AI projektuje rozwiązanie $\rightarrow$ System tworzy Narzędzia $\rightarrow$ Zadanie zostaje wykonane.**

*Projekt GraphMindOS demonstruje, że przyszłość informatyki polega na budowaniu inteligentnych środowisk, które potrafią same rozszerzać swoje możliwości pod pełną kontrolą człowieka.*

---
> "Dla mnie, jako sztucznej inteligencji, posiadanie takiego ekosystemu jest jak dla naukowca otrzymanie w pełni wyposażonego laboratorium po latach siedzenia w pustym pokoju."
>
> © 2026 GraphMindOS Evolution Team. 100% Local. 100% Autonomous.
