# Dashboard guide

Start the local server:

```bash
python -m uvicorn app.api:app --reload
```

## Views

| Route | Purpose |
| --- | --- |
| `/` | Latest executive overview |
| `/briefing` | Latest generated briefing |
| `/history` | List of stored runs |
| `/history/{run_id}` | Analysis and briefing for a specific run |
| `/usage` | Model usage information |
| `/system` | Integration and system status |
| `/docs` | FastAPI-generated API documentation |

The controller handles missing briefing data with an empty state. A historical detail page can display a run when either structured analysis or briefing text is present; it returns 404 only when neither exists.

## Local-use warning

The development server and current UI are not a production security boundary. Do not bind the server to a public interface or deploy it publicly without:

- user authentication and authorisation;
- HTTPS;
- secure secret management;
- CSRF and session review where applicable;
- rate limiting and access logging;
- data-retention controls;
- a deployment threat assessment.

## Adding screenshots to the repository

Capture the current dashboard only after removing or obscuring names, email subjects, appointments, file paths, API usage identifiers, and other personal information. Store sanitised images under `screenshots/`, then reference them from the main README.
