# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

from typing import Protocol

from .llm_client import OpenAICompatibleClient
from .types import ExecutorResult, Obligation, TextChunk


class Executor(Protocol):
    async def run(
        self,
        query: str,
        chunks: list[TextChunk],
        obligations: list[Obligation],
        prior: str,
        history: list[dict] | None = None,
    ) -> ExecutorResult: ...


class LLMExecutor:
    def __init__(self, client: OpenAICompatibleClient):
        self.client = client

    async def run(
        self,
        query: str,
        chunks: list[TextChunk],
        obligations: list[Obligation],
        prior: str,
        history: list[dict] | None = None,
    ) -> ExecutorResult:
        evidence = "\n\n".join(
            f"[{chunk.id}] source={chunk.source} page={chunk.page or '-'}\n{chunk.text}"
            for chunk in chunks
        )
        jobs = "\n".join(f"- {obligation.id}: {obligation.text}" for obligation in obligations)
        system = (
            "You are F_theta, the pretrained language executor inside OBLIVION TextLM. "
            "Answer from supplied evidence when evidence is present. Work on the live semantic "
            "obligations. Do not claim an obligation is retired; the OBLIVION verifier controls "
            "retirement. Cite evidence IDs in square brackets when supporting factual claims."
        )
        messages = [{"role": "system", "content": system}]
        for message in (history or [])[-12:]:
            if message.get("role") in {"user", "assistant", "system"}:
                messages.append(
                    {
                        "role": message["role"],
                        "content": str(message.get("content", "")),
                    }
                )
        messages.append(
            {
                "role": "user",
                "content": (
                    f"QUERY:\n{query}\n\nLIVE OBLIGATIONS:\n{jobs or '- none'}\n\n"
                    f"ACTIVE EVIDENCE:\n{evidence or '(none)'}\n\n"
                    f"PRIOR INTERMEDIATE RESULT:\n{prior or '(none)'}\n\n"
                    "Return the best current answer or intermediate conclusion."
                ),
            }
        )
        result = await self.client.chat(messages, temperature=0.0, max_tokens=900)
        result.evidence_ids = [chunk.id for chunk in chunks]
        return result


class DeterministicDemoExecutor:
    async def run(
        self,
        query: str,
        chunks: list[TextChunk],
        obligations: list[Obligation],
        prior: str,
        history: list[dict] | None = None,
    ) -> ExecutorResult:
        joined = " ".join(chunk.text for chunk in chunks).lower()
        if "rahul" in query.lower() and "bicycle" in query.lower() and "red" in joined:
            text = "Rahul's bicycle is red."
        elif chunks:
            text = chunks[0].text[:300]
        else:
            text = "Insufficient evidence."
        return ExecutorResult(
            text=text,
            evidence_ids=[chunk.id for chunk in chunks],
            input_tokens=20,
            output_tokens=8,
            latency_ms=1.0,
        )
