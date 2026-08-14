import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"
from typing import Any
from core.intent.compiler import IntentCompiler
from core.intent.preprocessor import IntentPreProcessor
from core.storage.hybrid_store import HybridStore
from core.engine.router import RoutingEngine
from core.evolution.mutator import SandboxMutator
from core.evolution.tool_designer import ToolDesigner
from core.engine.primitives import PrimitiveRegistry
from core.llm.llm_client import LLMProviderManager

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def fetch_local_models() -> list:
    """Odpytuje Ollamę i LM Studio, zwracając listę dostępnych modeli."""
    all_models = LLMProviderManager.fetch_all_models()
    if not all_models:
        return [{"name": "qwen3.5:9b", "provider": "ollama"}]
    return all_models

def render_menu() -> Any:
    clear_screen()
    print("==================================================")
    print("  GraphMindOS v1.4 - Multi-Provider AI-Native OS  ")
    print("  Selektywna Piaskownica & Rój Modułowy Aktywny    ")
    print("==================================================\n")
    
    models = fetch_local_models()
    has_local = any(m.get("provider") in ["ollama", "lmstudio"] for m in models)
    
    if not has_local:
        print("⚠️  [INFORMACJA O WYMAGANIACH SYSTEMOWYCH]")
        print(" Nie wykryto aktywnego lokalnego serwera LLM (Ollama / LM Studio).")
        print("\n Aby korzystać z modeli lokalnych:")
        print(" 1. Uruchom LM Studio -> włącz serwer w zakładce Developer (http://127.0.0.1:1234)")
        print(" 2. LUB Uruchom Ollama -> wpisz 'ollama serve' w terminalu (http://localhost:11434)")
        print(" 3. LUB wybierz model [GEMINI] z listy poniżej i podaj klucz z https://aistudio.google.com\n")
        print("--------------------------------------------------\n")
        
    print("--- Dostępne Modele (Ollama / LM Studio / Gemini API): ---")
    suggested_idx = -1
    
    for idx, m_info in enumerate(models):
        m_name = m_info["name"]
        m_prov = m_info["provider"].upper()
        if "qwen" in m_name.lower() or "minicpm" in m_name.lower():
            suggested_idx = idx + 1
            print(f"  [{idx + 1}] [{m_prov}] {m_name} [REKOMENDOWANY]")
        else:
            print(f"  [{idx + 1}] [{m_prov}] {m_name}")
            
    print("\n--------------------------------------------------")
    suggested_str = f"(Enter = {models[suggested_idx-1]['name']})" if suggested_idx > 0 else "(Wpisz num)"
    wybor = input(f"Wybierz numer modelu {suggested_str}: ").strip()
    
    chosen_model = models[0] if models else {"name": "qwen3.5:9b", "provider": "ollama"}
    if not wybor and suggested_idx > 0:
        chosen_model = models[suggested_idx - 1]
    else:
        try:
            idx = int(wybor)
            if 1 <= idx <= len(models):
                chosen_model = models[idx - 1]
        except:
            pass

    if isinstance(chosen_model, dict) and chosen_model.get("provider") == "gemini":
        if not os.environ.get("GEMINI_API_KEY"):
            print("\n[GOOGLE GEMINI API KEY REQUIRED]")
            key = input("Wklej Twój GEMINI_API_KEY z Google AI Studio: ").strip()
            if key:
                os.environ["GEMINI_API_KEY"] = key

    return chosen_model


