import json
from core.engine.primitives import PrimitiveRegistry
from core.standards import resolve_filepath

@PrimitiveRegistry.register("json_processor", "Parsuje, waliduje i ładnie formatuje struktury JSON lub wyciąga klucze. Wymaga: text (lub filepath). Opcjonalnie: query_key.")
def json_processor(payload: dict) -> dict:
    raw_json = payload.get("text") or payload.get("content") or payload.get("json_string")
    target_file = payload.get("filepath") or payload.get("filename")

    if not raw_json and target_file:
        read_path = resolve_filepath(target_file)
        with open(read_path, 'r', encoding='utf-8') as f:
            raw_json = f.read()

    if not raw_json:
        raise ValueError("Brak podanej treści JSON w 'text' ani w podanym pliku 'filepath'.")

    try:
        data = json.loads(raw_json)
    except Exception as e:
        raise ValueError(f"Błąd składniowy JSON: {e}")

    query_key = payload.get("query_key") or payload.get("key")
    if query_key:
        extracted = data.get(query_key) if isinstance(data, dict) else None
        formatted_result = json.dumps(extracted, indent=2, ensure_ascii=False)
        msg = f"Wartość klucza '{query_key}':\n{formatted_result}"
    else:
        formatted_result = json.dumps(data, indent=2, ensure_ascii=False)
        msg = f"Sformatowana struktura JSON:\n{formatted_result}"

    print(f"[JSON_PROCESSOR] Pomyślnie przetworzono JSON.")

    result = {
        "content": formatted_result,
        "result": formatted_result,
        "json_data": data,
        "status": "success"
    }

    output_file = payload.get("target_filepath") or payload.get("target_filename")
    if output_file:
        save_path = resolve_filepath(output_file)
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(formatted_result)
        result["saved_to"] = save_path
        print(f"[JSON_PROCESSOR] Zapisano przetworzony JSON w: {save_path}")

    return result
