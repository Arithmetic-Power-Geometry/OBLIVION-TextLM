# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

import re
from dataclasses import dataclass

_TOKEN = re.compile(r"\w+|[^\w\s]", re.UNICODE)


@dataclass(slots=True)
class TokenCount:
    tokens: int
    exact: bool
    source: str


class TokenCounter:
    """Portable token accounting.

    Provider-reported usage is considered exact for billing/benchmark purposes.
    Local text counting is an estimator unless a deployment injects the executor's
    native tokenizer.
    """

    def count_text(self, text: str) -> TokenCount:
        return TokenCount(tokens=len(_TOKEN.findall(text)), exact=False, source="portable-estimator")

    def count_messages(self, messages: list[dict]) -> TokenCount:
        total = sum(self.count_text(str(message.get("content", ""))).tokens for message in messages)
        return TokenCount(tokens=total, exact=False, source="portable-estimator")
