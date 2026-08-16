# Contributing

Thank you for considering a contribution.

## Development workflow

1. Fork the repository.
2. Create a focused branch.
3. Create and activate a Python 3.11 virtual environment.
4. Install `requirements.txt`.
5. Make the smallest coherent change.
6. Add or update tests.
7. Run `python -m pytest`.
8. Confirm that no credentials, personal data, or generated logs are staged.
9. Open a pull request with a clear explanation and verification evidence.

## Pull-request expectations

- Preserve read-only Google scopes unless a separately justified design change is reviewed.
- Keep provider-specific logic inside integrations.
- Keep application behaviour inside services.
- Use typed models for cross-layer contracts.
- Do not make tests call real external APIs by default.
- Update documentation when setup or behaviour changes.
- Use synthetic examples rather than real email or calendar data.

## Commit messages

Use short, descriptive messages, for example:

```text
Add history detail empty-state test
Document Google OAuth test-user setup
Fix dashboard usage view model
```

## Issues

Include the operating system, Python version, command run, expected behaviour, and sanitised error output. Remove tokens, message contents, email addresses, usernames, and local paths before posting.

## Code of conduct

Be respectful, constructive, and mindful that contributors have different levels of experience. Harassment, discrimination, and publication of another person's private information are not acceptable.
