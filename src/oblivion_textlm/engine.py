# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

import time
from dataclasses import asdict

from .audit import CostModel, add_audit
from .citations import build_citations
from .counterfactual import text_delta
from .metrics.hardware import HardwareProfiler
from .tracing import TraceRecorder
from .types import (
    CostAudit,
    Decision,
    InferenceResult,
    Obligation,
    RetirementRecord,
    RunMode,
    StepTrace,
    Verdict,
)
from .util import approx_tokens


class OblivionTextLM:
    """OBLIVION query-relative inference-control engine."""

    def __init__(
        self,
        executor,
        control,
        router,
        cost_model: CostModel,
        *,
        max_steps: int = 6,
        counterfactual_enabled: bool = False,
        counterfactual_tolerance: float = 0.08,
        trace_enabled: bool = True,
        memory=None,
    ):
        self.executor = executor
        self.control = control
        self.router = router
        self.cost_model = cost_model
        self.max_steps = max_steps
        self.counterfactual_enabled = counterfactual_enabled
        self.counterfactual_tolerance = counterfactual_tolerance
        self.trace_enabled = trace_enabled
        self.memory = memory

    async def infer(
        self,
        query: str,
        chunks,
        *,
        session_id: str | None = None,
        history: list[dict] | None = None,
    ) -> InferenceResult:
        recorder = TraceRecorder()
        profiler = HardwareProfiler()
        profiler.start()
        started_total = time.perf_counter()

        if history is None and session_id and self.memory:
            history = self.memory.history(session_id)
        history = history or []

        with recorder.stage("obligation_construction", step=0):
            obligations = await self.control.construct(query, chunks)

        trace: list[StepTrace] = []
        total = CostAudit()
        prior = ""
        answer = ""
        evidence_ids: list[str] = []

        for step in range(self.max_steps):
            if not obligations:
                break

            before = [asdict(obligation) for obligation in obligations]
            step_timings_start = len(recorder.timings)

            with recorder.stage("routing", step=step):
                active, routing_ms = self.router.route(query, obligations, chunks)

            with recorder.stage("executor", step=step):
                result = await self.executor.run(
                    query,
                    active,
                    obligations,
                    prior,
                    history=history,
                )
            answer = result.text or answer
            evidence_ids.extend(result.evidence_ids)

            with recorder.stage("obligation_birth", step=step):
                births = await self.control.births(
                    query,
                    obligations,
                    result.text,
                    active,
                    step + 1,
                )

            candidates = self._dedupe(obligations + births)
            records: list[RetirementRecord] = []
            discharge_ids: set[str] = set()
            verification_ms = 0.0

            for obligation in candidates:
                verify_started = time.perf_counter()
                with recorder.stage("certificate_and_verification", step=step):
                    certificate = await self.control.certificate(
                        query,
                        obligation,
                        result.text,
                        active,
                    )
                    verdict = await self.control.verify(
                        query,
                        obligation,
                        certificate,
                        result.text,
                        active,
                    )
                verify_ms = (time.perf_counter() - verify_started) * 1000.0
                verification_ms += verify_ms

                delta = None
                decision = Decision.KEEP
                reason = "verification did not establish safe retirement"
                active_tokens = result.input_tokens or approx_tokens(
                    " ".join(chunk.text for chunk in active)
                )
                projected_saved_tokens = active_tokens / max(1, len(candidates))
                gain = self.cost_model.retirement_gain(projected_saved_tokens, verify_ms)

                if verdict == Verdict.VERIFIED:
                    if self.counterfactual_enabled:
                        without = [item for item in candidates if item.id != obligation.id]
                        alt_active, _ = self.router.route(query, without, chunks)
                        alt = await self.executor.run(
                            query,
                            alt_active,
                            without,
                            prior,
                            history=history,
                        )
                        delta = text_delta(result.text, alt.text)
                        if delta > self.counterfactual_tolerance:
                            reason = "counterfactual change exceeded tolerance"
                        elif gain > 0:
                            decision = Decision.RETIRE
                            reason = (
                                "verified, counterfactually tolerated, and positive audited gain"
                            )
                    elif gain > 0:
                        decision = Decision.RETIRE
                        reason = "verified and positive audited gain"
                    else:
                        reason = "semantically verified but audited gain was nonpositive"

                if decision == Decision.RETIRE:
                    discharge_ids.add(obligation.id)

                records.append(
                    RetirementRecord(
                        obligation.id,
                        verdict,
                        decision,
                        gain,
                        delta,
                        reason,
                    )
                )

            obligations = [
                obligation for obligation in candidates if obligation.id not in discharge_ids
            ]

            stage_audit = self.cost_model.stage(
                routing_ms=routing_ms,
                verification_ms=verification_ms,
                executor_ms=result.latency_ms,
                input_tokens=result.input_tokens
                or approx_tokens(" ".join(chunk.text for chunk in active)),
                output_tokens=result.output_tokens or approx_tokens(result.text),
                active_chars=sum(len(chunk.text) for chunk in active),
                ttft_ms=result.ttft_ms,
            )
            add_audit(total, stage_audit)

            if self.trace_enabled:
                trace.append(
                    StepTrace(
                        step=step,
                        obligations_before=before,
                        active_chunk_ids=[chunk.id for chunk in active],
                        executor_text=result.text,
                        births=[asdict(birth) for birth in births],
                        retirements=[asdict(record) for record in records],
                        obligations_after=[asdict(obligation) for obligation in obligations],
                        audit=asdict(stage_audit),
                        timings=[
                            asdict(timing) for timing in recorder.timings[step_timings_start:]
                        ],
                    )
                )

            prior = result.text

        hardware = profiler.stop()
        total.total_ms = (time.perf_counter() - started_total) * 1000.0
        total.peak_memory_mb = hardware.max_rss_mb
        if total.output_tokens > 0 and total.executor_ms > 0:
            # Provider-specific TTFT remains separate; this is completion throughput.
            pass

        citations = build_citations(chunks, list(dict.fromkeys(evidence_ids)))

        if session_id and self.memory:
            self.memory.append(session_id, "user", query)
            self.memory.append(session_id, "assistant", answer)

        return InferenceResult(
            answer=answer,
            obligations=obligations,
            trace=trace,
            audit=total,
            citations=citations,
            timings=recorder.timings,
            mode=RunMode.OBLIVION.value,
        )

    @staticmethod
    def _dedupe(items: list[Obligation]) -> list[Obligation]:
        out: list[Obligation] = []
        seen: set[str] = set()
        for obligation in items:
            key = obligation.text.strip().lower()
            if key and key not in seen:
                out.append(obligation)
                seen.add(key)
        return out
