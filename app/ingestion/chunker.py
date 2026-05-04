"""
Chunker for AI Risk Advisor

Takes page-level PDF text from pdf_loader.py and splits it into smaller
overlapping chunks for retrieval-augmented generation.

Run from project root:
    python -m app.ingestion.chunker
"""

from typing import List, Dict, Any


def chunk_pages(
    pages: List[Dict[str, Any]],
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> List[Dict[str, Any]]:
    """
    Split loaded PDF pages into text chunks.

    Args:
        pages: List of page dictionaries from load_pdf().
        chunk_size: Maximum number of characters per chunk.
        chunk_overlap: Number of characters repeated between chunks.

    Returns:
        List of chunk dictionaries with text and metadata.
    """

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks: List[Dict[str, Any]] = []

    for page in pages:
        text = page.get("text", "")
        page_number = page.get("page_number")
        source = page.get("source")

        if not text.strip():
            continue

        start = 0
        chunk_index = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    {
                        "chunk_id": f"page_{page_number}_chunk_{chunk_index}",
                        "text": chunk_text,
                        "metadata": {
                            "source": source,
                            "page_number": page_number,
                            "chunk_index": chunk_index,
                        },
                    }
                )

            start += chunk_size - chunk_overlap
            chunk_index += 1

    return chunks


if __name__ == "__main__":
    from app.ingestion.pdf_loader import load_pdf

    pdf_path = "data/raw/nist_ai_rmf.pdf"

    pages = load_pdf(pdf_path)
    chunks = chunk_pages(pages)

    print(f"Loaded pages: {len(pages)}")
    print(f"Created chunks: {len(chunks)}")

    if chunks:
        print("\nPreview chunk:")
        print(f"Chunk ID: {chunks[0]['chunk_id']}")
        print(f"Metadata: {chunks[0]['metadata']}")
        print(chunks[0]["text"][:700])
