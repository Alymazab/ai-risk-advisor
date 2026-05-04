"""
PDF Loader for AI Risk Advisor

Loads the NIST AI RMF PDF or any other PDF document from disk
and returns page-level text with metadata.

Run from project root:
    python -m app.ingestion.pdf_loader
"""

from pathlib import Path
from typing import List, Dict, Any

from pypdf import PdfReader


def load_pdf(file_path: str) -> List[Dict[str, Any]]:
    """
    Load a PDF file and return a list of page dictionaries.

    Each page dictionary contains:
    - page_number
    - text
    - source
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a PDF file, got: {path.suffix}")

    reader = PdfReader(str(path))
    pages: List[Dict[str, Any]] = []

    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        cleaned_text = " ".join(text.split())

        if cleaned_text:
            pages.append(
                {
                    "page_number": index,
                    "text": cleaned_text,
                    "source": str(path),
                }
            )

    return pages


if __name__ == "__main__":
    pdf_path = "data/raw/nist_ai_rmf.pdf"

    loaded_pages = load_pdf(pdf_path)

    print(f"Loaded {len(loaded_pages)} pages from {pdf_path}")

    if loaded_pages:
        print("\nPreview:")
        print(f"Page: {loaded_pages[0]['page_number']}")
        print(loaded_pages[0]["text"][:500])
