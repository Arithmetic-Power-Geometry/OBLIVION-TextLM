# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
required = [
    "README.md",
    "LICENSE",
    "NOTICE",
    "THIRD_PARTY_NOTICES.md",
    "CITATION.cff",
    "VERSION",
    "pyproject.toml",
    "app/streamlit_app.py",
    "src/oblivion_textlm/engine.py",
    "src/oblivion_textlm/baseline.py",
    "src/oblivion_textlm/rag.py",
    "src/oblivion_textlm/embeddings.py",
    "src/oblivion_textlm/vector_store.py",
    "src/oblivion_textlm/reranker.py",
    "src/oblivion_textlm/citations.py",
    "src/oblivion_textlm/memory.py",
    "src/oblivion_textlm/runtime/kv_manager.py",
    "src/oblivion_textlm/metrics/hardware.py",
    "src/oblivion_textlm/tools/registry.py",
    "benchmarks/data/sample.jsonl",
]

missing = [path for path in required if not (ROOT / path).exists()]
if missing:
    raise SystemExit("Missing release files: " + ", ".join(missing))

version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
if version != "2.0.0":
    raise SystemExit(f"Unexpected VERSION: {version}")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for doi in [
    "10.5281/zenodo.22172608",
    "10.5281/zenodo.22160359",
    "10.5281/zenodo.22162568",
    "10.5281/zenodo.22164419",
]:
    if doi not in readme:
        raise SystemExit(f"README missing DOI {doi}")

forbidden = ["TO" + "DO:", "FIX" + "ME:", "YOUR_" + "API_KEY_HERE"]
for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts:
        continue
    if path.suffix.lower() not in {".py", ".md", ".toml", ".yml", ".yaml", ".txt", ".cff"}:
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    for marker in forbidden:
        if marker in text:
            raise SystemExit(f"Release marker {marker!r} found in {path.relative_to(ROOT)}")

print("Release metadata check passed for OBLIVION TextLM v2.0.0.")
