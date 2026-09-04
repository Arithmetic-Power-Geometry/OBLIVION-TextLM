# OBLIVION TextLM v2.0.0

**OBLIVION TextLM** is a proprietary query-relative TextLM system powered by the
OBLIVION inference-control architecture and a separately licensed pretrained
language-model executor. The reference production profile targets an
OpenAI-compatible deployment of **Mistral Small 4
(`mistralai/Mistral-Small-4-119B-2603`)**, but the executor is replaceable.

OBLIVION TextLM is **not** presented as a foundation model trained from scratch.
The pretrained executor supplies tokenizer/model knowledge and neural language
generation. OBLIVION supplies the query-relative control plane: explicit unresolved
semantic obligations, task-relative routing, obligation birth, evidence-bound
certification, conservative verification, semantic retirement, and SHC-aware
operational accounting.

**Copyright © 2026 Mohammad Amir Khusru Akhtar. All rights reserved.**

## Complete v2 architecture

```text
Input / chat / document
        │
        ├── parsing + chunk metadata
        ├── conversation memory
        ├── safety / prompt-injection signals
        │
        ▼
  G_theta: obligation construction
        │
        ▼
    O_t: live obligations
        │
        ▼
  Z(O_t): hybrid retrieval
    ├── lexical score
    ├── deterministic semantic embedding
    └── reranking
        │
        ▼
  F_theta: pretrained LLM executor
        │
        ├── B_theta obligation birth
        ├── P_theta completion certificate
        └── V_Q independent/conservative verifier
                    │
         UNCERTAIN ─┴─ KEEP
                    │
                VERIFIED
                    │
              SHC cost audit
                    │
            positive net gain?
              │             │
             no            yes
              │             │
             KEEP        RETIRE D_t
                            │
                            ▼
                 O_(t+1)=(O_t∪B_t)\D_t
                            │
                            └── repeat
```

## What v2.0.0 adds

- real OpenAI-compatible pretrained LLM execution path, with Mistral Small 4 as the default model identifier;
- portable tokenizer accounting plus provider-reported exact usage when available;
- semantic embedding abstraction and dependency-free hashing embedder;
- persistent vector store;
- hybrid lexical + semantic obligation router;
- deterministic reranker;
- source/page/section chunk metadata and user-visible citations;
- persistent multi-turn conversation memory;
- system/user/assistant conversational prompting;
- streaming-capable OpenAI-compatible client;
- verifier-specific model configuration;
- stronger counterfactual text delta;
- advisory obligation-aware KV-cache ownership/eviction interface;
- inference scheduler and token-budget batching utilities;
- process/GPU hardware profiler with optional `nvidia-smi` sampling;
- detailed per-stage trace timing;
- three fair comparison modes: **BASELINE**, **RAG**, **OBLIVION**;
- benchmark runner with EM, token-F1, latency, audit, citations and timings;
- bootstrap statistical analysis;
- tool registry with calculator, read-only SQLite and connector-neutral web search;
- safety/input-limit and prompt-injection signal modules;
- persistent document storage;
- usage ledger and configurable token-cost estimator;
- provider abstraction and health probing;
- upgraded Streamlit comparison console;
- expanded CI and tests.

## Important measurement boundary

Text-level semantic retirement is implemented. The included KV manager is an
**advisory interface**; this repository does not falsely claim transparent eviction
of arbitrary internal KV blocks from every third-party model server. Real GPU/KV
savings must be measured on a serving engine that exposes the necessary hooks.

Likewise, the built-in hashing embedder is a dependency-free production-safe baseline,
not a claim of state-of-the-art semantic embedding quality. Deployments may substitute
a separately licensed embedding model.

## Quick start: offline smoke test

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,ui]"
pytest
oblivion-textlm demo --mode oblivion
streamlit run app/streamlit_app.py
```

The offline demo uses `DeterministicDemoExecutor`; it is a smoke test, not a
general-purpose LLM.

## Production executor

Configure `.env`:

```dotenv
OBLIVION_MODEL_NAME=mistralai/Mistral-Small-4-119B-2603
OBLIVION_EXECUTOR_BASE_URL=https://YOUR_OPENAI_COMPATIBLE_SERVER/v1
OBLIVION_EXECUTOR_API_KEY=YOUR_SERVER_KEY

