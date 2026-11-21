"""Small PostgreSQL connection-pool helper (psycopg 3)."""
from __future__ import annotations


from psycopg_pool import ConnectionPool
from .config import database_url

_pool: ConnectionPool | None = None


def get_pool() -> ConnectionPool:
    """Get or lazily create the shared pool."""
    global _pool
    if _pool is None:
        _pool = ConnectionPool(conninfo=database_url(), min_size=1, max_size=5, open=True)
    return _pool


def close_pool() -> None:
    """Close the pool at application shutdown, if it was created."""
    global _pool
    if _pool is not None:
        _pool.close()
        _pool = None
