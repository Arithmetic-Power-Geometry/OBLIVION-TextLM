# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

from typing import Protocol

from ..types import ExecutorResult


class LanguageProvider(Protocol):
    async def chat(
        self,
        messages: list[dict],
        *,
        temperature: float = 0.0,
        max_tokens: int = 700,
    ) -> ExecutorResult: ...
