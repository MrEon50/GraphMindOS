import secrets
import string
from core.engine.primitives import PrimitiveRegistry

@PrimitiveRegistry.register("generate_password", "Generuje losowe haslo o podanej dlugosci. Przyjmuje: length, count.")
def generate_password(payload: dict) -> dict:
    # Szukanie długości pod wieloma kluczami
    length = payload.get("length") or payload.get("count")

    if length is None:
        raise ValueError("Brak podanej dlugosci hasla (wymagany klucz 'length' lub 'count').")

    try:
        length_int = int(length)
    except (ValueError, TypeError):
        raise ValueError("Podana dlugosc hasla musi byc liczbą całkowitą.")

    if length_int < 4 or length_int > 128:
        raise ValueError("Dlugosc hasla musi miezcic sie w zakresie od 4 do 128 znakow.")

    # Definicja zestawu znaków (litery, cyfry i znaki specjalne)
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?"
    
    # Generowanie bezpiecznego hasla
    password = ''.join(secrets.choice(alphabet) for _ in range(length_int))

    return {
        "content": password,
        "status": "success",
        "message": f"Wygenerowano losowe haslo o dlugosci {length_int}."
    }