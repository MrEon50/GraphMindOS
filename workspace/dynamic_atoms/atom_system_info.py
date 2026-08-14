import os
import platform
import shutil
import sys
from core.engine.primitives import PrimitiveRegistry
from core.standards import resolve_filepath

@PrimitiveRegistry.register("system_info", "Zwraca podsumowanie diagnostyczne komputera (OS, CPU, RAM, dysk, Python). Opcjonalnie: filepath.")
def system_info(payload: dict) -> dict:
    os_name = platform.system()
    os_release = platform.release()
    os_version = platform.version()
    architecture = platform.machine()
    python_ver = sys.version.split(" ")[0]
    user_name = os.getlogin() if hasattr(os, 'getlogin') else os.environ.get('USERNAME', 'User')

    # Miejsce na dysku
    total, used, free = shutil.disk_usage("/")
    total_gb = round(total / (1024 ** 3), 2)
    used_gb = round(used / (1024 ** 3), 2)
    free_gb = round(free / (1024 ** 3), 2)

    cpu_count = os.cpu_count() or "Nieznana"

    report_lines = [
        "=== DIAGNOSTYKA SYSTEMOWA GraphMindOS ===",
        f" Użytkownik:       {user_name}",
        f" System Operacyjny:{os_name} {os_release} ({architecture})",
        f" Wersja OS:        {os_version}",
        f" Wersja Pythona:   {python_ver}",
        f" Liczba rdzeni CPU:{cpu_count}",
        f" Dysk Główny:      Razem: {total_gb} GB | Użyte: {used_gb} GB | Wolne: {free_gb} GB",
        "========================================="
    ]

    report_text = "\n".join(report_lines)
    print(f"\n{report_text}\n")

    result = {
        "content": report_text,
        "result": report_text,
        "os": os_name,
        "python": python_ver,
        "free_gb": free_gb,
        "status": "success"
    }

    target_file = payload.get("filepath") or payload.get("filename")
    if target_file:
        save_path = resolve_filepath(target_file)
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        result["saved_to"] = save_path
        print(f"[SYSTEM_INFO] Zapisano raport diagnostyczny w: {save_path}")

    return result
