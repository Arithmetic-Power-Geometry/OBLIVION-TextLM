# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

import math
import re
import time
from collections import Counter

from .embeddings import HashingEmbedder
from .reranker import HybridReranker
from .types import Obligation, TextChunk

_WORD = re.compile(r"[A-Za-z0-9_'-]+")
_STOP = {
    "the", "a", "an", "and", "or", "of", "to", "in", "is", "are", "was",
    "were", "be", "for", "with", "on", "at", "by", "what", "which", "who",
    "when", "where", "why", "how",
}


def _terms(text: str) -> Counter[str]:
    return Counter(
        word.lower()
        for word in _WORD.findall(text)
        if word.lower() not in _STOP and len(word) > 1
    )


class LexicalObligationRouter:
    """Cheap deterministic Z(O_t) baseline."""

    def __init__(self, top_k: int = 6):
        self.top_k = top_k

    def route(
        self,
        query: str,
        obligations: list[Obligation],
        chunks: list[TextChunk],
    ) -> tuple[list[TextChunk], float]:
        started = time.perf_counter()
        if not chunks:
            return [], 0.0
        q = _terms(query + " " + " ".join(obligation.text for obligation in obligations))
        scored = []
        for chunk in chunks:
            terms = _terms(chunk.text)
            overlap = sum(min(value, terms.get(key, 0)) for key, value in q.items())
            norm = math.sqrt(sum(value * value for value in terms.values())) or 1.0
            scored.append((overlap / norm, chunk.id, chunk))
        scored.sort(key=lambda item: (-item[0], item[1]))
        selected = [chunk for _, _, chunk in scored[: min(self.top_k, len(scored))]]
        return selected, (time.perf_counter() - started) * 1000.0


class HybridObligationRouter:
    """Lexical + semantic obligation-aware routing with deterministic reranking."""

    def __init__(self, top_k: int = 6, embed_dimensions: int = 384):
        self.top_k = top_k
        self.embedder = HashingEmbedder(embed_dimensions)
        self.reranker = HybridReranker(self.embedder)

    def route(
        self,
        query: str,
        obligations: list[Obligation],
        chunks: list[TextChunk],
    ) -> tuple[list[TextChunk], float]:
        started = time.perf_counter()
        ranked = self.reranker.rank(query, obligations, chunks)
        selected = [chunk for _, chunk in ranked[: min(self.top_k, len(ranked))]]
        return selected, (time.perf_counter() - started) * 1000.0
