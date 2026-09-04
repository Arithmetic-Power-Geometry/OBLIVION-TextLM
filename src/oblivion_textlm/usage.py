# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class UsageRecord:
    user_id: str
    input_tokens: int
    output_tokens: int
    requests: int = 1


class UsageLedger:
    def __init__(self):
        self.records: list[UsageRecord] = []

    def add(self, record: UsageRecord) -> None:
        self.records.append(record)

    def totals(self, user_id: str) -> dict[str, int]:
        selected = [record for record in self.records if record.user_id == user_id]
        return {
            "input_tokens": sum(record.input_tokens for record in selected),
            "output_tokens": sum(record.output_tokens for record in selected),
            "requests": sum(record.requests for record in selected),
        }
