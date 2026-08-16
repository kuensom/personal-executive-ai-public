# Testing and verification

## Run the complete suite

From the repository root:

```bash
python -m pytest
```

Use `python -m pytest` rather than a bare `pytest` command. This ensures the test runner uses the active environment and includes the repository root on Python's import path.

The documented checkpoint reports:

```text
23 passed
```

## Run a focused test file

```bash
python -m pytest tests/test_dashboard_controller.py -v
```

## Test strategy

- Domain-model tests validate data contracts.
- Service tests validate transformation and retrieval behaviour.
- Integration boundaries are mocked to avoid real Gmail, Calendar, and OpenAI calls.
- Controller tests use FastAPI's test client.
- Dashboard tests cover normal and empty states.
- History tests cover successful detail retrieval and missing-run 404 behaviour.

## Test isolation

Automated tests should never require the maintainer's:

- `.env`;
- `credentials.json`;
- `token.json`;
- real Gmail or Calendar data;
- billable OpenAI requests.

Use fixtures, temporary directories, and mocks. A contributor should be able to run the default suite safely after installing dependencies.

## Before a pull request

```bash
python -m pytest
git status
```

Confirm that no generated logs or credential files appear in the change set.
