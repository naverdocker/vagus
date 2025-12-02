import os
from pypdf import PdfReader

def extract_text_from_pdf(file_path):
    """Reads a PDF file and returns its full text contents."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    reader = PdfReader(file_path)
    full_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    return full_text

def chunk_text(text, chunk_size=1000, overlap=100):
    """
    Splits a long string into smaller overlapping chunks.

    Args:
        text (str): The full document text.
        chunk_size (int): Characters per chunk.
        overlap (int): Characters to overlap between chunks to preserve context.

    Returns:
        list[str]: a list of text chunks.
    """
    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size

        # slice the text
        chunk = text[start:end]
        chunks.append(chunk)

        # Move the window forward, but step back by 'overlap' amount
        start += (chunk_size - overlap)

    return chunks
