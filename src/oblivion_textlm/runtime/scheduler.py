# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable


class InferenceScheduler:
    def __init__(self, concurrency: int = 4):
        if concurrency < 1:
            raise ValueError("concurrency must be >= 1")
        self._semaphore = asyncio.Semaphore(concurrency)

    async def run(self, job: Callable[[], Awaitable[object]]) -> object:
        async with self._semaphore:
            return await job()
