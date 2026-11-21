"""Parameterized repository functions for Member 3's additive schema."""
from __future__ import annotations
from typing import Any
from .connection import get_pool


def create_student(display_name: str, email: str | None = None,
                  external_user_id: str | None = None) -> dict[str, Any]:
    if not display_name.strip():
        raise ValueError("display_name cannot be empty")
    query = """INSERT INTO member3_students (display_name, email, external_user_id)
               VALUES (%s, %s, %s) RETURNING student_id, display_name, email, external_user_id, created_at"""
    with get_pool().connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (display_name.strip(), email, external_user_id))
            row = cur.fetchone()
        conn.commit()
    return dict(zip(("student_id", "display_name", "email", "external_user_id", "created_at"), row))


def create_course(owner_external_user_id: str, course_name: str,
                 description: str | None = None) -> dict[str, Any]:
    if not owner_external_user_id.strip() or not course_name.strip():
        raise ValueError("owner_external_user_id and course_name are required")
    query = """INSERT INTO member3_courses (owner_external_user_id, course_name, description)
               VALUES (%s, %s, %s) RETURNING course_id, owner_external_user_id, course_name, description, created_at"""
    with get_pool().connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (owner_external_user_id.strip(), course_name.strip(), description))
            row = cur.fetchone()
        conn.commit()
    return dict(zip(("course_id", "owner_external_user_id", "course_name", "description", "created_at"), row))


def add_document_metadata(*, owner_external_user_id: str, document_name: str,
                         document_type: str, storage_key: str,
                         course_id: int | None = None, subject: str | None = None,
                         unit_name: str | None = None, topic_name: str | None = None,
                         storage_provider: str = "external", mime_type: str | None = None,
                         file_size_bytes: int | None = None) -> dict[str, Any]:
    allowed = {"syllabus", "textbook", "notes", "reference", "other"}
    if document_type not in allowed:
        raise ValueError(f"document_type must be one of {sorted(allowed)}")
    if not owner_external_user_id.strip() or not document_name.strip() or not storage_key.strip():
        raise ValueError("owner, document_name, and storage_key are required")
    query = """INSERT INTO member3_documents
        (owner_external_user_id, course_id, subject, unit_name, topic_name, document_name,
         document_type, storage_provider, storage_key, mime_type, file_size_bytes)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING document_id, owner_external_user_id, course_id, document_name,
                  document_type, storage_provider, storage_key, processing_status, created_at"""
    values = (owner_external_user_id.strip(), course_id, subject, unit_name, topic_name,
              document_name.strip(), document_type, storage_provider, storage_key,
              mime_type, file_size_bytes)
    with get_pool().connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)
            row = cur.fetchone()
        conn.commit()
    keys = ("document_id", "owner_external_user_id", "course_id", "document_name",
            "document_type", "storage_provider", "storage_key", "processing_status", "created_at")
    return dict(zip(keys, row))


def list_documents_for_owner(owner_external_user_id: str) -> list[dict[str, Any]]:
    query = """SELECT document_id, course_id, document_name, document_type, subject,
                      unit_name, topic_name, storage_provider, storage_key,
                      processing_status, created_at
               FROM member3_documents WHERE owner_external_user_id = %s
               ORDER BY created_at DESC"""
    with get_pool().connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (owner_external_user_id,))
            rows = cur.fetchall()
    keys = ("document_id", "course_id", "document_name", "document_type", "subject",
            "unit_name", "topic_name", "storage_provider", "storage_key", "processing_status", "created_at")
    return [dict(zip(keys, row)) for row in rows]


def update_document_status(document_id: int, status: str) -> None:
    allowed = {"pending", "processing", "completed", "failed"}
    if status not in allowed:
        raise ValueError(f"status must be one of {sorted(allowed)}")
    query = "UPDATE member3_documents SET processing_status=%s, updated_at=NOW() WHERE document_id=%s"
    with get_pool().connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (status, document_id))
            if cur.rowcount != 1:
                raise LookupError(f"Document {document_id} not found")
        conn.commit()
