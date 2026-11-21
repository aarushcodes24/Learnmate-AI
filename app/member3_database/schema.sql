-- Member 3 additive schema. All tables use the member3_ prefix to avoid
-- collisions with the team's existing tables. PostgreSQL 14+ compatible.

CREATE TABLE IF NOT EXISTS member3_students (
    student_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    external_user_id TEXT UNIQUE,
    display_name TEXT NOT NULL,
    email TEXT UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS member3_courses (
    course_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    owner_external_user_id TEXT NOT NULL,
    course_name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS member3_enrollments (
    enrollment_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    course_id BIGINT NOT NULL REFERENCES member3_courses(course_id) ON DELETE CASCADE,
    student_id BIGINT NOT NULL REFERENCES member3_students(student_id) ON DELETE CASCADE,
    enrolled_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(course_id, student_id)
);

CREATE TABLE IF NOT EXISTS member3_documents (
    document_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    owner_external_user_id TEXT NOT NULL,
    course_id BIGINT REFERENCES member3_courses(course_id) ON DELETE CASCADE,
    subject TEXT,
    unit_name TEXT,
    topic_name TEXT,
    document_name TEXT NOT NULL,
    document_type TEXT NOT NULL CHECK (document_type IN ('syllabus','textbook','notes','reference','other')),
    storage_provider TEXT NOT NULL DEFAULT 'external',
    storage_key TEXT NOT NULL,
    mime_type TEXT,
    file_size_bytes BIGINT CHECK (file_size_bytes IS NULL OR file_size_bytes >= 0),
    processing_status TEXT NOT NULL DEFAULT 'pending'
        CHECK (processing_status IN ('pending','processing','completed','failed')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(storage_provider, storage_key)
);

CREATE TABLE IF NOT EXISTS member3_document_chunks (
    chunk_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    document_id BIGINT NOT NULL REFERENCES member3_documents(document_id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL CHECK (chunk_index >= 0),
    content TEXT NOT NULL,
    page_number INTEGER CHECK (page_number IS NULL OR page_number > 0),
    topic_name TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(document_id, chunk_index)
);

CREATE INDEX IF NOT EXISTS idx_member3_courses_owner ON member3_courses(owner_external_user_id);
CREATE INDEX IF NOT EXISTS idx_member3_enrollments_student ON member3_enrollments(student_id);
CREATE INDEX IF NOT EXISTS idx_member3_documents_owner ON member3_documents(owner_external_user_id);
CREATE INDEX IF NOT EXISTS idx_member3_documents_course ON member3_documents(course_id);
CREATE INDEX IF NOT EXISTS idx_member3_documents_status ON member3_documents(processing_status);
CREATE INDEX IF NOT EXISTS idx_member3_chunks_document ON member3_document_chunks(document_id, chunk_index);
