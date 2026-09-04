# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

from dataclasses import dataclass

from .prompt_security import injection_signals


@dataclass(slots=True)
class SafetyResult:
    allowed: bool
    reason: str = ""
    signals: list[str] | None = None


class SafetyGuard:
    def __init__(self, max_query_chars: int = 20_000, max_context_chars: int = 2_000_000):
        self.max_query_chars = max_query_chars
        self.max_context_chars = max_context_chars

    def check(self, query: str, context: str) -> SafetyResult:
        if len(query) > self.max_query_chars:
            return SafetyResult(False, "query exceeds configured size limit")
        if len(context) > self.max_context_chars:
            return SafetyResult(False, "context exceeds configured size limit")
        signals = injection_signals(context)
        return SafetyResult(True, signals=signals)
