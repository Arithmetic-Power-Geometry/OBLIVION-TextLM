# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

from ..llm_client import OpenAICompatibleClient


def build_openai_compatible(
    base_url: str,
    api_key: str,
    model: str,
    timeout: float = 120.0,
) -> OpenAICompatibleClient:
    return OpenAICompatibleClient(base_url, api_key, model, timeout)
