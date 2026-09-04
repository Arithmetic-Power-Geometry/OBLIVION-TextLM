# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

import sqlite3
import time
from pathlib import Path


class DocumentStore:
    def __init__(self, path: str | Path = "data/oblivion_documents.db"):
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    document_id TEXT PRIMARY KEY,
                    owner_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    text TEXT NOT NULL,
                    created REAL NOT NULL
                )
                """
            )

    def put(self, document_id: str, owner_id: str, title: str, text: str) -> None:
        with sqlite3.connect(self.path) as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO documents(document_id, owner_id, title, text, created)
                VALUES (?, ?, ?, ?, ?)
                """,
                (document_id, owner_id, title, text, time.time()),
            )

    def get(self, document_id: str, owner_id: str) -> str | None:
        with sqlite3.connect(self.path) as connection:
            row = connection.execute(
                "SELECT text FROM documents WHERE document_id = ? AND owner_id = ?",
                (document_id, owner_id),
            ).fetchone()
        return row[0] if row else None
