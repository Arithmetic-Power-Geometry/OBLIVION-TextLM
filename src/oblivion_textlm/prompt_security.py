# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

import re

_INJECTION = [
    re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.I),
    re.compile(r"reveal\s+(the\s+)?system\s+prompt", re.I),
    re.compile(r"developer\s+message", re.I),
]


def injection_signals(text: str) -> list[str]:
    return [pattern.pattern for pattern in _INJECTION if pattern.search(text)]
