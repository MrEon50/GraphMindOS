import os
from core.engine.primitives import PrimitiveRegistry
from core.standards import resolve_filepath

@PrimitiveRegistry.register("file_searcher", "Wyszukuje pliki w katalogu według rozszerzenia lub frazy w nazwie. Wymaga: path (lub folder). Opcjonalnie: extension, query.")
def file_searcher(payload: dict) -> dict:
    folder = payload.get("path") or payload.get("folder") or payload.get("directory") or "."
    abs_path = os.path.abspath(folder)
    
    extension = payload.get("extension") or payload.get("ext")
    query = payload.get("query") or payload.get("search") or payload.get("term")
    
    if extension and not extension.startswith("."):
        extension = "." + extension

    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Katalog nie istnieje: {abs_path}")

    matched_files = []
    
    for root, dirs, files in os.walk(abs_path):
        # Pomijaj __pycache__ i chroma_data
        if "__pycache__" in root or "chroma_data" in root or ".git" in root:
            continue
            
        for file in files:
            full_file_path = os.path.join(root, file)
            rel_file_path = os.path.relpath(full_file_path, abs_path)
            
            # Filtr rozszerzenia
            if extension and not file.lower().endswith(extension.lower()):
                continue
                
            # Filtr frazy
            if query and query.lower() not in file.lower():
                continue
                
            matched_files.append(rel_file_path)

    matched_str = "\n".join(matched_files) if matched_files else "Nie znaleziono pasujących plików."
    print(f"[FILE_SEARCHER] Znaleziono {len(matched_files)} plików w: {abs_path}")

    result = {
        "files": matched_files,
        "count": len(matched_files),
        "content": matched_str,
        "result": matched_str,
        "status": "success"
    }

    output_target = payload.get("filepath") or payload.get("filename")
    if output_target:
        save_path = resolve_filepath(output_target)
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(f"Wyniki wyszukiwania w '{abs_path}' (Rozszerzenie: {extension}, Fraza: {query}):\n\n")
            f.write(matched_str)
        result["saved_to"] = save_path
        print(f"[FILE_SEARCHER] Zapisano wynik wyszukiwania w: {save_path}")

    return result