# Optional cheaper controller / independent verifier:
OBLIVION_CONTROLLER_BASE_URL=
OBLIVION_CONTROLLER_API_KEY=
OBLIVION_CONTROLLER_MODEL=
OBLIVION_VERIFIER_BASE_URL=
OBLIVION_VERIFIER_API_KEY=
OBLIVION_VERIFIER_MODEL=

OBLIVION_ROUTER_MODE=hybrid
OBLIVION_API_KEYS=CHANGE_THIS
```

Start:

```bash
uvicorn oblivion_textlm.api:app --host 0.0.0.0 --port 8080
```

## Fair comparison API

The same `/v1/oblivion/query` endpoint accepts:

- `mode="baseline"` — same pretrained executor, full supplied context;
- `mode="rag"` — same executor + retrieval, no obligation lifecycle;
- `mode="oblivion"` — same executor + retrieval + OBLIVION lifecycle.

This isolates the effect of OBLIVION from the quality of the underlying LLM.

## Benchmark

```bash
python scripts/benchmark.py benchmarks/data/sample.jsonl results.jsonl \
  --url http://127.0.0.1:8080 --key CHANGE_THIS \
  --modes baseline,rag,oblivion --repeats 3

python scripts/analyze_benchmarks.py results.jsonl
```

Reported benchmark metrics include exact match, token F1, end-to-end latency,
provider token usage, OBLIVION audit channels, citations and per-stage timings.
Do not publish performance percentages until they have been measured with a real
executor under matched conditions.

## Theory and citation

OBLIVION TextLM follows the scoped architecture and novelty boundary of the
associated papers:

1. Akhtar, M. A. K. (2026). *OBLIVION: Query-Relative Neural Computation by
   Verified Semantic Obligation Retirement* (Version V1). Zenodo.
   https://doi.org/10.5281/zenodo.22172608
2. Akhtar, M. A. K. (2026). *Beyond Complete Compilation: Task-Semantic Images and
   the Complexity of Computing Only What a Query Can See* (Version V1). Zenodo.
   https://doi.org/10.5281/zenodo.22160359
3. Akhtar, M. A. K. (2026). *When Can a Computation Forget? Semantic Lifetime Width
   and Query-Relative State Retirement* (Version V1). Zenodo.
   https://doi.org/10.5281/zenodo.22162568
4. Akhtar, M. A. K. (2026). *Semantic Hardness Conservation: An Operational Normal
   Form for Exact Reasoning After Compression* (Version V1). Zenodo.
   https://doi.org/10.5281/zenodo.22164419

OBLIVION's paper explicitly frames the system as a birth–work–verify–discharge
process with live obligation state `O_t`, birth set `B_t`, discharge set `D_t`,
and the update `O_(t+1)=(O_t ∪ B_t)\D_t`, with retirement additionally subject to
a positive net-compute audit.

## Proprietary product boundary

The original OBLIVION TextLM product code, prompts, schemas, documentation and UI
in this repository are proprietary under the included `LICENSE`. Third-party
models, libraries, adapters, datasets and serving engines retain their own licenses.
No Mistral weights or other foundation-model weights are redistributed here.

Before commercial deployment, audit the exact license/version of every model,
embedding model, quantization, dataset and dependency actually deployed.

## Repository map

- `src/oblivion_textlm/` — product and OBLIVION control plane
- `src/oblivion_textlm/runtime/` — KV accounting, batching, scheduler
- `src/oblivion_textlm/metrics/` — hardware instrumentation
- `src/oblivion_textlm/providers/` — executor/provider abstraction
- `src/oblivion_textlm/storage/` — persistent document store
- `src/oblivion_textlm/tools/` — tool registry/connectors
- `app/` — Streamlit console
- `scripts/` — benchmark, release and smoke-test tools
- `benchmarks/data/` — small reproducibility inputs
- `tests/` — unit/integration tests
- `docs/` — architecture, deployment, security, theory and release documentation
