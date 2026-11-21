"""Storage contract: metadata lives in PostgreSQL; bytes belong in object storage.

Member 2's document-processing/RAG code can use this interface later. This module
intentionally does not pretend to implement cloud uploads without credentials.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class StoredFile:
    provider: str
    key: str
    original_name: str
    mime_type: str | None = None
    size_bytes: int | None = None


class ObjectStorage(Protocol):
    """Provider-neutral interface to be implemented by cloud storage adapter."""
    def upload(self, *, object_key: str, content: bytes, content_type: str | None = None) -> StoredFile: ...
    def download(self, *, object_key: str) -> bytes: ...
    def delete(self, *, object_key: str) -> None: ...


class StorageNotConfiguredError(RuntimeError):
    """Raised when a cloud-storage adapter has not yet been configured."""


class UnconfiguredObjectStorage:
    """Safe adapter placeholder that clearly fails rather than storing fake files."""
    def upload(self, *, object_key: str, content: bytes, content_type: str | None = None) -> StoredFile:
        raise StorageNotConfiguredError("Configure an object-storage provider before uploading files.")
    def download(self, *, object_key: str) -> bytes:
        raise StorageNotConfiguredError("Configure an object-storage provider before downloading files.")
    def delete(self, *, object_key: str) -> None:
        raise StorageNotConfiguredError("Configure an object-storage provider before deleting files.")
