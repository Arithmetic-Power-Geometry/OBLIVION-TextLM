# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class KVBlock:
    block_id: str
    obligation_ids: set[str] = field(default_factory=set)
    bytes_used: int = 0


class KVCacheManager:
    """Advisory obligation-to-KV ownership map.

    It does not claim physical eviction from a third-party inference engine. A provider
    adapter may use `eligible_for_eviction` to perform real eviction where supported.
    """

    def __init__(self):
        self.blocks: dict[str, KVBlock] = {}

    def register(self, block_id: str, obligation_ids: set[str], bytes_used: int = 0) -> None:
        self.blocks[block_id] = KVBlock(block_id, set(obligation_ids), max(0, bytes_used))

    def eligible_for_eviction(self, live_obligation_ids: set[str]) -> list[str]:
        return [
            block_id
            for block_id, block in self.blocks.items()
            if not (block.obligation_ids & live_obligation_ids)
        ]

    def tracked_bytes(self) -> int:
        return sum(block.bytes_used for block in self.blocks.values())
