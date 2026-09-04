# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

from collections.abc import Callable

from .base import ToolResult


class WebSearchTool:
    """Connector-neutral web-search tool.

    The product does not bundle a search provider or credentials. Supply an authorized
    provider callable in deployment.
    """

    name = "web_search"
    description = "Search the public web through a deployment-provided connector."

    def __init__(self, provider: Callable[[str], str] | None = None):
        self.provider = provider

    def run(self, arguments: dict) -> ToolResult:
        if self.provider is None:
            return ToolResult(False, "no web-search provider configured")
        query = str(arguments.get("query", "")).strip()
        return ToolResult(True, self.provider(query))
