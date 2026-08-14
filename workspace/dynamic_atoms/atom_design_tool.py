from core.engine.primitives import PrimitiveRegistry
from core.evolution.tool_designer import ToolDesigner
import uuid
import os

@PrimitiveRegistry.register("design_atom", "Autonomiczna Kuźnia. Tworzy nowy Atom w locie. Wymaga: text (opis czego potrzebuje nowe narzędzie).")
def design_atom(payload: dict) -> dict:
    concept = payload.get("text") or payload.get("text_content") or payload.get("content") or payload.get("message")
    
    if not concept:
        raise ValueError("Kuźnia wymaga opisu narzędzia w kluczu 'text' lub 'message'.")
        
    print(f"[KUŹNIA NARZĘDZI] Rozpoczynam kucie narzędzia pod koncept: '{concept}'")
    
    designer = ToolDesigner()
    max_forge_attempts = 3
    new_code = ""
    current_prompt = concept
    
    for attempt in range(1, max_forge_attempts + 1):
        print(f"[KUŹNIA NARZĘDZI] Kucie (Próba {attempt}/{max_forge_attempts})...")
        new_code = designer.design_tool(current_prompt)
        
        if not new_code or "def " not in new_code:
            current_prompt = f"ZROBIŁEŚ BŁĄD. Twój kod musi zawierać w pełni poprawną logikę Pythona (def nazwa_narzedzia(payload)). Spróbuj jeszcze raz dla konceptu: {concept}"
            continue
            
        # Selektywny Sandbox: Testowanie WYŁĄCZNIE nowego, nietestowanego kodu
        from core.evolution.sandbox_validator import SandboxValidator
        is_valid, validation_msg = SandboxValidator.validate_and_test_atom(new_code)
        
        if is_valid:
            print(f"[KUŹNIA NARZĘDZI] ✅ Kod pomyślnie przeszedł testy w Piaskownicy: {validation_msg}")
            break
        else:
            print(f"[KUŹNIA NARZĘDZI] ❌ Test w Piaskownicy nieudany: {validation_msg}")
            current_prompt = f"Twój poprzedni kod nie przeszedł testów w Piaskownicy ({validation_msg}). Popraw go dla konceptu: {concept}"
            
    else:
        raise ValueError("Kuźnia zawiodła: Model nie wygenerował poprawnego kodu po 3 próbach samo-naprawy w Piaskownicy.")
        
    # Kod przeszedł testy w Piaskownicy - staje się zaufany i zostaje wdrożony bezpośrednio do rdzenia OS
    
    dynamic_dir = os.path.abspath(os.path.join(os.getcwd(), "workspace", "dynamic_atoms"))
    safe_filename = f"atom_{uuid.uuid4().hex[:6]}.py"
    file_path = os.path.join(dynamic_dir, safe_filename)
    
    os.makedirs(dynamic_dir, exist_ok=True)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_code)
        
    print(f"[KUŹNIA NARZĘDZI] Wykuto zmysł! Zapisano jako: {safe_filename}")
    
    # Reload do RAMu w tym samym ułamku sekundy
    PrimitiveRegistry.load_dynamic_atoms()
    
    return {
        "status": "success",
        "message": f"Narzędzie zostało stworzone i załadowane z pliku {safe_filename}.",
        "filepath": file_path
    }
