# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

import time
from contextlib import contextmanager

from .types import StageTiming


class TraceRecorder:
    def __init__(self):
        self.timings: list[StageTiming] = []

    @contextmanager
    def stage(self, name: str, *, step: int | None = None, **details):
        started = time.perf_counter()
        try:
            yield
        finally:
            self.timings.append(
                StageTiming(
                    stage=name,
                    duration_ms=(time.perf_counter() - started) * 1000.0,
                    step=step,
                    details=details,
                )
            )
