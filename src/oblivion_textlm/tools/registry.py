# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

from .base import Tool, ToolResult


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def names(self) -> list[str]:
        return sorted(self._tools)

    def call(self, name: str, arguments: dict) -> ToolResult:
        if name not in self._tools:
            return ToolResult(False, f"Unknown tool: {name}")
        return self._tools[name].run(arguments)
