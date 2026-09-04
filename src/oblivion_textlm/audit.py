# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

from dataclasses import asdict

from .types import CostAudit


class CostModel:
    """SHC-aware operational accounting in configured normalized units."""

    def __init__(self, controller_weight: float = 1.0, active_token_weight: float = 1.0):
        self.controller_weight = controller_weight
        self.active_token_weight = active_token_weight

    def stage(
        self,
        *,
        routing_ms: float,
        verification_ms: float,
        executor_ms: float,
        input_tokens: int,
        output_tokens: int,
        active_chars: int,
        total_ms: float = 0.0,
        ttft_ms: float | None = None,
        peak_memory_mb: float | None = None,
        kv_cache_bytes: int | None = None,
    ) -> CostAudit:
        return CostAudit(
            encoding=0.0,
            routing=routing_ms * self.controller_weight,
            realizability=0.0,
            separation=verification_ms * self.controller_weight,
            transformation=0.0,
            active_work=input_tokens * self.active_token_weight,
            routing_ms=routing_ms,
            verification_ms=verification_ms,
            executor_ms=executor_ms,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            active_chars=active_chars,
            total_ms=total_ms,
            ttft_ms=ttft_ms,
            peak_memory_mb=peak_memory_mb,
            kv_cache_bytes=kv_cache_bytes,
        )

    def retirement_gain(
        self,
        projected_saved_tokens: float,
        verify_ms: float,
        transform_cost: float = 0.0,
    ) -> float:
        keep = max(0.0, projected_saved_tokens) * self.active_token_weight
        verify = max(0.0, verify_ms) * self.controller_weight
        return keep - verify - max(0.0, transform_cost)


def add_audit(total: CostAudit, stage: CostAudit) -> None:
    numeric = [
        "encoding",
        "routing",
        "realizability",
        "separation",
        "transformation",
        "active_work",
        "routing_ms",
        "verification_ms",
        "executor_ms",
        "input_tokens",
        "output_tokens",
        "active_chars",
        "total_ms",
    ]
    for key in numeric:
        setattr(total, key, getattr(total, key) + getattr(stage, key))
    total.ttft_ms = stage.ttft_ms if stage.ttft_ms is not None else total.ttft_ms
    if stage.peak_memory_mb is not None:
        total.peak_memory_mb = max(total.peak_memory_mb or 0.0, stage.peak_memory_mb)
    if stage.kv_cache_bytes is not None:
        total.kv_cache_bytes = stage.kv_cache_bytes
