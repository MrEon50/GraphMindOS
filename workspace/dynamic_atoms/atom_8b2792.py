from core.engine.primitives import PrimitiveRegistry
import shutil
from pathlib import Path

@PrimitiveRegistry.register("file_operator", "Bezpieczne kopiowanie lub przenoszenie plików")
def file_operator(payload: dict) -> dict:
    try:
        source = payload.get("source")
        target = payload.get("target")
        action = payload.get("action", "copy")

        if not isinstance(source, str) or not isinstance(target, str):
            raise ValueError("Pola 'source' i 'target' musza byc typem string.")

        src_path = Path(source).resolve()
        tgt_path = Path(target).resolve()

        if not src_path.exists():
            raise ValueError("Podana ścieżka źródłowa nie istnieje.")

        if action == "move":
            if tgt_path.exists():
                raise ValueError("Ścieżka docelowa już istnieje przy operacji move.")
            shutil.move(str(src_path), str(tgt_path))
            return {"status": "success", "action": "moved", "source": str(src_path), "target": str(tgt_path)}
        elif action == "copy":
            if tgt_path.exists():
                raise ValueError("Ścieżka docelowa już istnieje przy operacji copy.")
            shutil.copy2(src_path, tgt_path)
            return {"status": "success", "action": "copied", "source": str(src_path), "target": str(tgt_path)}
        else:
            raise ValueError("Akcyjna metoda musi byc 'copy' lub 'move'.")

    except Exception as e:
        raise ValueError(f"Błąd operacji na plikach: {str(e)}")