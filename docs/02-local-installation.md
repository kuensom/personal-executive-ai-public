# Local installation

These steps target macOS and Linux. Windows users can use the equivalent PowerShell activation command.

## 1. Clone the repository

```bash
git clone https://github.com/kuensom/personal-executive-ai.git
cd personal-executive-ai
```

## 2. Confirm Python

The project was developed with Python 3.11.5. Use Python 3.11 for the most reproducible result.

```bash
python3.11 --version
```

## 3. Create an isolated environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -c "import sys; print(sys.executable)"
```

The printed path should end in `.venv/bin/python`. Seeing both `(.venv)` and `(base)` in a prompt may mean Conda is also active. That can create confusing dependency resolution. Prefer deactivating Conda before creating or using this environment:

```bash
conda deactivate
```

## 4. Upgrade packaging tools

```bash
python -m pip install --upgrade pip setuptools wheel
```

This step is important on macOS because outdated packaging tools may try to compile dependencies such as `cryptography` unnecessarily.

## 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

Verify key imports:

```bash
python -c "import fastapi, google.auth, openai, pydantic; print('Core imports OK')"
```

## 6. Configure local environment

```bash
cp .env.example .env
```

Edit `.env` locally. Never paste API keys into documentation, source code, screenshots, issues, or commits.

## 7. Configure Google OAuth

Follow [03-google-cloud-oauth.md](03-google-cloud-oauth.md). Place the downloaded desktop OAuth file at the path configured by `GOOGLE_CREDENTIALS_FILE`, normally `credentials.json` in the project root.

## 8. Configure OpenAI

Follow [04-openai-setup.md](04-openai-setup.md), then set `OPENAI_API_KEY` and `OPENAI_MODEL` in `.env`.

## 9. Confirm ignored files

```bash
git check-ignore .env credentials.json token.json logs/
git ls-files | grep -E '(^|/)(\.env|credentials\.json|token\.json)$'
```

The first command should identify the sensitive paths as ignored. The second should produce no output.

## 10. Run tests

```bash
python -m pytest
```

The documented checkpoint reports 23 passing tests.

## 11. Run locally

```bash
python -m app.scheduled_runner
python -m uvicorn app.api:app --reload
```

If the repository has renamed an entry point, inspect `app/` and use the current module documented in its source. Open <http://127.0.0.1:8000/> after the server starts.
