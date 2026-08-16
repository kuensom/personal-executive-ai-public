# Troubleshooting

## `ModuleNotFoundError: No module named 'google'`

The Google packages are missing from the active environment, or a different Python interpreter is running.

```bash
source .venv/bin/activate
python -c "import sys; print(sys.executable)"
python -m pip install -r requirements.txt
python -m pip show google-auth
```

Use `python -m pip`, not an unqualified `pip`, so installation and execution use the same interpreter.

## `cryptography` wheel build fails on macOS

First upgrade packaging tools and retry:

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

Use a supported Python 3.11 installation and a fresh environment. If Conda `(base)` and `.venv` are both active, deactivate Conda and recreate the venv. Avoid pinning obsolete dependency versions that have no wheel for your Python/macOS combination.

## `NameError: get_message_details is not defined`

This indicates a code mismatch in an early Gmail-client version, not an OAuth problem. Update to the current repository version and confirm the helper is defined or imported before its call. Run the automated tests after updating.

## `ModuleNotFoundError: No module named 'app'` during pytest

Run tests from the repository root with:

```bash
python -m pytest
```

Keep tests in the top-level `tests/` directory rather than placing `test_*.py` inside `app/`. Confirm the `app` package contains `__init__.py` where required by the project structure.

## Google OAuth fails

- Confirm Gmail API and Calendar API are enabled in the selected project.
- Confirm the OAuth client type is Desktop app.
- Add the account as a test user.
- Confirm only the documented read-only scopes are configured.
- Confirm `credentials.json` belongs to the selected project.

## OpenAI request fails

- Confirm the API project has credit.
- Confirm the model is available to the API project.
- Confirm `.env` is loading.
- Never confuse a ChatGPT subscription with API billing.
- Rotate the key if it appeared in a terminal recording, screenshot, commit, or issue.

## Dashboard shows no briefing

Run the complete workflow once and check that the configured `LOG_DIR` contains a briefing file. Confirm the dashboard process uses the same working directory and environment configuration as the scheduled workflow.
