from core.engine.primitives import PrimitiveRegistry
import os

@PrimitiveRegistry.register("write_file", "Zapisuje tekst do pliku. Przyjmuje: filepath, content (lub text_content/cleaned_text).")
def write_file(payload: dict) -> dict:
    # Szukaj sciezki pod wieloma kluczami
    filepath = payload.get("filepath") or payload.get("filename") or payload.get("path") or payload.get("output_path")
    # Szukaj tresci pod wieloma kluczami
    content = payload.get("content") or payload.get("cleaned_text") or payload.get("text_content") or payload.get("text")
    mode = payload.get("mode", "w")

    if not filepath or not isinstance(filepath, str):
        raise ValueError(f"Brak sciezki pliku. Dostepne klucze: {list(payload.keys())}")

    if not content:
        raise ValueError(f"Brak tresci do zapisania. Dostepne klucze: {list(payload.keys())}")

    abs_path = os.path.abspath(filepath)
    
    with open(abs_path, mode, encoding="utf-8") as f:
        f.write(content)

    print(f"[WRITE_FILE] Zapisano {len(content)} znakow do: {abs_path}")
    return {"status": "success", "filepath": abs_path, "bytes_written": len(content)}