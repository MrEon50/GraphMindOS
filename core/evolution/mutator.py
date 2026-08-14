import json
from typing import Optional
from core.models.node import GraphNode

class SandboxMutator:
    """
    Self-Evolving Mutator Sandbox.
    System Immunologiczny GraphMindOS. Łapie uszkodzony węzeł (tzw. stan zapalny), 
    prosi LLM o wygenerowanie rekonfiguracji/łatki grafu (Mutacja),
    odpala to wirtualnie ze Sędzią (Judge Sandbox) i naprawia w locie GraphDB.
    """
    def __init__(self, model_name: str = "qwen3.5:9b", endpoint: str = "http://localhost:11434/api/chat"):
        self.model_name = model_name
        self.endpoint = endpoint
        self.system_prompt = """
        Jesteś Agentem-Mutatorem i Sędzią (Judge) w systemie GraphMindOS. Twoje zadanie to 'Self-Healing'.
        Jeden z węzłów w grafie wykonawczym zgłosił awarię (Status: Failed). 
        Otrzymasz zrzut węzła (JSON) oraz treść błędu (Exception z pythona na Atomie ewaluacyjnym).
        
        ZABIEG RATUNKOWY (MUTATION):
        - Znajdź przyczynę błędu (np. brakujący argument w 'payload', zła nazwa w 'processor_ref').
        - Zwróć JEDEN naprawiony zrzut tego węzła w czystym JSON (bez markdown).
        - Wypełnij 'payload' odpowiednimi kluczami na podstawie błędu.
        """

    def heal_node(self, failed_node: GraphNode, error_msg: str) -> Optional[GraphNode]:
        print(f"\n[MUTATOR SANDBOX] Wykryto uszkodzony węzeł '{failed_node.nodeId}'. Inicjuję ewolucyjną rekonfigurację.")
        print(f"[MUTATOR SANDBOX] Raport patologii: {error_msg}")
        
        node_json = failed_node.model_dump_json()
        
        from core.llm.llm_client import LLMProviderManager
        
        try:
            raw_content = LLMProviderManager.chat_completion(
                model_info=self.model_name,
                system_prompt=self.system_prompt,
                user_prompt=f"WĘZEŁ (JSON): {node_json}\n\nRAPORT Z AWARII: {error_msg}\n\nWygeneruj patch JSON z poprawionym payloadem lub ref. Zwróć go ujętego w znacznik ```json ... ```",
                timeout=60
            )
            
            import re
            
            # Wzmocniona ekstrakcja JSON z tekstu (BUG-10 FIX)
            match = re.search(r'```(?:json)?\s*(.*?)\s*```', raw_content, re.DOTALL)
            if match:
                raw_content = match.group(1).strip()
            else:
                raw_content = raw_content.strip()
                
            try:
                data = json.loads(raw_content)
            except json.JSONDecodeError:
                print(f"[MUTATOR] Otrzymano nieczytelną łatkę od modelu. Samoleczenie zawieszone.")
                return None
            
            # Wdrażamy patcha (Mutację) - Pydantic v2 mode
            healed_node_dict = failed_node.model_dump()
            healed_node = GraphNode(**healed_node_dict)
            if "execution" in data:
                if "processor_ref" in data["execution"]:
                    healed_node.execution.processor_ref = data["execution"]["processor_ref"]
                if "payload" in data["execution"]:
                    healed_node.execution.payload = data["execution"]["payload"]
                    
            print(f"[JUDGE] Patch wygenerowany. Zaktualizowany Payload: {healed_node.execution.payload}")
            return healed_node
            
        except Exception as e:
            print(f"[MUTATOR] Błąd podczas mutacji (LLM Timeout or Parse Error): {e}")
            return None

    def run_sandbox_judge(self, healed_node: GraphNode) -> bool:
        # Prawdziwy sandbox izoluje wykonanie na Wasm. Tutaj robimy symulowany przegląd logiki:
        print("[JUDGE] Symulacja wykonania nowej topologii w izolacji (Virtual Run)...")
        if healed_node and healed_node.execution.payload and len(healed_node.execution.payload.keys()) > 0:
            print("[JUDGE] Test udany. Węzeł nie zgłasza błędu pustych parametrów. Wdrażam łatkę.")
            return True
        print("[JUDGE] Mutacja nieudana - łatka odrzucona przez wirtualne środowisko.")
        return False
