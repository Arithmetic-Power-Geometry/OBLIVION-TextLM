# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

import time

from .citations import build_citations
from .types import CostAudit, InferenceResult, RunMode
from .util import approx_tokens


class BaselineTextLM:
    """Same executor, no OBLIVION and no retrieval: full supplied context."""

    def __init__(self, executor):
        self.executor = executor

    async def infer(self, query: str, chunks, *, history=None) -> InferenceResult:
        started = time.perf_counter()
        result = await self.executor.run(query, chunks, [], "", history=history or [])
        total_ms = (time.perf_counter() - started) * 1000.0
        audit = CostAudit(
            active_work=result.input_tokens or approx_tokens(" ".join(c.text for c in chunks)),
            executor_ms=result.latency_ms,
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
            active_chars=sum(len(c.text) for c in chunks),
            total_ms=total_ms,
        )
        return InferenceResult(
            answer=result.text,
            obligations=[],
            trace=[],
            audit=audit,
            citations=build_citations(chunks, result.evidence_ids),
            mode=RunMode.BASELINE.value,
        )
