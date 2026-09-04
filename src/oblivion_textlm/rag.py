# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

import time

from .citations import build_citations
from .types import CostAudit, InferenceResult, Obligation, RunMode
from .util import approx_tokens


class RAGTextLM:
    """Same executor + retrieval, but no OBLIVION lifecycle."""

    def __init__(self, executor, router):
        self.executor = executor
        self.router = router

    async def infer(self, query: str, chunks, *, history=None) -> InferenceResult:
        pseudo = [Obligation(id="rag-query", text=query)]
        started = time.perf_counter()
        selected, routing_ms = self.router.route(query, pseudo, chunks)
        result = await self.executor.run(query, selected, [], "", history=history or [])
        total_ms = (time.perf_counter() - started) * 1000.0
        audit = CostAudit(
            routing=routing_ms,
            active_work=result.input_tokens
            or approx_tokens(" ".join(chunk.text for chunk in selected)),
            routing_ms=routing_ms,
            executor_ms=result.latency_ms,
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
            active_chars=sum(len(chunk.text) for chunk in selected),
            total_ms=total_ms,
        )
        return InferenceResult(
            answer=result.text,
            obligations=[],
            trace=[],
            audit=audit,
            citations=build_citations(selected, result.evidence_ids),
            mode=RunMode.RAG.value,
        )
