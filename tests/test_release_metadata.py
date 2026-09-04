from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOIS = [
    "10.5281/zenodo.22172608",
    "10.5281/zenodo.22160359",
    "10.5281/zenodo.22162568",
    "10.5281/zenodo.22164419",
]


def test_release_version_is_synchronized():
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    assert f'version = "{version}"' in (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert f'__version__ = "{version}"' in (ROOT / "src/oblivion_textlm/__init__.py").read_text(
        encoding="utf-8"
    )


def test_primary_citations_are_present_in_release_metadata():
    for rel in ["README.md", "NOTICE", "CITATION.cff", "docs/REFERENCES.md"]:
        text = (ROOT / rel).read_text(encoding="utf-8")
        for doi in DOIS:
            assert doi in text, (rel, doi)


def test_streamlit_release_surface_exists():
    for rel in [
        "app/streamlit_app.py",
        "requirements-ui.txt",
        "Dockerfile.streamlit",
        ".streamlit/config.toml",
        ".streamlit/secrets.toml.example",
        "docs/STREAMLIT_CONSOLE.md",
    ]:
        assert (ROOT / rel).is_file(), rel
