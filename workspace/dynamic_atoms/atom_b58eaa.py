from core.engine.primitives import PrimitiveRegistry
import os

@PrimitiveRegistry.register("file_renamer", "Zmienia nazwy plikow w folderze (np. dodaje numeracje). Wymaga: path.")
def file_renamer(payload: dict) -> dict:
    target_folder = payload.get("path") or payload.get("filepath")
    
    if not target_folder:
        raise ValueError("Brak klucza 'path' wymaganego do renumeracji plikow.")
        
    if not os.path.exists(target_folder) or not os.path.isdir(target_folder):
        raise ValueError(f"Sciezka nie istnieje lub nie jest folderem: {target_folder}")
        
    # Pobierz pliki z katalogu i posortuj je
    items = sorted(os.listdir(target_folder))
    files = [f for f in items if os.path.isfile(os.path.join(target_folder, f))]
    
    if not files:
        raise ValueError(f"Folder jest pusty, brak plikow do zmiany nazwy: {target_folder}")

    count = 0
    for idx, filename in enumerate(files, start=1):
        old_path = os.path.join(target_folder, filename)
        
        # Ekstrakcja starej nazwy i rozszerzenia
        name, ext = os.path.splitext(filename)
        
        # Nowa nazwa: 01_StaraNazwa.ext, 02_StaraNazwa.ext itd.
        # Zero-padding dla estetyki (np. 01, 02, ..., 10)
        new_name = f"{idx:02d}_{name}{ext}"
        new_path = os.path.join(target_folder, new_name)
        
        # Zabezpieczenie przed nadpisywaniem istniejacych (rzadka sytuacja, ale sie zdarza)
        if not os.path.exists(new_path) and old_path != new_path:
            os.rename(old_path, new_path)
            count += 1
            
    msg = f"Pomyslnie ponumerowano i zmieniono nazwy {count} plikom w katalogu {target_folder}."
    print(f"[FILE_RENAMER] {msg}")
    
    return {"message": msg, "count": count, "renamed_files": count}
