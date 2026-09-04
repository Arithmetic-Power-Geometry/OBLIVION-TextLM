# OBLIVION TextLM v2 Architecture

OBLIVION TextLM separates the pretrained neural executor from a proprietary
query-relative control plane. The executor supplies language competence. The
OBLIVION layer supplies explicit obligation state and retirement semantics.

## Modes

| Mode | Executor | Retrieval | OBLIVION lifecycle |
|---|---|---|---|
| Baseline | same | full context | no |
| RAG | same | hybrid router | no |
| OBLIVION | same | hybrid obligation router | yes |

## OBLIVION lifecycle

`G_theta -> O_t -> Z(O_t) -> F_theta -> B_theta -> P_theta -> V_Q -> D_t`

`O_(t+1) = (O_t ∪ B_t) \ D_t`

The implementation applies `UNCERTAIN -> KEEP` and requires positive audited
retirement gain before discharge.

## SHC audit

Operational cost is exposed rather than hidden in routing or verification:
encoding (E), realizability (R), separation/certification (S), transformation (T),
routing and active work are independently recorded.

## KV-cache boundary

`runtime/kv_manager.py` provides obligation-to-cache ownership accounting and
identifies blocks eligible for eviction. Actual physical eviction requires a serving
engine exposing the necessary hooks; it is not simulated as a proven hardware saving.
