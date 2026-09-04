# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

import os
import resource
import subprocess
import time

from ..types import HardwareMetrics


class HardwareProfiler:
    """Portable process metrics plus optional NVIDIA-SMI sampling."""

    def __init__(self):
        self._wall_start = 0.0
        self._cpu_start = 0.0

    def start(self) -> None:
        self._wall_start = time.perf_counter()
        self._cpu_start = time.process_time()

    def stop(self) -> HardwareMetrics:
        wall_ms = (time.perf_counter() - self._wall_start) * 1000.0
        cpu_seconds = max(0.0, time.process_time() - self._cpu_start)
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        # Linux reports KiB; macOS reports bytes.
        max_rss_mb = rss / (1024.0 if os.name == "posix" else 1024.0 * 1024.0)
        gpu_memory, gpu_util = self._nvidia_metrics()
        return HardwareMetrics(
            wall_ms=wall_ms,
            process_cpu_seconds=cpu_seconds,
            max_rss_mb=max_rss_mb,
            gpu_memory_mb=gpu_memory,
            gpu_utilization_pct=gpu_util,
        )

    @staticmethod
    def _nvidia_metrics() -> tuple[float | None, float | None]:
        try:
            output = subprocess.check_output(
                [
                    "nvidia-smi",
                    "--query-gpu=memory.used,utilization.gpu",
                    "--format=csv,noheader,nounits",
                ],
                stderr=subprocess.DEVNULL,
                timeout=2,
                text=True,
            )
            first = output.strip().splitlines()[0]
            memory, util = [float(part.strip()) for part in first.split(",")[:2]]
            return memory, util
        except Exception:
            return None, None
