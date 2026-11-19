from dataclasses import dataclass
import re


@dataclass(frozen=True)
class TextChunk:
    text: str
    chunk_index: int
    metadata: dict


def _clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(
    text: str,
    *,
    chunk_size: int = 900,
    overlap: int = 120,
    metadata: dict | None = None,
) -> list[TextChunk]:
    """Split extracted material into overlapping, retrievable chunks.

    The function is deliberately independent of PDF/database code so Member 3
    can later persist the same chunks and their metadata.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size")

    cleaned = _clean_text(text)
    if not cleaned:
        return []

    base_metadata = dict(metadata or {})
    chunks: list[TextChunk] = []
    start = 0
    index = 0

    while start < len(cleaned):
        end = min(len(cleaned), start + chunk_size)

        if end < len(cleaned):
            boundary = max(
                cleaned.rfind("\n", start, end),
                cleaned.rfind(". ", start, end),
                cleaned.rfind(" ", start, end),
            )
            if boundary > start + (chunk_size // 2):
                end = boundary + (1 if cleaned[boundary] == "." else 0)

        piece = cleaned[start:end].strip()
        if piece:
            chunks.append(
                TextChunk(
                    text=piece,
                    chunk_index=index,
                    metadata={**base_metadata, "chunk_index": index},
                )
            )
            index += 1

        if end >= len(cleaned):
            break
        start = max(0, end - overlap)

    return chunks


def extract_pdf_text(file_bytes: bytes) -> str:
    """Extract text from a PDF upload.

    PDF extraction is kept separate from the RAG pipeline so cloud storage and
    database code can call the same processing layer.
    """
    from io import BytesIO
    from pypdf import PdfReader

    reader = PdfReader(BytesIO(file_bytes))
    pages = [(page.extract_text() or "") for page in reader.pages]
    return "\n\n".join(pages).strip()
