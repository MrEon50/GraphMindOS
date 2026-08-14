from core.engine.primitives import PrimitiveRegistry
import subprocess

@PrimitiveRegistry.register("cmd_executor", "Uruchamia polecenia systemowe. Zwraca: console_output.")
def cmd_executor(payload: dict) -> dict:
    command = payload.get("command") or payload.get("text_content") or payload.get("text")
    if not command:
        raise ValueError("Brak kluczowej komendy 'command' w payloadu.")
    
    # Wykonanie komendy w domylnej powloce (Windows: cmd.exe)
    # Zauwaz: Jesli chcesz uzyc cmdletow PowerShell, komenda musi zaczynac sie od "powershell -c ..."
    result = subprocess.run(
        command, 
        shell=True, 
        capture_output=True, 
        text=True, 
        encoding="utf-8"
    )
    
    full_output = ""
    if result.stdout:
        full_output += result.stdout.strip()
    if result.stderr:
        full_output += "\n\n" + result.stderr.strip()
        
    # CHIRURGICZNA POPRAWKA:
    # Wczesniej `subprocess.run` bez `check=True` nie rzucal wyjatku TheCalledProcessError,
    # przez co powazne bledy powloki byly ignorowane! 
    if result.returncode != 0:
        error_msg = f"Komenda zakonczyla sie bledem (kod {result.returncode}).\nKonsola zwrocila:\n{full_output}"
        print(f"[CMD_EXECUTOR] {error_msg}")
        raise ValueError(error_msg)
        
    payload["console_output"] = full_output
    print(f"[CMD_EXECUTOR] Komenda wykonana pomyslnie. Wynik: {len(full_output)} znakow.")

    return payload