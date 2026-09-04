# OBLIVION TextLM v1.0.0 — System Card

## System type

Text-based query-relative inference system composed from a pretrained language-model executor
and an OBLIVION semantic-obligation control plane. It is not a new pretrained foundation model.

## Intended use

Long-document question answering, enterprise knowledge retrieval, multi-hop text reasoning, and
controlled experiments comparing full-context inference with obligation-conditioned inference.

## Base executor

Default configuration name: `mistralai/Mistral-Small-4-119B-2603` served through an
OpenAI-compatible endpoint. No base-model weights are bundled.

## Outputs

The API returns an answer plus an `oblivion` object containing remaining obligations, per-stage
trace data, and cost audit fields. Trace exposure can be disabled for deployments where internal
control state should not be returned.

## Limitations

Generic learned obligation construction and verification can be wrong. The exact soundness
results in the source theories require their stated assumptions and do not automatically transfer
to an unconstrained natural-language verifier. Routing can cost more than it saves. Dynamic
selection can also harm batching and memory locality. End-to-end measurements are mandatory.

## Commercial acceptance criteria

A production release should be promoted as an efficiency improvement only when matched tests
with identical executor weights demonstrate acceptable task quality and lower total deployment
cost after routing, verification, transformation, and serving overhead are included.
