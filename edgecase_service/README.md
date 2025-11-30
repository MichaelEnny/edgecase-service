## Edgecase Service

A small, intentionally imperfect Python codebase for testing how models handle underspecified or unclear coding tasks.

### High-level description

This project is a toy "task management" backend. It pretends to support:
- Creating and updating users
- Creating, updating, and listing tasks
- Basic permissions so users can only see their own tasks
- Soft-delete of tasks (according to this README)

The actual code is intentionally inconsistent with this description in a few places.

### Project layout

- `src/edgecase_service/` – core business logic
  - `config.py` – global settings (page size, feature flags, etc.)
  - `models.py` – simple data models
  - `repository.py` – in-memory "database"
  - `services/` – higher-level business operations
  - `api/http_handlers.py` – thin HTTP-style handlers (no real web framework)
  - `utils/` – logging and validation helpers
- `tests/` – a few unit tests that document some (but not all) expected behavior

### Known gaps (on purpose)

This codebase is **not** production-ready. It intentionally includes:
- Missing error handling in several places
- Inconsistent validation between user and task flows
- TODOs for features that are half-implemented
- Slightly conflicting expectations between README, code, and tests

Examples of things that might be turned into tricky evaluation tasks:
- "Add pagination to the list tasks endpoint"
- "Implement soft-delete like the README says"
- "Improve error handling around task creation"
- "Add logging to follow the existing pattern"

### Running tests

From the `edgecase_service` directory, you can run:

```bash
python -m unittest discover -s tests
```

Note: the tests and implementation are small and intentionally incomplete; not all behavior is covered.

