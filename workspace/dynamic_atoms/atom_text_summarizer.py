import re
from collections import Counter
from core.engine.primitives import PrimitiveRegistry
from core.standards import resolve_filepath

@PrimitiveRegistry.register("text_summarizer", "Generuje statystyki i analityczne podsumowanie tekstu (słowa, zdania, kluczowe frazy). Wymaga: text lub filepath.")
def text_summarizer(payload: dict) -> dict:
    text = payload.get("text") or payload.get("content")
    target_file = payload.get("filepath") or payload.get("filename")

    if not text and target_file:
        read_path = resolve_filepath(target_file)
        with open(read_path, 'r', encoding='utf-8') as f:
            text = f.read()

    if not text:
        raise ValueError("Brak tekstu do podsumowania w 'text' ani w pliku 'filepath'.")

    # Podstawowa analityka
    words = re.findall(r'\b\w+\b', text.lower())
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    word_count = len(words)
    sentence_count = len(sentences)
    char_count = len(text)

    # Filtr słów pomocniczych (stop words PL/EN)
    stop_words = {'w', 'z', 'i', 'na', 'do', 'to', 'że', 'o', 'a', 'jak', 'od', 'po', 'za', 'tak', 'ale', 'dla', 'lub', 'the', 'and', 'is', 'in', 'it', 'of', 'to', 'for', 'with', 'on', 'at'}
    filtered_words = [w for w in words if len(w) > 3 and w not in stop_words]
    top_words = Counter(filtered_words).most_common(5)

    keywords_str = ", ".join(f"{w} ({c}x)" for w, c in top_words) if top_words else "Brak"

    summary_lines = [
        "=== PODSUMOWANIE ANALITYCZNE TEKSTU ===",
        f" Liczba znaków:    {char_count}",
        f" Liczba słów:      {word_count}",
        f" Liczba zdań:      {sentence_count}",
        f" Najczęstsze słowa: {keywords_str}",
        "======================================="
    ]

    report_text = "\n".join(summary_lines)

    result = {
        "content": report_text,
        "result": report_text,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "keywords": [w for w, c in top_words],
        "status": "success"
    }

    output_file = payload.get("target_filepath") or payload.get("target_filename")
    if output_file:
        save_path = resolve_filepath(output_file)
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(report_text + "\n\nOryginalny tekst:\n" + text)
        result["saved_to"] = save_path
        print(f"[TEXT_SUMMARIZER] Zapisano podsumowanie w: {save_path}")

    return result
