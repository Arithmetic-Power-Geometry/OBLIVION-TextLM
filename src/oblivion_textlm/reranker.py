# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

import re
from collections import Counter

from .embeddings import Embedder, cosine_similarity
from .types import Obligation, TextChunk

_WORD = re.compile(r"[A-Za-z0-9_'-]+")


def lexical_score(query: str, text: str) -> float:
    q = Counter(_WORD.findall(query.lower()))
    t = Counter(_WORD.findall(text.lower()))
    if not q or not t:
        return 0.0
    overlap = sum(min(count, t.get(term, 0)) for term, count in q.items())
    return overlap / max(1, sum(q.values()))


class HybridReranker:
    def __init__(
        self,
        embedder: Embedder,
        *,
        lexical_weight: float = 0.35,
        semantic_weight: float = 0.65,
    ):
        total = lexical_weight + semantic_weight
        if total <= 0:
            raise ValueError("reranker weights must sum to a positive value")
        self.embedder = embedder
        self.lexical_weight = lexical_weight / total
        self.semantic_weight = semantic_weight / total

    def rank(
        self,
        query: str,
        obligations: list[Obligation],
        chunks: list[TextChunk],
    ) -> list[tuple[float, TextChunk]]:
        task = query + " " + " ".join(obligation.text for obligation in obligations)
        task_embedding = self.embedder.embed(task)
        scored: list[tuple[float, TextChunk]] = []
        for chunk in chunks:
            lexical = lexical_score(task, chunk.text)
            semantic = cosine_similarity(task_embedding, self.embedder.embed(chunk.text))
            score = self.lexical_weight * lexical + self.semantic_weight * semantic
            scored.append((score, chunk))
        scored.sort(key=lambda item: (-item[0], item[1].id))
        return scored
