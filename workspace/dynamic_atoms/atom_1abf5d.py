from core.engine.primitives import PrimitiveRegistry
import os
import shutil

@PrimitiveRegistry.register("deleteFile", "Usuwanie plikow i folderow z systemu. Akceptuje: filepath, path, filename.")
def deleteFile(payload: dict) -> dict:
    filepath = payload.get("filepath") or payload.get("path") or payload.get("filename")
    
    if not filepath:
        raise ValueError("Brak podanej sciezki w payload.")
        
    full_path = os.path.abspath(filepath)
    
    if not os.path.exists(full_path):
        raise ValueError(f"Podana sciezka nie istnieje: {full_path}")
        
    try:
        if os.path.isdir(full_path):
            shutil.rmtree(full_path)
            print(f"[DELETE] Usunięto cały folder z zawartością: {full_path}")
        else:
            os.remove(full_path)
            print(f"[DELETE] Plik usuniety: {full_path}")
    except PermissionError as e:
        raise ValueError(f"Brak uprawnien lub plik jest uzywany przez inny program: {e}")
    except Exception as e:
        raise ValueError(f"Wystapil nieoczekiwany blad: {e}")
        
    return {"message": f"Obiekt {full_path} zostal pomyslnie usuniety ze wszystkimi elementami."}