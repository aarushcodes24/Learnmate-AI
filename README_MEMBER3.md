# Member 3 contribution: Database + Files

This is an additive module for the AI Teaching Assistant group project. It provides a PostgreSQL connection pool, an additive SQL schema, migration runner, parameterized repository functions, a provider-neutral object-storage contract, and validation tests.

## Integration note

The team's existing database reportedly has tables named `Chat_History`, `Quiz_Questions`, `Quiz_Results`, `Quizzes`, `Students`, and `Study_Materials`. Because their exact definitions were not supplied here, this contribution uses `member3_`-prefixed tables to avoid altering or colliding with them. Before production integration, the team should map these new tables to the existing schema or agree to consolidate them in a reviewed migration.

## Requirements

Install from the project root:

```bash
pip install -r requirements-member3.txt
```

Set `DATABASE_URL` in your local environment. Copy `.env.member3.example` as a reference; do not commit real credentials. The example is not automatically loaded by Python.

## Apply schema

From project root, after placing these files under `app/member3_database/`:

```bash
python -m app.member3_database.migrate
```

## Tests

From project root:

```bash
pytest tests/member3_database -q
```

The included tests validate input checks and do not claim to test a live database. PostgreSQL integration tests should be added once the team's test database is available.

## Interfaces for teammates

- `get_pool()` / `close_pool()` — database connection pool lifecycle.
- `create_student(...)` and `create_course(...)` — persistence functions.
- `add_document_metadata(...)` and `list_documents_for_owner(...)` — document metadata persistence.
- `update_document_status(...)` — processing-state update.
- `ObjectStorage` protocol — contract for Member 2 or future cloud-storage adapter.

This module does not implement authentication, UI, RAG, PDF extraction, or cloud uploads. It exposes database support and a storage contract without duplicating those team responsibilities.