def main_loop():
    selected_model = render_menu()
    model_label = f"[{selected_model.get('provider', 'ollama').upper()}] {selected_model.get('name', selected_model)}" if isinstance(selected_model, dict) else str(selected_model)
    clear_screen()
    print(f"==================================================")
    print(f" Zalogowano: {model_label}")
    print(f" Wpisz 'exit' lub '/exit' by zamknąć system.")
    print(f" Wpisz '/select' aby zmienić model LLM.")
    print(f"==================================================\n")
    
    # Bootowanie Systemu GraphOS
    preprocessor = IntentPreProcessor(model_name=selected_model)
    compiler = IntentCompiler(model_name=selected_model)
    store = HybridStore()
    engine = RoutingEngine(store)
    mutator = SandboxMutator(model_name=selected_model)
    
    # Opcjonalne ładowanie na starcie
    PrimitiveRegistry.load_dynamic_atoms()
    
    while True:
        print("-" * 50)
        # 1. Zmysły (Przyjmowanie intencji / Intent-Protocol API)
        intent = input(f"[Intencja]> ")
        
        # --- OBSŁUGA KOMEND SYSTEMOWYCH (SLASH COMMANDS) ---
        if intent.strip().startswith("/"):
            cmd = intent.strip().split(" ", 1)[0].lower()
            args = intent.strip()[len(cmd):].strip()
            
            if cmd in ["/exit", "/quit"]:
                print("Zamykanie GraphMindOS...")
                break
                
            elif cmd == "/help":
                print("\n[DOSTEPNE KOMENDY SYSTEMOWE]")
                print("  /help            - Wyswietla te liste komend.")
                print("  /workspace       - Pokazuje/zmienia domyślny folder danych i plików wyjściowych.")
                print("  /select          - Wybierz inny model LLM (Ollama / LM Studio) bez restartu.")
                print("  /status          - Wyświetla status aktywnego silnika i dostawcy LLM.")
                print("  /tools <fraza>   - Pokazuje/filtruje liste dostepnych narzedzi (Atomow).")
                print("  /model <pytanie> - Zwykła rozmowa / pytanie do AI (bez budowania grafu).")
                print("  /del <nazwa>     - Usuwa dynamiczne narzedzie z systemu.")
                print("  /info            - Informacje o GraphMindOS i instrukcja obslugi.")
                print("  /clear           - Czysci ekran konsoli.")
                print("  /exit            - Zamyka system.")
                continue

            elif cmd in ["/workspace", "/dir", "/data"]:
                import core.standards as standards_mod
                if not args:
                    curr_dir = standards_mod.DEFAULT_DATA_DIR
                    print(f"\n[DOMYŚLNY FOLDER DANYCH GRAPH MIND OS]")
                    print(f" Ścieżka: {curr_dir}")
                    if os.path.exists(curr_dir):
                        files = os.listdir(curr_dir)
                        print(f" Zawartość ({len(files)} plików): {files if files else 'Brak plików'}")
                    else:
                        print(" Folder jeszcze nie istnieje.")
                    print(" Użyj: /workspace <nowa_ścieżka> aby zmienić domyślny folder danych.\n")
                else:
                    new_dir = os.path.abspath(args.strip())
                    os.makedirs(new_dir, exist_ok=True)
                    standards_mod.DEFAULT_DATA_DIR = new_dir
                    print(f"\n[WORKSPACE UPDATE] Zmieniono domyślny folder danych na: {new_dir}\n")
                continue

            elif cmd in ["/select", "/change", "/menu", "/models"]:
                selected_model = render_menu()
                model_label = f"[{selected_model.get('provider', 'ollama').upper()}] {selected_model.get('name', selected_model)}" if isinstance(selected_model, dict) else str(selected_model)
                preprocessor = IntentPreProcessor(model_name=selected_model)
                compiler = IntentCompiler(model_name=selected_model)
                mutator = SandboxMutator(model_name=selected_model)
                clear_screen()
                print(f"[SYSTEM UPDATE] Zmieniono aktywny model na: {model_label}\n")
                continue

            elif cmd == "/status":
                total_atoms = len(PrimitiveRegistry._registry)
                print(f"\n[STATUS SYSTEMU GraphMindOS v1.4]")
                print(f"  Aktywny dostawca i model: {model_label}")
                print(f"  Zarejestrowane Atomy:     {total_atoms}")
                print(f"  Baza Pamięci RAG:         ChromaDB (SQLite Persistent Backend)")
                print(f"  Selektywny Sandbox:       AKTYWNY (Testing only new atoms)")
                continue
                
            elif cmd == "/info":
                print("\n[O SYSTEMIE GraphMindOS v1.4]")
                print("GraphMindOS to AI-Native Operating System.")
                print("Zamiast wykonywać sztywny kod, system słucha Twoich Intencji w języku naturalnym,")
                print("tłumaczy je na plan działania i w locie kompiluje Dynamiczny Graf Akcji (DAG).")
                print("\n📖 Podręcznik Użytkownika & Instrukcja krok po kroku z przykładami:")
                print("   Otwórz plik USER_GUIDE.md w katalogu głównym projektu!")
                print("\nSzybki start:")
                print("1. Wpisz potoczną prośbę, np. 'Zapisz nowe 12-znakowe hasło w pliku tajne_haslo.txt'.")
                print("2. Pytania ogólne/rozmowa: po prostu wpisz je (np. 'cześć', 'dlaczego niebo jest niebieskie?').")
                print("3. Zmiana modelu LLM w dowolnym momencie: wpisz /select")
                print("4. Domyślny folder danych: /workspace\n")
                continue
                
            elif cmd in ["/tools", "/tool"]:
                filter_term = args.strip().lower() if args else ""
                header = f" (Filtrowanie: '{args}')" if filter_term else ""
                print(f"\n[ZAINSTALOWANE NARZEDZIA / ATOMY{header}]")
                if not PrimitiveRegistry._registry:
                    print("  Brak zaladowanych narzedzi.")
                else:
                    core_count = 0
                    dynamic_count = 0
                    matched_count = 0
                    for name, func in PrimitiveRegistry._registry.items():
                        desc = PrimitiveRegistry._descriptions.get(name, "Brak opisu.")
                        origin = PrimitiveRegistry._origins.get(name, "CORE")
                        tag = "[CORE]" if origin == "CORE" else "[DYNAMIC]"
                        
                        if filter_term and (filter_term not in name.lower() and filter_term not in desc.lower()):
                            continue
                            
                        matched_count += 1
                        print(f"  - {name} {tag}: {desc}")
                        if origin == "CORE":
                            core_count += 1
                        else:
                            dynamic_count += 1
                    print(f"\n  Podsumowanie: Widoczne {matched_count} z {len(PrimitiveRegistry._registry)} Atomów")
                print("\nWskazowka: Wpisz '/tools <fraza>' aby przefiltrować narzędzia, np. '/tools file'.")
                continue
                
            elif cmd == "/clear":
                clear_screen()
                continue
                
            elif cmd in ["/model", "/chat", "/ask"]:
                if not args:
                    print("[!] Podaj treść zapytania, np. /chat Jak działa fotosynteza?")
                else:
                    print(f"\n[MODEL {model_label} MYŚLI...]")
                    try:
                        resp = LLMProviderManager.chat_completion(
                            model_info=selected_model,
                            system_prompt="Jesteś pomocnym, inteligentnym asystentem AI w systemie GraphMindOS.",
                            user_prompt=args,
                            timeout=120
                        )
                        print(f"\n🤖 {resp}\n")
                    except Exception as e:
                        print(f"[!] Błąd komunikacji z modelem: {e}")
                continue
            elif cmd == "/del":
                if not args:
                    print("[!] Podaj nazwe narzedzia do usuniecia, np. /del text_cleaner")
                else:
                    tool_name = args.strip()
                    confirm = input(f"Czy na pewno chcesz usunac narzedzie '{tool_name}'? [Y/N]: ").strip().lower()
                    if confirm in ['y', 'yes']:
                        result = PrimitiveRegistry.unregister(tool_name)
                        if result["success"]:
                            deleted = result.get('deleted_file', 'nieznany')
                            print(f"[UNINSTALL] Atom '{tool_name}' zostal usuniety z rejestru.")
                            if deleted:
                                print(f"[UNINSTALL] Plik zrodlowy '{deleted}' zostal skasowany z dynamic_atoms/.")
                            else:
                                print(f"[UNINSTALL] Nie znaleziono pliku zrodlowego (atom byl tylko w pamieci).")
                        else:
                            print(f"[!] {result['reason']}")
                    else:
                        print("[!] Anulowano usuwanie.")
                continue

            else:
                print(f"[!] Nieznana komenda: {cmd}. Wpisz /help aby zobaczyc liste.")
                continue

        if not intent.strip():
            print("Wpisz /help aby zobaczyć dostępne komendy.")
            continue
            
        try:
            # 1b. The Tool Designer (Self-Evolving Code Pipeline)
            # Inteligentna detekcja na bazie slow kluczowych (zamiast sztywnych prefixow)
            intent_lower = intent.lower()
            creation_verbs = ["stwórz", "stworz", "zbuduj", "napisz", "zaprojektuj", "zrób", "zrob", "dodaj", "wygeneruj"]
            tool_nouns = ["atom", "narzędzie", "narzedzie", "tool", "zmysł", "zmysl", "narząd", "narzad"]
            has_verb = any(v in intent_lower for v in creation_verbs)
            has_noun = any(n in intent_lower for n in tool_nouns)
            is_tool_request = has_verb and has_noun
            
            if is_tool_request:
                designer = ToolDesigner(model_name=selected_model)
                new_code = designer.design_tool(intent)
                
                if new_code and designer.validate_code(new_code):
                    print(f"\n==================================================")
                    print(f"[KLAUZULA EWOLUCYJNA] Agent stworzyl nowy narzad:")
                    print(f"==================================================\n")
                    print(new_code)
                    print(f"\n==================================================")
                    choice = input("> Czy zgadzasz się, aby skompilować ten kod i wstrzyknąć w rdzeń OS? [Y/N]: ").strip().lower()
                    if choice in ['y', 'yes']:
                        # Zapis pliku
                        dynamic_dir = os.path.abspath(os.path.join(os.getcwd(), "workspace", "dynamic_atoms"))
                        import uuid
                        safe_filename = f"atom_{uuid.uuid4().hex[:6]}.py"
                        file_path = os.path.join(dynamic_dir, safe_filename)
                        if not os.path.exists(dynamic_dir):
                            os.makedirs(dynamic_dir)
                        with open(file_path, "w", encoding="utf-8") as raw_f:
                            raw_f.write(new_code)
                            
                        # Hot-Reload w pamięć RAM
                        PrimitiveRegistry.load_dynamic_atoms()
                        print(f"[SUCCESS] Nowy zmysl pomyslnie zintegrowany. Mozesz go uzywac w Intencjach, podajac jego nowa nazwe!")
                    else:
                        print(f"[REJECTED] Odmowiono wstrzykniecia. Kod zniszczony.")
                else:
                    print(f"[ERROR] Agent zawiodl podczas pisania Atoma lub Judge go zablokowal.")
                continue # Wróć po zbudowaniu atoma na początek menu
                
            # 2. Pre-processing (Tłumaczenie potocznego języka na techniczne polecenia BUG-4)
            processed_intent = preprocessor.process(intent)
            
            # 3. Kompilacja
            nodes = compiler.compile_intent(processed_intent)
            if not nodes:
                print("  -> [BŁĄD] Kompilator zwrócił pusty strumień. Zmień intencję.")
                continue

            # 3b. AUTO-EVOLUTION (Wykrywanie brakujących atomów - UPG-2)
            is_forge_planned = any(n.kind == "primitive" and n.execution.processor_ref == "design_atom" for n in nodes)
            
            for node in nodes:
                if node.kind == "primitive" and node.execution.processor_ref:
                    if node.execution.processor_ref not in PrimitiveRegistry._registry:
                        if is_forge_planned:
                            print(f"\n[AUTO-EVOLUTION] Narzedzie '{node.execution.processor_ref}' nie istnieje, ale Kuznia ma je w planie. Zezwalam na incepcje.")
                            continue
                            
                        print(f"\n[AUTO-EVOLUTION] Wykryto brakujący Atom: '{node.execution.processor_ref}'")
                        print(f"[AUTO-EVOLUTION] Uruchamiam proces projektowania brakującego narządu...")
                        
                        designer = ToolDesigner(model_name=selected_model)
                        # Tworzymy opis na podstawie kontekstu węzła
                        desc = f"Stwórz atom o nazwie '{node.execution.processor_ref}', który w payload przyjmuje argumenty: {list(node.execution.payload.keys())}"
                        new_code = designer.design_tool(desc)
                        
                        if new_code and designer.validate_code(new_code):
                            print(f"\n==================================================")
                            print(f"[KLAUZULA EWOLUCYJNA] Wygenerowano brakujący kod:")
                            print(f"==================================================\n")
                            print(new_code)
                            choice = input(f"> Czy chcesz zainstalować ten brakujący Atom '{node.execution.processor_ref}'? [Y/N]: ").strip().lower()
                            if choice in ['y', 'yes']:
                                dynamic_dir = os.path.abspath(os.path.join(os.getcwd(), "workspace", "dynamic_atoms"))
                                if not os.path.exists(dynamic_dir): os.makedirs(dynamic_dir)
                                import uuid
                                with open(os.path.join(dynamic_dir, f"auto_{node.execution.processor_ref}_{uuid.uuid4().hex[:4]}.py"), "w", encoding="utf-8") as f:
                                    f.write(new_code)
                                PrimitiveRegistry.load_dynamic_atoms()
                            else:
                                print("[!] Zrezygnowano. Egzekucja grafu może się nie udać.")
            
            # 4. Zapis do GraphDB
            start_node_id = None
            for node in nodes:
                store.add_node(node)
                if node.kind == "intent":
                    start_node_id = node.nodeId
                    
            if not start_node_id and len(nodes) > 0:
                 start_node_id = nodes[0].nodeId # Fallback jak AI się pogubi
                 
            # 3. Nawigacja Grafu
            print("\n--- Uruchomiono Egzkeutor (Topologia Mózgu) ---")
            engine.execute_node(start_node_id)
            
            # 4. MUTATOR SANDBOX (SELF-HEALING)
            failed_nodes = [n for n in store._nodes.values() if n.execution and n.execution.status == "failed"]
            for failed_node in failed_nodes:
                # Pobieramy prawdziwy log błędu z węzła (BUG-3 FIX)
                error_message = failed_node.execution.error or "Nieznany błąd wykonania Atomu."
                                 
                # Żądanie do AI, by wygenerowała łatkę bez naszej ingerencji !
                healed_node = mutator.heal_node(failed_node, error_msg=error_message)
                
                if healed_node and mutator.run_sandbox_judge(healed_node):
                    print(f"[IMMUNE SYSTEM] Mutacja zatwierdzona! Restartowanie urwanego przewodu neurologicznego do węzła: {healed_node.nodeId}")
                    # Aktualizacja bazy o naprawiony Payload w locie
                    store.update_node(healed_node)
                    # Dokończenie egzekucji tego urwanego procesu !
                    engine.execute_node(healed_node.nodeId)
                else:
                    print(f"[IMMUNE SYSTEM] Próba samo-naprawy zawiodła.")
                    
            # 5. Sprzątanie (Entropy)
            print("\n--- Uruchomiono Entropy (Garbage Collector) ---")
            store.process_entropy()

        except KeyboardInterrupt:
            print("\n[PANIC BUTTON] Wymuszono twarde zatrzymanie procesu (Ctrl+C).")
            print("[PANIC BUTTON] GraphMindOS wraca do menu Intencji...")
            continue
        except Exception as system_exc:
            print(f"\n[KRYTYCZNY BLAD SYSTEMU]: {system_exc}")

if __name__ == "__main__":
    main_loop()
