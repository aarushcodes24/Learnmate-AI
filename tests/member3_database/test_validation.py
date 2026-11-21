"""Small unit tests for input validation; DB integration tests require PostgreSQL."""
import pytest
from app.member3_database.repositories import create_student, create_course, add_document_metadata, update_document_status


def test_student_requires_name():
    with pytest.raises(ValueError):
        create_student("   ")


def test_course_requires_owner_and_name():
    with pytest.raises(ValueError):
        create_course("", "Course")
    with pytest.raises(ValueError):
        create_course("owner", "  ")


def test_document_type_validation():
    with pytest.raises(ValueError):
        add_document_metadata(owner_external_user_id="u1", document_name="Notes",
                            document_type="bad_type", storage_key="key")


def test_document_metadata_required_fields():
    with pytest.raises(ValueError):
        add_document_metadata(owner_external_user_id="", document_name="Notes",
                            document_type="notes", storage_key="key")


def test_status_validation():
    with pytest.raises(ValueError):
        update_document_status(1, "invalid")
