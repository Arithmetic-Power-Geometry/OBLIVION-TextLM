# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class BatchItem:
    request_id: str
    active_tokens: int
    payload: object


def pack_batches(items: list[BatchItem], max_batch_tokens: int) -> list[list[BatchItem]]:
    if max_batch_tokens <= 0:
        raise ValueError("max_batch_tokens must be positive")
    batches: list[list[BatchItem]] = []
    current: list[BatchItem] = []
    total = 0
    for item in sorted(items, key=lambda value: value.active_tokens):
        if current and total + item.active_tokens > max_batch_tokens:
            batches.append(current)
            current = []
            total = 0
        current.append(item)
        total += item.active_tokens
    if current:
        batches.append(current)
    return batches
