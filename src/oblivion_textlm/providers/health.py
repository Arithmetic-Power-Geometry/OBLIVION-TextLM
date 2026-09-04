# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

import httpx


async def provider_health(base_url: str, timeout: float = 5.0) -> tuple[bool, str]:
    candidates = ["/models", "/health"]
    async with httpx.AsyncClient(timeout=timeout) as client:
        for suffix in candidates:
            try:
                response = await client.get(base_url.rstrip("/") + suffix)
                if response.status_code < 500:
                    return True, f"{suffix}: HTTP {response.status_code}"
            except Exception:
                continue
    return False, "provider did not respond to health probes"
