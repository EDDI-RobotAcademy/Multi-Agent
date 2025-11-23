from PyPDF2 import PdfReader

def parse_document(content: bytes, cache_path: str) -> str:
    with open(cache_path, "wb") as f:
        f.write(content)
    reader = PdfReader(cache_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text
