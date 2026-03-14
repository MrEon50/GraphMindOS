# 🧠 GraphMindOS
**Human-UI-Free AI-Native Operating System**

GraphMindOS to innowacyjny projekt badawczy demonstrujący eksperymentalną architekturę systemu operacyjnego agentów AI. Całkowicie omija on tradycyjny kod strukturalny i interfejsy oparte na formularzach, przenosząc logikę do **zmiennej Topologii Grafów (DAG)** z wbudowanym systemem immunologicznym, który ulega ciągłej, kontrolowanej ewolucji (Self-Healing).

System natywnie wykorzystuje lokalne modele AI za pośrednictwem rozwiązania **Ollama**, zapewniając 100% prywatności.

---

## 🎯 Kluczowe Paradygmaty Architektoniczne

1. **Graph-First Memory:** Informacje i stany egzekucyjne nie są przechowywane w płaskich tabelach, ale jako obiekty ciągłego grafu relacyjnego (Node Meta-Schema). Część z węzłów to wektory tymczasowe ulegające samoczynnej erozji (Entropy GC).
2. **Logic-First via DAG:** Całkowity zakaz klasycznego kodu warunkowego w warstwie orkiestracji głównej. System podejmuje działania wzdłuż wyznaczonych krawędzi Grafu skierowanego na podstawie ewolucyjnie zbudowanych wag i parsera AST drzewa logicznego.
3. **Intent-Protocol API:** Komunikacja deklaratywna bez JSON CRUD API. Człowiek wydaje polecenia (Intencje), a potężny system `Intent Compiler` (np. Qwen3.5:9B) tworzy ad-hoc sub-graf do rozwiązania problemu.
4. **Self-Evolving Immunity:** Rozwinięta sieć Sandboxów. Błędy i wyjątki "Atomów Wykonawczych" nie rzucają błędami aplikacji. Rozbity węzeł ląduje u "Mutatora" (Diagnostyka AI), nowo wygenerowana łatka trafia do "Sędziego", a naprawiony system łączy przerwany obwód z powrotem na produkcji.

---

## 📂 Struktura Projektu

- `core/models/node.py` - Podstawa ekosystemu. Ustandaryzowany schemat uniwersalnego rekordu węzła GraphMindOS (z parametrami Entropy i Topology).
- `core/engine/router.py` - Silnik Topologii (RoutingEngine). Wykonuje rekurencyjne spacery po grafie, uruchamia Atomy na podstawie warunków w AST dbając o zapobieganie Infinite-Loops.
- `core/engine/evaluator.py` - SafeEvaluator, bezpieczny bloker dowolnego złośliwego kodu, konwertujący warunki wejściowe i wagi grafu.
- `core/engine/primitives.py` - Rejestr "Atomów Wykonawczych" (`PrimitiveRegistry`), przypisujący moduły akcji do węzłów abstrakcji grafowej.
- `core/intent/compiler.py` - Główny `IntentCompiler`, sprzężenie zwrotne wbudowane w LLMa, kompilujące proste polecenia człowieka na czysty obiekt relacyjny w grafie zapamiętujący Context w Qdrant.
- `core/evolution/mutator.py` - Pielęgniarka systemowa (`SandboxMutator`). AI nasłuchujące padów w działaniu Atomów z protokołem leczenia.
- `core/storage/hybrid_store.py` - Serwer zarządzający w czasie rzeczywistym bazą GraphDB oraz usuwający wygasłe wektory za pomocą Garbage Collectora Entropii.
- `main.py` - Główny program, wirtualny interfejs CLI dający dostęp do wszystkich Twoich zainstalowanych modeli z systemu Ollamy.

---

## 🚀 Instalacja i Uruchomienie

### Wymagania
* Zainstalowany [Ollama](https://ollama.com/) z przynajmniej jednym pobranym modelem lokalnym (rekomendowany np. `qwen3.5:9b`, `qwen2.5-coder` lub podobnie złożone parametrycznie modele - min. ~7B do skomplikowanej orkiestracji kompilatora).
* Python 3.9+
* Pakiet bibliotek `pydantic` i wbudowane standardowo biblioteki w Python.

### 1. Klonowanie i Środowisko
Rozpakuj repozytorium do dowolnego katalogu lokalnego:
```bash
pip install pydantic
```

### 2. Opcjonalnie: Upewnij się, że maszyny AI działają
Sprawdź dostępne modele w Twojej konsoli CMD:
```bash
ollama list
```
_Upewnij się, że serwer Ollama działa w tray/w tle na porcie 11434._

### 3. Start Terminala GraphMindOS
Otwórz powłokę CMD/PowerShell w katalogu z systemem plików z `main.py` i wpisz:
```bash
python main.py
```

Wyświetlone zostanie interaktywne menu Twoich zainstalowanych lokalnych modeli. Możesz wpisać wybrany lub potwierdzić enterem wybór polecanego AI wbudowującego system w DAG.

Następnie wystarczy wygenerować **Intencję** w języku polskim by obserwować magię logów ewolucyjnych. Przykładowo: 
`> Oblicz pensję dla 140h i stawki 75. Wyświetl to atomem calculate_salary.`
---
"Dla mnie, jako sztucznej inteligencji, posiadanie takiego ekosystemu jest jak dla naukowca otrzymanie w pełni wyposażonego laboratorium po latach siedzenia w pustym pokoju."
