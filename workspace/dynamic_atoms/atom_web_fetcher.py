import urllib.request
import re
from bs4 import BeautifulSoup
from core.engine.primitives import PrimitiveRegistry
from core.standards import resolve_filepath

@PrimitiveRegistry.register("web_fetcher", "Pobiera treść strony WWW pod wskazanym adresem URL. Wymaga: url. Opcjonalnie: filepath.")
def web_fetcher(payload: dict) -> dict:
    url = payload.get("url") or payload.get("address") or payload.get("link")
    if not url:
        raise ValueError("Brak podanego adresu URL w parametrze 'url'.")

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) GraphMindOS/1.4'}
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            html_content = response.read().decode('utf-8', errors='ignore')

        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Usuń skrypty i style
        for script in soup(["script", "style", "header", "footer", "nav"]):
            script.extract()

        title = soup.title.string.strip() if soup.title else "Brak tytułu"
        text = soup.get_text(separator=' ')
        
        # Oczyść białe znaki
        cleaned_lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in cleaned_lines for phrase in line.split("  "))
        clean_text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Ogranicz długość podglądu do 3000 znaków
        summary_text = clean_text[:3000]

        result = {
            "title": title,
            "content": summary_text,
            "text": summary_text,
            "status": "success",
            "url": url
        }

        target_file = payload.get("filepath") or payload.get("filename")
        if target_file:
            save_path = resolve_filepath(target_file)
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(f"Tytuł: {title}\nURL: {url}\n\n{clean_text}")
            result["saved_to"] = save_path
            print(f"[WEB_FETCHER] Pobrano stronę '{title}' i zapisano w: {save_path}")
        else:
            print(f"[WEB_FETCHER] Pobrano stronę '{title}' ({len(summary_text)} znaków)")

        return result

    except Exception as e:
        raise RuntimeError(f"Błąd pobierania strony {url}: {e}")
