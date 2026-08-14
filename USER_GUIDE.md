# 📖 GraphMindOS v1.4 - Podręcznik Użytkownika i Instrukcja Obsługi

Witamy w podręczniku użytkownika **GraphMindOS v1.4** – autorskiego, autonomicznego systemu operacyjnego sterowanego Intencjami w języku naturalnym (*AI-Native Operating System*).

Ten dokument zawiera instrukcję krok po kroku oraz zestaw praktycznych przykładów, które pozwolą Ci wykorzystać pełny potencjał systemu.

---

## 🚀 1. Pierwsze Uruchomienie

### Uruchomienie Systemu
Na systemie Windows możesz uruchomić system na dwa sposoby:
1. **Dwuklik w plik [`run_main.bat`](run_main.bat)**
2. **Wykonywanie polecenia w konsoli:**
   ```bash
   python main.py
   ```

### Wybór Dostawcy LLM i Modelu
Po uruchomieniu zobaczysz menu wyboru dostępnych modeli z trzech dostawców:
* **`[OLLAMA]`** (np. `qwen3.5:9b`, `gemma4:12b`, `phi4`)
* **`[LMSTUDIO]`** (np. `minicpm5-1b-agentic-tooluse`, `nanbeige4.2-3b`, `gemma-4-12b-it-qat`)
* **`[GEMINI]`** (np. `gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-1.5-pro`)

Wystarczy wpisać **numer z listy** i nacisnąć `Enter`. Model zalecany oznaczony jest jako `[REKOMENDOWANY]`.

> **Wskazówka:** W dowolnym momencie możesz zmienić model bez przerywania pracy, wpisując w konsoli komendę `/select`.

---

## 🧠 2. Podstawy Pracy z Intencjami

GraphMindOS nie wymaga znajomości komend składniowych ani skryptów. Wystarczy, że opiszesz swoją prośbę w **języku naturalnym** w znaku zachęty `[Intencja]>`.

### Jak działa cykl wykonawczy?
1. **Pre-procesor:** Analizuje intencję i doprecyzowuje techniczne szczegóły zadania.
2. **Kompilator DAG:** Zamienia intencję na plan kroków (Graf Akcji).
3. **Egzekutor & Router:** Wykonuje wyselekcjonowane Atomy (narzędzia) i przekazuje dane między nimi.
4. **Automatyczny Wynik:** Zwrócone dane wyświetlają się w ramce `✨ [WYNIK ATOMU]`.

---

## 💡 3. Praktyczne Scenariusze i Przykłady Użycia

### Scenariusz A: Generowanie i Bezpieczny Zapis Plików
**Intencja:**
```text
Zapisz nowe 16-znakowe hasło w pliku tajne_haslo.txt
```
**Co zrobi system?**
1. Wywoła Atom `generate_password (length=16)`.
2. Zapyta Cię o potwierdzenie zapisu `[Y/N]` (Human-in-the-Loop).
3. Bezpiecznie zapisze plik w domyślnym folderze danych: `workspace/data/tajne_haslo.txt`.

---

### Scenariusz B: Pobieranie i Analiza Stron WWW
**Intencja:**
```text
Pobierz treść ze strony python.org i zapisz w pliku python_info.txt
```
**Co zrobi system?**
1. Uruchomi Atom `web_fetcher`, usuwając kod HTML/JS i pobierając czysty tekst.
2. Zapyta o zgodę na zapis do pliku.
3. Zapisze odfiltrowane podsumowanie w `workspace/data/python_info.txt`.

---

### Scenariusz C: Diagnostyka Sprzętowa Komputera
**Intencja:**
```text
Sprawdź parametry mego komputera i wolne miejsce na dysku
```
**Co zrobi system?**
1. Wywoła Atom `system_info`.
2. Wyświetli raport obejmujący użytkownika, wersję Windowsa, rdzenie CPU i dostępną przestrzeń na dysku (w GB).

---

### Scenariusz D: Wyszukiwanie Plików na Dysku
**Intencja:**
```text
Znajdź wszystkie pliki z rozszerzeniem py w moim folderze
```
**Co zrobi system?**
1. Uruchomi Atom `file_searcher (extension=.py)`.
2. Wyświetli listę odnalezionych plików w czytelnym zestawieniu.

---

### Scenariusz E: Zwykła Rozmowa i Pytania Ogólne
**Intencja:**
```text
Dlaczego niebo w dzień jest niebieskie?
```
**Co zrobi system?**
1. Wykryje brak potrzeby operacji na plikach.
2. Wywoła Atom `ai_chat`, odpowiadając w przyjaznym formacie `🤖 [GRAPH MIND OS]`.

