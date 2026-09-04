# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

import re
from difflib import SequenceMatcher

_WORD = re.compile(r"\w+")


def text_delta(a: str, b: str) -> float:
    sequence_delta = 1.0 - SequenceMatcher(None, a.strip().lower(), b.strip().lower()).ratio()
    left = set(_WORD.findall(a.lower()))
    right = set(_WORD.findall(b.lower()))
    union = left | right
    jaccard_delta = 0.0 if not union else 1.0 - len(left & right) / len(union)
    return max(0.0, min(1.0, 0.5 * sequence_delta + 0.5 * jaccard_delta))
