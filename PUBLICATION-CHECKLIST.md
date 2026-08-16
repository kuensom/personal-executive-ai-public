# GitHub publication checklist

## Repository hygiene

- [ ] Confirm the repository URL and default branch.
- [ ] Confirm `.env`, `credentials.json`, `token.json`, and `logs/` are ignored.
- [ ] Confirm no secret is present anywhere in Git history.
- [ ] Rotate any credential that may have been exposed.
- [ ] Remove personal data from examples, tests, fixtures, and screenshots.
- [ ] Confirm `requirements.txt` installs in a fresh Python 3.11 environment.
- [ ] Confirm `python -m pytest` passes.

## Documentation

- [ ] Copy this bundle's `README.md` to the repository root.
- [ ] Copy the `docs/` directory to the repository root.
- [ ] Add `.env.example`, `SECURITY.md`, and `CONTRIBUTING.md`.
- [ ] Reconcile the existing `.gitignore` with `docs/recommended.gitignore`.
- [ ] Reconcile any commands marked as expected with the actual current modules.
- [ ] Replace the test-count statement if the suite has changed.
- [ ] Add sanitised screenshots of the current dashboard, not early setup errors.

## Open-source readiness

- [ ] Select and add a `LICENSE`.
- [ ] Enable Issues only if they will be monitored.
- [ ] Enable private vulnerability reporting where available.
- [ ] Enable secret scanning and push protection.
- [ ] Add a repository description and relevant topics.
- [ ] Copy `docs/github-actions-example.yml` to `.github/workflows/tests.yml` after verifying dependency installation.

## Release

- [ ] Commit the documentation on a branch.
- [ ] Review the rendered Markdown on GitHub.
- [ ] Merge into `main`.
- [ ] Tag a stable checkpoint, for example `v0.2.5`.
- [ ] Create a GitHub Release describing the single-agent workflow, dashboard, and test status.
- [ ] Change repository visibility only after all security checks are complete.
