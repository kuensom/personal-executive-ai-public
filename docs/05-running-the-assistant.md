# Running the assistant

Activate the project environment before every command:

```bash
source .venv/bin/activate
```

## Preflight check

Confirm:

- dependencies are installed;
- `.env` contains a valid OpenAI key and model;
- `credentials.json` exists locally;
- Google OAuth has produced `token.json`;
- both Google APIs are enabled;
- tests pass.

## Run the complete workflow

At the documented checkpoint:

```bash
python -m app.scheduled_runner
```

The workflow should:

1. authenticate with Google;
2. retrieve the configured Gmail and Calendar window;
3. normalise records into domain models;
4. request structured analysis from OpenAI;
5. save analysis JSON and briefing text under the local log directory;
6. report completion without printing sensitive content unnecessarily.

## Inspect outputs

Generated filenames use a timestamp-based run identifier, for example:

```text
logs/analysis_2026-08-15_07-30-00.json
logs/briefing_2026-08-15_07-30-00.txt
```

These files can contain personal data. Keep the directory ignored and apply an appropriate retention policy.

## Start the dashboard

```bash
python -m uvicorn app.api:app --reload
```

Open <http://127.0.0.1:8000/>. The dashboard reads stored outputs; it does not need to rerun the external integrations on each page request.

## Stop the server

Press `Control+C` in the terminal running Uvicorn.
