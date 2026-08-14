from core.engine.primitives import PrimitiveRegistry
import os
import shutil

@PrimitiveRegistry.register("file_sorter", "Sortuje pliki w folderze wg ich rozszerzenia. Wymaga: path.")
def file_sorter(payload: dict) -> dict:
    target_folder = payload.get("path") or payload.get("target_folder") or payload.get("filepath")
    
    if not target_folder:
        raise ValueError("Brak klucza 'path' w parametrach wejsciowych.")
    
    # Walidacja sciezki folderu
    if not os.path.isdir(target_folder):
        raise ValueError(f"Sciezka '{target_folder}' nie istnieje lub nie jest folderem.")
        
    items = os.listdir(target_folder)
    count = 0
    
    for item in items:
        filepath = os.path.join(target_folder, item)
        
        # Pomijamy podfoldery (subfolders)
        if os.path.isdir(filepath):
            continue
        
        _, ext = os.path.splitext(item)
        extension_name = ext.lstrip('.') or "bez_rozszerzenia"
        target_dir = os.path.join(target_folder, extension_name)
        
        os.makedirs(target_dir, exist_ok=True)
        shutil.move(filepath, os.path.join(target_dir, item))
        count += 1
    
    msg = f"Posortowano {count} plikow w folderze {target_folder}."
    print(f"[FILE_SORTER] {msg}")
    
    return {"message": msg, "count": count}