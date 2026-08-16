# Google Cloud and OAuth setup

Each user must create their own Google Cloud project and OAuth credentials. Never share the repository owner's credentials.

## 1. Create or select a Google Cloud project

Open the Google Cloud Console, create a project, and select it before enabling APIs. A descriptive name such as `Personal Executive AI` is suitable.

## 2. Enable APIs

In **APIs & Services → Library**, enable:

- Gmail API
- Google Calendar API

If an API page shows **Disable API**, it is already enabled.

## 3. Configure Google Auth Platform

Open **Google Auth Platform** and choose **Get started** if the project has not been configured.

Complete:

1. **Branding:** application name and support email.
2. **Audience:** select External for a personal Google account unless your Workspace policy requires Internal.
3. **Contact information:** provide a developer contact email.

For a personal/local project, keep the app in testing while developing.

## 4. Add a test user

If the OAuth app is External and in testing, add the Google account that the assistant will read as a test user. Authentication can fail with `access_denied` when this is omitted.

## 5. Configure data access

Use only these scopes:

```text
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/calendar.readonly
```

Do not select broad BigQuery, Cloud Platform, Gmail modify, or Calendar write scopes for this implementation. If the scope picker is difficult to navigate, use its filter or pasted-scopes field.

## 6. Create an OAuth client

Go to **Clients → Create client** and choose:

```text
Application type: Desktop app
```

Give the client a descriptive name, create it, and download the JSON file.

## 7. Store credentials locally

Rename the download to `credentials.json` if necessary and place it in the project root, or update `GOOGLE_CREDENTIALS_FILE` in `.env`.

```text
personal-executive-ai/
├── credentials.json   # local only; never commit
├── .env               # local only; never commit
└── app/
```

## 8. Complete first authentication

Run the repository's Google authentication module. In the refactored structure, this is expected to be:

```bash
python -m app.integrations.google_auth
```

An earlier project version used `python -m app.google_auth`; use the module that exists in your checkout.

The browser will ask you to choose the configured test-user account and approve the two read-only permissions. On success, a local `token.json` is created.

## 9. Verify safely

Confirm that both credential files are ignored:

```bash
git check-ignore credentials.json token.json
```

Do not print their contents in a terminal recording or attach them to an issue.

## OAuth troubleshooting

- **`Error 403: access_denied`:** add the account as a test user and verify the correct project is selected.
- **`redirect_uri_mismatch`:** recreate the client as a Desktop app; do not use a Web application client for this local flow.
- **API not enabled:** enable both APIs in the same project as the OAuth client.
- **Scope changes not reflected:** delete the local `token.json` and authenticate again after confirming the scope list. Do this only to your own local token.
- **App verification warning:** testing-mode apps used by their configured test users generally do not need public verification; broader public distribution may trigger Google's verification requirements.
