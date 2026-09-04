# GitHub release profile

Repository name: `OBLIVION-TextLM`

Recommended visibility for the proprietary release: **Private**.

Release tag: `v1.0.0`

Primary commands:

```bash
python -m pip install -e ".[dev]"
pytest
oblivion-textlm demo
uvicorn oblivion_textlm.api:app --host 0.0.0.0 --port 8080
```

Container deployment:

```bash
cp .env.example .env
docker compose up --build -d
```

The base model is intentionally external to the repository. In production, configure the executor
URL to the OpenAI-compatible endpoint serving the selected licensed model. The default model
identifier is `mistralai/Mistral-Small-4-119B-2603`.

This proprietary product repository is distinct from the existing Apache-2.0 OBLIVION research
companion repository cited by the manuscript. Keeping the repositories distinct avoids changing
the licensing representation made by the research paper.
