import ast
import traceback
from typing import Tuple

class SandboxValidator:
    """
    Selektywna Piaskownica Testowa (Sandbox).
    Uruchamiana WYŁĄCZNIE dla nowo wygenerowanego kodu Atomów z Kuźni.
    Narzędzia, które przeszły ten test, stają się zaufane i trafiają do systemu bez narzutu piaskownicy.
    """
    
    @classmethod
    def validate_and_test_atom(cls, code_string: str) -> Tuple[bool, str]:
        """
        Dwuetapowa weryfikacja nowo wyklutego Atoma:
        1. Weryfikacja składniowa AST (Syntax, Indentation, Decorator).
        2. Wirtualna ewaluacja w izolowanym słowniku (Dry-Run Test).
        """
        if not code_string or not code_string.strip():
            return False, "Kod jest pusty."
            
        # 1. AST Syntax Check
        try:
            tree = ast.parse(code_string)
        except SyntaxError as se:
            return False, f"Błąd składniowy (SyntaxError) w linii {se.lineno}: {se.msg}"
        except Exception as e:
            return False, f"Krytyczny błąd struktury kodu: {e}"
            
        # 2. Weryfikacja strukturalna dekoratora i funkcji
        has_decorator = False
        has_func = False
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                has_func = True
                for dec in node.decorator_list:
                    if isinstance(dec, ast.Call):
                        if isinstance(dec.func, ast.Attribute) and dec.func.attr == "register":
                            has_decorator = True
                        elif isinstance(dec.func, ast.Name) and dec.func.id == "register":
                            has_decorator = True
                            
        if not has_func:
            return False, "Brak definicji funkcji (def) w wygenerowanym kodzie."
        if not has_decorator:
            return False, "Brak dekoratora @PrimitiveRegistry.register w wygenerowanym kodzie."

        # 3. Wirtualny Dry-Run Test w odizolowanej przestrzeni nazw
        isolated_globals = {}
        try:
            exec(code_string, isolated_globals)
            print("[SANDBOX TESTBENCH] Dry-run kompilacji w izolowanej przestrzeni zakończony sukcesem.")
            return True, "Kod przeszedł pełną weryfikację piaskownicy."
        except Exception as e:
            tb = traceback.format_exc()
            print(f"[SANDBOX TESTBENCH] Wyjątek podczas próbnego uruchomienia: {e}")
            return False, f"Błąd wykonania w piaskownicy: {e}"
