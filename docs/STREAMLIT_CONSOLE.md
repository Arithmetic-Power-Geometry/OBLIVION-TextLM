# Streamlit console

The Streamlit console is a public-facing presentation layer for OBLIVION TextLM. It calls the same
FastAPI backend used by programmatic clients, so the inference-control implementation remains
centralized in `src/oblivion_textlm`.

## Features

- text question and context input
- TXT, Markdown, CSV, JSON, LOG, PDF, and DOCX upload
- final answer panel
- current live-obligation view
- per-step obligation birth and retirement trace
- verifier and KEEP/RETIRE decisions
- SHC-aware audit table
- optional raw JSON inspection for research demonstrations
- dark professional theme
- server-side API credential handling for public deployments

## Local run

```bash
pip install -r requirements-ui.txt
export OBLIVION_UI_API_BASE_URL=http://127.0.0.1:8080
export OBLIVION_UI_API_KEY=change-me
streamlit run app/streamlit_app.py
```

## Public deployment

Deploy the proprietary backend separately behind TLS. Configure the Streamlit host with these
server-side secrets:

```toml
OBLIVION_UI_API_BASE_URL = "https://api.example.com"
OBLIVION_UI_API_KEY = "strong-private-backend-key"
OBLIVION_UI_PUBLIC_MODE = "true"
```

Never embed the backend API key in client-side JavaScript or publish it in a repository. The
console intentionally reads credentials on the Streamlit server.

The current UI parses documents in memory and sends extracted text to the configured backend. A
production operator remains responsible for document-retention policy, malware scanning,
confidentiality controls, and infrastructure logs.

## Streamlit Community Cloud dependency note

Streamlit Community Cloud installs the repository-root `requirements.txt` for this app. The root requirements therefore intentionally include `streamlit`, `pypdf`, and `python-docx` in addition to backend dependencies. Do not remove those entries when deploying `app/streamlit_app.py` directly on Streamlit Community Cloud.
