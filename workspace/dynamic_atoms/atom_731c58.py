from core.engine.primitives import PrimitiveRegistry
import shutil
import os

@PrimitiveRegistry.register("zip_archiver", "Pakuje wskazany folder zrodlowy (source) do archiwum zip (target).")
def zip_archiver(payload: dict) -> dict:
    source_folder = payload.get("source") or payload.get("path") or payload.get("source_folder")
    output_path = payload.get("target") or payload.get("filepath") or payload.get("output_path")

    if not source_folder or not output_path:
        raise ValueError("Brak odpowiednich kluczy zrodla (source/path) i celu (target/filepath).")
    
    if not os.path.isdir(source_folder):
        raise ValueError(f"Folder zrodlowy nie istnieje: {source_folder}")

    # Usunięcie ewentualnego rozszerzenia .zip aby uniknąć podwójnych rozszerzeń
    safe_name = output_path.rsplit(".zip", 1)[0] if output_path.endswith(".zip") else output_path
    
    try:
        archive_file = shutil.make_archive(safe_name, 'zip', source_folder)
    except Exception as e:
        raise ValueError(f"Blad systemu podczas tworzenia archiwum: {e}")
        
    msg = f"Spakowano {source_folder} do {archive_file}"
    print(f"[ZIP_ARCHIVER] {msg}")
    
    return {
        "filepath": archive_file,
        "target": archive_file,
        "message": msg
    }