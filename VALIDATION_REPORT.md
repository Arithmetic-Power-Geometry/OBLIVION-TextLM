# OBLIVION TextLM v1.1.1 — Validation Report

Validation date: 2026-09-03

## Release scope

This release is the professional proprietary OBLIVION TextLM package with the FastAPI backend,
CLI, deterministic offline validation path, deployment assets, theory/citation metadata, and a
public-facing Streamlit text console. Model weights are deliberately not bundled.

## Required architecture stages

| Stage | Release implementation | Status |
|---|---|---|
| 1. Pretrained executor | OpenAI-compatible `F_theta` executor interface | Complete |
| 2. Obligation constructor | `G_theta` structured control plane | Complete |
| 3. Obligation router | `Z(O_t)` obligation-conditioned router | Complete |
| 4. Text execution | executor prompt/evidence interface | Complete |
| 5. Obligation birth | `B_theta` birth transition | Complete |
| 6. Verification/discharge | certificate, three-way verifier, conservative KEEP | Complete |
| 7. Cost audit | local net-gain + SHC-style audit channels | Complete |
| 8. Professional deployment | FastAPI, auth/rate limit, metrics, Docker, CI, Streamlit | Complete as application package |

## Executed checks in this build environment

- Python compilation succeeded for `src`, `app`, `scripts`, and `tests`.
- Editable package installation succeeded with `--no-build-isolation --no-deps` using the
  dependencies already available in the build environment.
- Release metadata check passed.
- Full pytest regression suite: **18 passed**.
- Installed CLI entry point executed successfully.
- Deterministic OBLIVION demo returned **“Rahul's bicycle is red.”**, produced `VERIFIED →
  RETIRE`, and ended with zero live obligations.
- README, NOTICE, `CITATION.cff`, and `docs/REFERENCES.md` were mechanically checked for all
  four primary DOI records.
- Source, script, and app Python files were mechanically checked for the copyright header.
- Release text/code metadata were checked for unfinished-work and author-instruction markers.

## Streamlit validation boundary

The Streamlit application is syntactically compiled as part of the release checks. The current
build sandbox did not contain the `streamlit` wheel and could not reach the package index to
install it, so an actual Streamlit server startup was **not** executed in this sandbox. The GitHub
Actions workflow installs the `ui` dependency set, compiles the application, checks the
Streamlit executable, starts the console headlessly, and probes its health endpoint on a normal
networked CI runner. The UI dependency versions are pinned by
range in `requirements-ui.txt` and `pyproject.toml`.

## Commercial boundary

The release is suitable as a professional proprietary application package, but a production
operator must still provide and license the actual model-serving infrastructure, configure strong
production secrets, complete dependency/SBOM and vulnerability review, implement organization-
specific identity/tenant controls, and benchmark the deployed hardware before advertising an
inference-cost advantage.

Generic learned natural-language verification is an operational approximation and is not labeled
as theorem-level sound unless a deployment supplies a sound verifier for its domain. Text-level
active-context routing is implemented; arbitrary physical KV-cache eviction in third-party model
servers is not claimed by this release.
