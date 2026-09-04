# Theory alignment

OBLIVION TextLM implements the four-paper chain without collapsing the frameworks into one.

## Task-Semantic Images (TSI)

TSI asks what values a task-specific semantic map can expose. Its central warning is operationally
important: a small task-semantic image does not imply cheap realizability or cheap composition.
OBLIVION TextLM therefore uses task-conditioned routing as an engineering approximation to a
live task-visible representation but does not label lexical retrieval itself as an exact TSI.

Reference: Akhtar, M. A. K. (2026), *Beyond Complete Compilation: Task-Semantic Images and
the Complexity of Computing Only What a Query Can See*, Version V1,
https://doi.org/10.5281/zenodo.22160359.

## Semantic Lifetime Width (SLW)

SLW asks how long distinctions must remain separable with respect to future terminal behavior.
Its retirement calculus is certificate based. The implementation preserves the conservative
asymmetry: failed or uncertain verification yields `KEEP`. Exact SLW soundness claims are made
only when a deployment supplies a sound domain-specific verifier; generic learned verification is
an operational approximation.

Reference: Akhtar, M. A. K. (2026), *When Can a Computation Forget? Semantic Lifetime Width
and Query-Relative State Retirement*, Version V1,
https://doi.org/10.5281/zenodo.22162568.

## Semantic Hardness Conservation (SHC)

SHC separates encoding, realizability, separation/certification, and transformation. The software
records these as explicit audit channels and keeps wall-clock, token counts, routing, and executor
latency separate. A lower active-token count is never automatically labeled a computational win.

Reference: Akhtar, M. A. K. (2026), *Semantic Hardness Conservation: An Operational Normal
Form for Exact Reasoning After Compression*, Version V1,
https://doi.org/10.5281/zenodo.22164419.

## OBLIVION

OBLIVION supplies the adaptive state machine: unresolved obligation state `O_t`, birth set `B_t`,
discharge set `D_t`, and the update

`O_{t+1} = (O_t union B_t) minus D_t`.

The implementation follows the ordering: construct, route, execute, birth, certify, verify, audit,
discharge, update, repeat. `UNCERTAIN` is not treated as permission to delete state, and a
semantically accepted retirement still requires positive audited gain in the configured local cost
model.

Reference: Akhtar, M. A. K. (2026), *OBLIVION: Query-Relative Neural Computation by Verified
Semantic Obligation Retirement*, Version V1,
https://doi.org/10.5281/zenodo.22172608.

## Deliberate non-claims

The package does not claim that relevance, pruning, future equivalence, compression, retrieval,
or dynamic memory were invented by OBLIVION. It does not claim universal Transformer
superiority. It does not equate learned natural-language verification with theorem-level soundness.
Commercial value must be established by paired end-to-end benchmarks using the same executor
weights and by charging controller overhead.