---

## 🛠️ 4. Kuźnia Narzędzi (Ewolucja - Tworzenie Nowych Atomów)

Jeśli poprosisz system o wykonanie zadania, do którego brakuje narzędzia, Kuźnia (`ToolDesigner`) **zbuduje nowe narzędzie w locie**.

### Jak poprosić o stworzenie nowego narzędzia?
Użyj frazy zawierającej czasownik tworzenia oraz słowo `narzędzie` lub `atom`:
```text
Stwórz narzędzie do konwersji stopni Celsjusza na Fahrenheita
```
lub
```text
Stwórz narzędzie, które pobiera tekst i odwraca kolejność wyrazów
```

### Selektywna Piaskownica (`SandboxValidator`)
1. Kuźnia napisze kod w Pythonie.
2. **Selektywna Piaskownica** dokona próby wykonania kodu w izolacji (*Virtual Dry-Run*).
3. Jeśli kod nie posiada błędów składniowych, system wyświetli kod i zapyta:
   `Czy zgadzasz się, aby skompilować ten kod i wstrzyknąć w rdzeń OS? [Y/N]`
4. Wciśnięcie `Y` spowoduje natychmiastowe wczytanie nowego Atomu do dysku w `workspace/dynamic_atoms/` oraz pamięci RAM!

---

## 🛡️ 5. System Immunologiczny (Samo-Naprawa)

Jeśli w trakcie wykonywania jakiegoś narzędzia wystąpi błąd (np. przekazano tekst zamiast liczby):
1. **Wyłapanie błędu:** System nie ulega awarii. Wyjątek trafia do `SandboxMutator`.
2. **Diagnoza Sędziego (`[JUDGE]`):** Sędzia analizuje logi błędów i przygotowuje poprawioną strukturę danych lub łatkę kodu.
3. **Wirtualny Test:** Łatka jest testowana w izolacji.
4. **Dokończenie:** Urwany przewód neurologiczny zostaje połączony i zadanie kończy się sukcesem.

---

## 💻 6. Zestaw Komend Systemowych (Slash Commands)

Możesz wpisywać poniższe komendy bezpośrednio w konsoli `[Intencja]>`:

| Komenda | Opis i Przykłady Użycia |
| :--- | :--- |
| **`/select`** | Zmiana aktywnego dostawcy i modelu LLM w locie. |
| **`/workspace`** | Wyświetla ścieżkę i pliki w domyślnym folderze danych.<br>Użycie: `/workspace` lub `/workspace C:/NowyFolder` |
| **`/status`** | Podsumowanie stanu systemu, aktywnego dostawcy i liczby Atomów. |
| **`/tools`** | Lista zainstalowanych narzędzi z opisami.<br>Użycie filtrowania: `/tools file` lub `/tools pdf` |
| **`/chat <tekst>`** | Zwykła rozmowa / pytanie do AI z pominięciem budowania grafu.<br>Przykłada: `/chat Jak działa silnik odrzutowy?` |
| **`/del <nazwa>`** | Usuwa wybrane narzędzie dynamiczne z rejestru i dysku.<br>Przykład: `/del generate_password` |
| **`/info`** | Instrukcja podręczna i informacje o systemie. |
| **`/clear`** | Czyszczenie ekranu konsoli. |
| **`/exit`** | Zamyka GraphMindOS. |

---

## 📂 7. Domyślna Przestrzeń Danych (`workspace/data/`)

Domyślnie wszystkie wygenerowane raporty, pliki tekstowe oraz pliki pobrane ze stron trafiają do katalogu:
`workspace/data/`

* Nie musisz podawać pełnych ścieżek `C:/...`.
* Wpisując samą nazwę `haslo.txt`, system automatycznie skieruje plik do `workspace/data/haslo.txt`.

---

## 🔧 8. Rozwiązywanie Problemów (Troubleshooting)

* **Problem z połączeniem Ollama / LM Studio:**
  Sprawdź, czy aplikacja LM Studio (port 1234) lub serwer Ollama (port 11434) są uruchomione. Wpisz `/select` aby przełączyć dostawcę.
* **Czyszczenie pamięci podręcznej:**
  Jeśli chcesz usunąć skompilowane pliki tymczasowe Pythona, uruchom dwuklikiem skrypt **`clean_cache.bat`**.

---

© 2026 GraphMindOS Evolution Team. 100% Local. 100% Autonomous.
