# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

from .types import TextChunk
from .util import stable_id


def chunk_text(
    text: str,
    chunk_chars: int = 1400,
    overlap: int = 180,
    *,
    source: str = "input",
    page: int | None = None,
    section: str | None = None,
    source_url: str | None = None,
) -> list[TextChunk]:
    if chunk_chars <= 0 or overlap < 0 or overlap >= chunk_chars:
        raise ValueError("Require chunk_chars > 0 and 0 <= overlap < chunk_chars")
    clean = " ".join(text.split())
    if not clean:
        return []

    out: list[TextChunk] = []
    start = 0
    index = 0
    while start < len(clean):
        end = min(len(clean), start + chunk_chars)
        if end < len(clean):
            boundary = clean.rfind(" ", start + chunk_chars // 2, end)
            if boundary > start:
                end = boundary
        part = clean[start:end].strip()
        if part:
            out.append(
                TextChunk(
                    id=stable_id(f"c{index}", f"{source}:{start}:{part}"),
                    text=part,
                    source=source,
                    page=page,
                    section=section,
                    start_char=start,
                    end_char=end,
                    source_url=source_url,
                )
            )
            index += 1
        if end >= len(clean):
            break
        start = max(start + 1, end - overlap)
    return out
