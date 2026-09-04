# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

import json
from pathlib import Path

from .embeddings import Embedder, cosine_similarity
from .types import TextChunk


class PersistentVectorStore:
    """Small dependency-free vector index suitable for documents and tests."""

    def __init__(self, embedder: Embedder, path: str | Path | None = None):
        self.embedder = embedder
        self.path = Path(path) if path else None
        self._items: dict[str, tuple[TextChunk, list[float]]] = {}
        if self.path and self.path.exists():
            self.load()

    def upsert(self, chunks: list[TextChunk]) -> None:
        for chunk in chunks:
            self._items[chunk.id] = (chunk, self.embedder.embed(chunk.text))
        if self.path:
            self.save()

    def search(self, query: str, top_k: int = 8) -> list[tuple[float, TextChunk]]:
        q = self.embedder.embed(query)
        scored = [
            (cosine_similarity(q, vector), chunk)
            for chunk, vector in self._items.values()
        ]
        scored.sort(key=lambda item: (-item[0], item[1].id))
        return scored[: max(0, top_k)]

    def save(self) -> None:
        if not self.path:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = []
        for chunk, vector in self._items.values():
            payload.append(
                {
                    "chunk": {
                        "id": chunk.id,
                        "text": chunk.text,
                        "source": chunk.source,
                        "page": chunk.page,
                        "section": chunk.section,
                        "start_char": chunk.start_char,
                        "end_char": chunk.end_char,
                        "source_url": chunk.source_url,
                        "metadata": chunk.metadata,
                    },
                    "vector": vector,
                }
            )
        self.path.write_text(json.dumps(payload), encoding="utf-8")

    def load(self) -> None:
        if not self.path:
            return
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        self._items.clear()
        for item in payload:
            chunk = TextChunk(**item["chunk"])
            self._items[chunk.id] = (chunk, [float(x) for x in item["vector"]])
