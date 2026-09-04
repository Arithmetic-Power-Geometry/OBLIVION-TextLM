# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request

from .config import get_settings

_BUCKETS: dict[str, deque[float]] = defaultdict(deque)


async def authenticate(request: Request) -> str:
    settings = get_settings()
    if settings.env.lower() == "production" and settings.api_key_set == {"change-me"}:
        raise HTTPException(
            status_code=503,
            detail="Production API key is not configured",
        )

    auth = request.headers.get("authorization", "")
    if not auth.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")

    key = auth.split(" ", 1)[1].strip()
    if key not in settings.api_key_set:
        raise HTTPException(status_code=403, detail="Invalid API key")

    now = time.monotonic()
    bucket = _BUCKETS[key]
    while bucket and now - bucket[0] > 60.0:
        bucket.popleft()
    if len(bucket) >= settings.rate_limit_per_minute:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    bucket.append(now)
    return key
