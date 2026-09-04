# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class ToolResult:
    ok: bool
    output: str
    metadata: dict | None = None


class Tool(Protocol):
    name: str
    description: str

    def run(self, arguments: dict) -> ToolResult: ...
