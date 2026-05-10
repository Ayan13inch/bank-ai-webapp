# Bank AI Webapp

**One-line**: Upload bank statements, extract transactions, and chat with an AI assistant for categorization and suggestions.

## Features
- PDF and Excel statement parsing
- OCR fallback for scanned PDFs
- LLM-based transaction categorization and chat
- Deployable to Render via Docker

## Quickstart (local)
1. Clone repo: `git clone https://github.com/<your-username>/bank-ai-webapp.git`
2. Create venv: `python -m venv .venv && source .venv/bin/activate`
3. Install: `pip install -r requirements.txt`
4. Run: `export FLASK_APP=app/app.py && flask run --host=0.0.0.0 --port=5000`

## Deploy to Render
1. Push to GitHub.
2. Create a Web Service on Render and connect this repo.
3. Use Docker build; set `OPENAI_API_KEY` and other secrets in Render dashboard.
4. Enable auto deploy.

## Security and privacy
- Do not commit real statements or secrets.
- Use HTTPS and store any persisted files encrypted.
- Add authentication before using with real data.

## Contributing
- Run tests: `pytest`
- Lint: `flake8` or `ruff`
