# Security policy

## Supported status

This repository is a learning-oriented local reference implementation. It is not currently presented as a production multi-user service.

## Never commit or publish

- `.env` or API keys
- `credentials.json`
- `token.json`
- Gmail messages or attachments
- Calendar event data
- Generated analysis or briefings containing personal data
- Scheduler logs containing personal data
- Screenshots exposing secrets, email subjects, events, usernames, or local paths

Recommended `.gitignore` coverage:

```gitignore
.env
.venv/
credentials.json
token.json
logs/
__pycache__/
*.pyc
.DS_Store
```

## Security design

- Use Gmail and Calendar read-only scopes.
- Keep OAuth and API credentials local.
- Mock integrations in automated tests.
- Keep the development dashboard bound to localhost.
- Review model-generated recommendations before acting.
- Minimise sensitive content sent to external model providers.

## Before making the repository public

```bash
git ls-files | grep -E '(^|/)(\.env|credentials\.json|token\.json)$'
git log --all -- .env credentials.json token.json
```

The first command should produce no output. Review the second carefully. If a secret was ever committed, removing the file in a later commit is insufficient: revoke or rotate the credential and clean the repository history before publication.

Enable GitHub secret scanning and push protection where available.

## Reporting a vulnerability

Do not open a public issue containing a vulnerability, personal data, credentials, or exploit details. Use GitHub's private vulnerability reporting feature if enabled, or contact the maintainer privately through a security contact published in the repository profile.

Include:

- affected version or commit;
- impact;
- reproduction steps using synthetic data;
- suggested mitigation, if known.

Never include real tokens or personal email/calendar content in a report.
