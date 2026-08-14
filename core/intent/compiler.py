import time
from typing import List
from core.models.node import GraphNode, Topology, Relationship, Execution, Entropy
from core.engine.primitives import PrimitiveRegistry
from core.standards import get_standards_for_prompt

class IntentCompiler:
    """
    Kompilator Intencji v4 - Simple Step Format.
    Zamiast prosic LLM o skomplikowany JSON, prosi o prosta liste krokow.
    Python sam buduje graf DAG z tych krokow.
    """
    
    def __init__(self, model_name: str = "qwen2.5-coder:14b-instruct-q8_0", endpoint: str = "http://localhost:11434/api/chat"):
        self.model_name = model_name
        self.endpoint = endpoint
        self.max_retries = 3
        
        standards = get_standards_for_prompt()
        self.system_prompt = f"""Jestes kompilatorem GraphMindOS. Zamien intencje na liste krokow.

FORMAT WYJSCIOWY - kazdy krok w nowej linii:
STEP: nazwa_narzedzia || klucz1=wartosc1 || klucz2=wartosc2

{standards}

PRZYKLAD 1 - "Odczytaj plik C:/test.txt i wyczysc tekst":
STEP: read_file || filepath=C:/test.txt
STEP: ask_user_permission || action_description=Modyfikacja pliku || consequences=Plik zostanie zmieniony
STEP: text_cleaner
STEP: write_file || filepath=C:/test.txt

PRZYKLAD 2 - "Wylistuj pliki w folderze C:/dane":
STEP: read_directory || path=C:/dane
STEP: log_message

PRZYKLAD 3 - "Uruchom komende ipconfig":
STEP: ask_user_permission || action_description=Uruchomienie komendy systemowej || consequences=Wykonanie komendy w konsoli
STEP: cmd_executor || command=ipconfig

PRZYKLAD 4 - "Cześć / Kim jesteś / Dzień dobry":
STEP: ai_chat || message=Witaj! Jestem GraphMindOS. W czym mogę Ci dzisiaj pomóc?

Zasady:
1. Zwroc TYLKO linie STEP: (bez innego tekstu, bez markdown).
2. Uzyj TYLKO narzedzi z listy ponizej.
3. Dla operacji modyfikujacych pliki/system DODAJ ask_user_permission.
4. Payload text_cleaner moze byc pusty (dostanie dane z poprzedniego kroku).
5. NIGDY nie wymyslaj nowych narzedzi Z WYJATKIEM jednej sytuacji:
   -> Jesli nie masz narzedzia do zadania (np. split_pdf), zaplanuj krok 'design_atom' i podaj w 'text' czego potrzebujesz. 
   -> W NASTEPNYM kroku mozesz BEZKARNIE uzyc nazwy tego wymyslonego narzedzia (Kuznia wykuje je dla Ciebie sekunde wczesniej)."""

    def _parse_steps(self, raw_text: str) -> List[dict]:
        """Parsuje prosty format STEP: do listy slownikow."""
        steps = []
        for line in raw_text.strip().split('\n'):
            line = line.strip()
            if not line.startswith('STEP:'):
                continue
            
            line = line[5:].strip()  # Usun 'STEP:'
            parts = [p.strip() for p in line.split('||')]
            
            if not parts:
                continue
                
            tool_name = parts[0].strip()
            payload = {}
            
            for part in parts[1:]:
                if '=' in part:
                    key, value = part.split('=', 1)
                    payload[key.strip()] = value.strip()
            
            steps.append({"tool": tool_name, "payload": payload})
        
        return steps

    def _build_graph(self, steps: List[dict]) -> List[GraphNode]:
        """Buduje pelny graf DAG z prostej listy krokow."""
        nodes = []
        total = len(steps)
        
        # Wezel startowy (intent)
        first_target = "step_1" if total > 0 else "final_state"
        start_node = GraphNode(
            nodeId="intent_start",
            kind="intent",
            execution=Execution(processor_ref=None, payload={"message": "Intent received"}),
            topology=Topology(outputs=[Relationship(targetId=first_target, relationshipType="next", weight=1.0)]),
            entropy=Entropy()
        )
        nodes.append(start_node)
        
        # Wezly krokow (primitive)
        for i, step in enumerate(steps):
            node_id = f"step_{i+1}"
            
            # Nastepny wezel
            if i + 1 < total:
                next_id = f"step_{i+2}"
            else:
                next_id = "final_state"
            
            # Warunek dla ask_user_permission
            outputs = []
            if step["tool"] == "ask_user_permission":
                outputs.append(Relationship(
                    targetId=next_id, 
                    relationshipType="next", 
                    weight=1.0,
                    condition="permission_granted == True"
                ))
            else:
                outputs.append(Relationship(
                    targetId=next_id, 
                    relationshipType="next", 
                    weight=1.0
                ))
            
            node = GraphNode(
                nodeId=node_id,
                kind="primitive",
                execution=Execution(processor_ref=step["tool"], payload=step["payload"]),
                topology=Topology(outputs=outputs),
                entropy=Entropy()
            )
            nodes.append(node)
        
        # Wezel koncowy (state)
        final_node = GraphNode(
            nodeId="final_state",
            kind="state",
            execution=Execution(processor_ref=None, payload={"text_content": "Zadanie zakonczone"}),
            topology=Topology(outputs=[]),
            entropy=Entropy()
        )
        nodes.append(final_node)
        
        return nodes

    def compile_intent(self, user_intent: str) -> List[GraphNode]:
        # Dynamicznie laduj dostepne narzedzia
        tools_desc = []
        for name, desc in PrimitiveRegistry._descriptions.items():
            tools_desc.append(f"- '{name}': {desc}")
        
        atoms_str = "\n".join(tools_desc)
        full_prompt = self.system_prompt + f"\n\nDOSTEPNE NARZEDZIA:\n{atoms_str}"
        
        from core.llm.llm_client import LLMProviderManager
        print(f"[COMPILER] Translating Intent via LLM ({self.model_name}): '{user_intent}'")
        
        for attempt in range(1, self.max_retries + 1):
            try:
                timeout = 60 * attempt
                raw_content = LLMProviderManager.chat_completion(
                    model_info=self.model_name,
                    system_prompt=full_prompt,
                    user_prompt=user_intent,
                    timeout=timeout
                )
                
                # Parsuj kroki
                steps = self._parse_steps(raw_content)
                
                if not steps:
                    print(f"[COMPILER] Brak krokow STEP: w odpowiedzi (proba {attempt}/{self.max_retries}).")
                    if attempt < self.max_retries:
                        time.sleep(2)
                        continue
                    return []
                
                # Walidacja: sprawdz czy narzedzia istnieja
                available = set(PrimitiveRegistry._registry.keys())
                for step in steps:
                    if step["tool"] not in available:
                        print(f"[COMPILER] Ostrzezenie: Narzedzie '{step['tool']}' nie istnieje w rejestrze!")
                
                # Zbuduj graf z krokow
                nodes = self._build_graph(steps)
                
                # Pokaz plan uzytkownikowi
                print(f"[COMPILER] Plan wykonania ({len(steps)} krokow):")
                for i, step in enumerate(steps, 1):
                    params = ", ".join(f"{k}={v}" for k, v in step["payload"].items())
                    print(f"   {i}. {step['tool']}" + (f" ({params})" if params else ""))
                
                return nodes
                
            except Exception as e:
                print(f"[COMPILER] Błąd podczas kompilacji (próba {attempt}/{self.max_retries}): {e}")
                if attempt < self.max_retries:
                    time.sleep(2)
                    continue
                return []
        
        print(f"[COMPILER] Nie udalo sie skompilowac po {self.max_retries} probach.")
        return []
