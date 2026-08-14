from core.storage.hybrid_store import HybridStore
from core.engine.evaluator import SafeEvaluator
from core.engine.primitives import PrimitiveRegistry
from core.standards import KEY_ALIASES

class RoutingEngine:
    """
    Egzekutor Logiki oparty na DAG i wagach przejsc.
    Posiada Smart Key Mapper do automatycznego tlumaczenia kluczy miedzy narzedziami.
    """
    
    def __init__(self, store: HybridStore, max_depth: int = 50):
        self.store = store
        self.max_depth = max_depth

    def _resolve_keys(self, payload: dict, processor_ref: str) -> dict:
        """
        Smart Key Mapper: automatycznie mapuje klucze miedzy narzedziami.
        Jesli narzedzie spodziewa sie klucza 'text' ale w payloadzie jest 'text_content',
        system automatycznie skopiuje wartosc.
        """
        resolved = dict(payload)
        
        for target_key, aliases in KEY_ALIASES.items():
            # Jesli klucz docelowy juz istnieje i ma wartosc - nie nadpisuj
            if target_key in resolved and resolved[target_key]:
                continue
        from core.standards import resolve_filepath
        
        # Automatyczne rozstrzyganie ścieżek względem domyślnego folderu workspace/data/
        for fp_key in ["filepath", "filename"]:
            if fp_key in resolved and isinstance(resolved[fp_key], str) and resolved[fp_key]:
                resolved[fp_key] = resolve_filepath(resolved[fp_key])

        return resolved

    def execute_node(self, node_id: str, depth: int = 0):
        if depth > self.max_depth:
            print(f"[ENGINE-ALERT] Infinite loop detected at depth {depth}! Halting.")
            return

        node = self.store.get_node(node_id)
        if not node:
            return
            
        print(f"[ENGINE] Executing node: {node_id} (Kind: {node.kind})")
        
        # Wykonanie Atoma (Primitive)
        if node.kind == "primitive":
            node.execution.status = "running"
            
            if node.execution.payload is None:
                node.execution.payload = {}
            
            if node.execution.processor_ref:
                try:
                    # SMART KEY MAPPER: rozwiaz aliasy kluczy przed wykonaniem
                    resolved_payload = self._resolve_keys(node.execution.payload, node.execution.processor_ref)
                    # Diagnostyka przeplywu danych
                    payload_keys = [k for k, v in resolved_payload.items() if v]
                    result = PrimitiveRegistry.execute(node.execution.processor_ref, resolved_payload)
                    node.execution.payload.update(result)
                    node.execution.status = "completed"
                    
                    # Automatyczny wyświetlacz wyniku dla użytkownika
                    if node.execution.processor_ref not in ["log_message", "ai_chat"] and isinstance(result, dict):
                        out_val = result.get("content") or result.get("result") or result.get("text_content") or result.get("response")
                        if out_val:
                            print(f"\n✨ [WYNIK ATOMU '{node.execution.processor_ref}']: {out_val}\n")
                except Exception as e:
                    print(f"   -> [!] Atom Execution Failed: {e}")
                    node.execution.status = "failed"
                    node.execution.error = str(e)
            else:
                node.execution.status = "completed"
                
            print(f"   -> Atom status: {node.execution.status}")
        
        # Nawigacja i routing
        outputs = node.topology.outputs
        sorted_outputs = sorted(outputs, key=lambda x: x.weight, reverse=True)
        
        dispatched = False
        for out in sorted_outputs:
            if SafeEvaluator.evaluate(out.condition, node.execution.payload):
                print(f"   -> Routing to {out.targetId} (Weight: {out.weight})")
                dispatched = True
                
                # PRZEKAZYWANIE PAYLOADU
                target_node = self.store.get_node(out.targetId)
                if target_node and target_node.execution:
                    if target_node.execution.payload is None:
                        target_node.execution.payload = {}
                    
                    # BARDZO WAZNE (CHIRURGICZNA POPRAWKA): 
                    # Zbieramy payload z poprzedniego wezla (stan dynamiczny), 
                    # ALER nadpisujemy go tym co kompilator TWARDO ustawil w wezle docelowym.
                    incoming_payload = dict(node.execution.payload)
                    incoming_payload.update(target_node.execution.payload) # Twarde ustawienia kompilatora wygrywaja
                    target_node.execution.payload = incoming_payload
                
                self.execute_node(out.targetId, depth=depth + 1)
                break
                
        if not dispatched and len(sorted_outputs) > 0:
            print(f"   -> [!] No outputs satisfied conditions for node: {node_id}")
            node.execution.status = "failed"

