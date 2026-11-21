"""Run the additive Member 3 SQL schema against the configured PostgreSQL DB."""
from pathlib import Path
from .connection import get_pool

SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def apply_schema() -> None:
    sql = SCHEMA_PATH.read_text(encoding="utf-8")
    with get_pool().connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()


if __name__ == "__main__":
    apply_schema()
    print("Member 3 database schema applied.")
