from core.engine.primitives import PrimitiveRegistry

@PrimitiveRegistry.register("text_cleaner", "Czysci tekst. Tryby: lowercase, strip_spaces, strip_all_spaces, strip_special. Przyjmuje: text lub text_content. Opcjonalnie: mode (domyslnie: lowercase,strip_spaces).")
def text_cleaner(payload: dict) -> dict:
    # Szukaj tekstu pod wieloma kluczami
    text = payload.get("text") or payload.get("text_content") or payload.get("content") or payload.get("cleaned_text")
    
    if not text or not isinstance(text, str):
        raise ValueError(f"Brak tekstu do czyszczenia. Dostepne klucze: {list(payload.keys())}")
    
    # Tryby czyszczenia - konfigurowalny przez payload
    mode = payload.get("mode", "lowercase,strip_spaces")
    modes = [m.strip() for m in mode.split(",")]
    
    result = text
    
    if "lowercase" in modes:
        result = result.lower()
    
    if "strip_all_spaces" in modes:
        # Usun WSZYSTKIE spacje
        result = result.replace(" ", "").replace("\t", "")
    elif "strip_spaces" in modes:
        # Normalizuj spacje (wiele spacji -> jedna)
        result = " ".join(result.split())
    
    if "strip_special" in modes:
        # Usun znaki specjalne ALE zachowaj litery (w tym polskie), cyfry i spacje
        cleaned = []
        for char in result:
            if char.isalpha() or char.isdigit() or char.isspace():
                cleaned.append(char)
        result = "".join(cleaned)
    
    print(f"[TEXT_CLEANER] Tryb: {mode} | {len(text)} -> {len(result)} znakow.")
    
    return {"cleaned_text": result, "text_content": result, "content": result}