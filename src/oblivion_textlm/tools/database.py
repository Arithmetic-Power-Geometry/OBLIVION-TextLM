# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

import sqlite3
from pathlib import Path

from .base import ToolResult


class ReadOnlySQLiteTool:
    name = "sqlite_read"
    description = "Run a read-only SELECT query against a configured SQLite database."

    def __init__(self, path: str | Path):
        self.path = str(path)

    def run(self, arguments: dict) -> ToolResult:
        query = str(arguments.get("query", "")).strip()
        if not query.lower().startswith("select"):
            return ToolResult(False, "only SELECT statements are permitted")
        try:
            uri = f"file:{self.path}?mode=ro"
            with sqlite3.connect(uri, uri=True) as connection:
                rows = connection.execute(query).fetchmany(100)
            return ToolResult(True, repr(rows))
        except Exception as exc:
            return ToolResult(False, f"database error: {exc}")
