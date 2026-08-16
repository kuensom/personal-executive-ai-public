# Scheduling

Test the complete workflow manually before scheduling it. A scheduler should call the virtual environment's Python executable rather than relying on whichever Python happens to be on the system path.

## macOS with `launchd`

Create a user LaunchAgent property list that runs the project module at the desired time. Use absolute paths for:

- the project directory;
- `.venv/bin/python`;
- the output and error log files.

The program arguments should be conceptually equivalent to:

```text
/absolute/path/personal-executive-ai/.venv/bin/python
-m
app.scheduled_runner
```

Set the working directory to the repository root so relative configuration paths resolve correctly.

Do not commit a personal LaunchAgent file containing your username or local filesystem paths. If the repository supplies a template, replace placeholders locally.

## Linux with cron

Example for a daily 7:00 AM run:

```cron
0 7 * * * cd /absolute/path/personal-executive-ai && .venv/bin/python -m app.scheduled_runner >> logs/scheduler.log 2>&1
```

Environment variables may not be the same in cron as in an interactive shell. Ensure the application loads `.env` from the project directory.

## Operational guidance

- Avoid overlapping runs.
- Keep scheduler logs free of email bodies, tokens, and API keys.
- Review failures regularly.
- Apply log rotation or retention.
- Re-authenticate Google OAuth when required.
- Disable scheduling before moving or deleting the project environment.
