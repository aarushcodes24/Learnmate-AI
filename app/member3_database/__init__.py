"""Member 3 database and document-metadata module for AI Teaching Assistant."""

from .connection import get_pool, close_pool

__all__ = ["get_pool", "close_pool"]
