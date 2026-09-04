# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TokenPrice:
    input_per_million: float
    output_per_million: float


def estimate_cost(input_tokens: int, output_tokens: int, price: TokenPrice) -> float:
    return (
        max(0, input_tokens) * price.input_per_million
        + max(0, output_tokens) * price.output_per_million
    ) / 1_000_000.0
