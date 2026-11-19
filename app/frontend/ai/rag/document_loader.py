from pathlib import Path

from app.ai.rag.chunker import extract_pdf_text


def extract_text_from_upload(
    file_bytes: bytes,
    *,
    filename: str,
) -> str:
    """Convert a supported academic upload into plain text.

    The caller is responsible for validating permissions and persisting the
    original document. This module only handles extraction.
    """
    suffix = Path(filename).suffix.lower()

    if suffix == ".pdf":
        return extract_pdf_text(file_bytes)

    if suffix in {".txt", ".md"}:
        return file_bytes.decode("utf-8", errors="replace").strip()

    raise ValueError(
        f"Unsupported document type: {suffix or 'unknown'}. "
        "Currently supported: PDF, TXT and Markdown."
    )
