# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class Verdict(StrEnum):
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    UNCERTAIN = "UNCERTAIN"


class Decision(StrEnum):
    KEEP = "KEEP"
    RETIRE = "RETIRE"


class RunMode(StrEnum):
    BASELINE = "baseline"
    RAG = "rag"
    OBLIVION = "oblivion"


@dataclass(frozen=True, slots=True)
class TextChunk:
    id: str
    text: str
    source: str = "input"
    page: int | None = None
    section: str | None = None
    start_char: int | None = None
    end_char: int | None = None
    source_url: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Obligation:
    id: str
    text: str
    reason: str = ""
    confidence: float = 1.0
    born_step: int = 0
    evidence_ids: list[str] = field(default_factory=list)


@dataclass(slots=True)
class Certificate:
    obligation_id: str
    claim: str
    evidence_ids: list[str]
    rationale: str
    confidence: float


@dataclass(slots=True)
class SourceCitation:
    chunk_id: str
    source: str
    page: int | None = None
    section: str | None = None
    quote: str = ""


@dataclass(slots=True)
class StageTiming:
    stage: str
    duration_ms: float
    step: int | None = None
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class HardwareMetrics:
    wall_ms: float = 0.0
    process_cpu_seconds: float = 0.0
    max_rss_mb: float = 0.0
    gpu_memory_mb: float | None = None
    gpu_utilization_pct: float | None = None
    kv_cache_bytes: int | None = None
    ttft_ms: float | None = None
    tokens_per_second: float | None = None


@dataclass(slots=True)
class CostAudit:
    encoding: float = 0.0
    routing: float = 0.0
    realizability: float = 0.0
    separation: float = 0.0
    transformation: float = 0.0
    active_work: float = 0.0
    routing_ms: float = 0.0
    verification_ms: float = 0.0
    executor_ms: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0
    active_chars: int = 0
    total_ms: float = 0.0
    ttft_ms: float | None = None
    peak_memory_mb: float | None = None
    kv_cache_bytes: int | None = None

    @property
    def shc_total(self) -> float:
        return (
            self.encoding
            + self.routing
            + self.realizability
            + self.separation
            + self.transformation
            + self.active_work
        )


@dataclass(slots=True)
class ExecutorResult:
    text: str
    evidence_ids: list[str]
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: float = 0.0
    ttft_ms: float | None = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RetirementRecord:
    obligation_id: str
    verdict: Verdict
    decision: Decision
    gain: float
    counterfactual_delta: float | None
    reason: str


@dataclass(slots=True)
class StepTrace:
    step: int
    obligations_before: list[dict[str, Any]]
    active_chunk_ids: list[str]
    executor_text: str
    births: list[dict[str, Any]]
    retirements: list[dict[str, Any]]
    obligations_after: list[dict[str, Any]]
    audit: dict[str, Any]
    timings: list[dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class InferenceResult:
    answer: str
    obligations: list[Obligation]
    trace: list[StepTrace]
    audit: CostAudit
    citations: list[SourceCitation] = field(default_factory=list)
    timings: list[StageTiming] = field(default_factory=list)
    mode: str = RunMode.OBLIVION.value
