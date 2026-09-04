# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

from .types import SourceCitation, TextChunk


def build_citations(
    chunks: list[TextChunk],
    evidence_ids: list[str] | None = None,
    quote_chars: int = 240,
) -> list[SourceCitation]:
    wanted = set(evidence_ids or [chunk.id for chunk in chunks])
    out: list[SourceCitation] = []
    for chunk in chunks:
        if chunk.id not in wanted:
            continue
        quote = " ".join(chunk.text.split())
        if len(quote) > quote_chars:
            quote = quote[: quote_chars - 1].rstrip() + "…"
        out.append(
            SourceCitation(
                chunk_id=chunk.id,
                source=chunk.source,
                page=chunk.page,
                section=chunk.section,
                quote=quote,
            )
        )
    return out
