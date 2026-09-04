# Copyright (c) 2026 Mohammad Amir Khusru Akhtar. All rights reserved.
from __future__ import annotations

from typing import Protocol

from .llm_client import OpenAICompatibleClient
from .types import Certificate, Obligation, TextChunk, Verdict
from .util import extract_json_object, stable_id


class ControlPlane(Protocol):
    async def construct(self, query: str, chunks: list[TextChunk]) -> list[Obligation]: ...

    async def births(
        self,
        query: str,
        current: list[Obligation],
        executor_text: str,
        chunks: list[TextChunk],
        step: int,
    ) -> list[Obligation]: ...

    async def certificate(
        self,
        query: str,
        obligation: Obligation,
        executor_text: str,
        chunks: list[TextChunk],
    ) -> Certificate: ...

    async def verify(
        self,
        query: str,
        obligation: Obligation,
        certificate: Certificate,
        executor_text: str,
        chunks: list[TextChunk],
    ) -> Verdict: ...


class LLMControlPlane:
    """Structured OBLIVION control plane with an optional independent verifier client."""

    def __init__(
        self,
        client: OpenAICompatibleClient,
        verify_threshold: float = 0.90,
        verifier_client: OpenAICompatibleClient | None = None,
    ):
        self.client = client
        self.verifier_client = verifier_client or client
        self.verify_threshold = verify_threshold

    async def _json(
        self,
        prompt: str,
        *,
        client: OpenAICompatibleClient | None = None,
    ) -> dict:
        selected = client or self.client
        result = await selected.chat(
            [
                {
                    "role": "system",
                    "content": "Return one valid JSON object only. No markdown.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            max_tokens=650,
        )
        return extract_json_object(result.text)

    async def construct(self, query: str, chunks: list[TextChunk]) -> list[Obligation]:
        sample = "\n".join(chunk.text[:500] for chunk in chunks[:4])
        payload = await self._json(
            f"""
Construct only the unresolved semantic jobs currently necessary to answer the query.
Do not predict every future hop.
Return:
{{"obligations":[{{"text":"...","reason":"...","confidence":0.0}}]}}

QUERY:
{query}

CONTEXT SAMPLE:
{sample}
"""
        )
        out: list[Obligation] = []
        for item in payload.get("obligations", [])[:8]:
            text = str(item.get("text", "")).strip()
            if not text:
                continue
            out.append(
                Obligation(
                    id=stable_id("o", text),
                    text=text,
                    reason=str(item.get("reason", "")),
                    confidence=float(item.get("confidence", 0.5)),
                    born_step=0,
                )
            )
        if out:
            return out
        fallback = f"resolve the user query: {query}"
        return [
            Obligation(
                id=stable_id("o", fallback),
                text=fallback,
                reason="fallback initial obligation",
                confidence=0.5,
                born_step=0,
            )
        ]

    async def births(
        self,
        query: str,
        current: list[Obligation],
        executor_text: str,
        chunks: list[TextChunk],
        step: int,
    ) -> list[Obligation]:
        current_text = "\n".join(f"{item.id}: {item.text}" for item in current)
        payload = await self._json(
            f"""
Intermediate evidence can reveal a new requirement. Propose only genuinely NEW
unresolved obligations not already listed. If none, return an empty list.
Return:
{{"births":[{{"text":"...","reason":"...","confidence":0.0}}]}}

QUERY:
{query}

CURRENT:
{current_text}

INTERMEDIATE:
{executor_text}
"""
        )
        seen = {item.text.strip().lower() for item in current}
        out: list[Obligation] = []
        for item in payload.get("births", [])[:6]:
            text = str(item.get("text", "")).strip()
            if not text or text.lower() in seen:
                continue
            out.append(
                Obligation(
                    id=stable_id("o", text),
                    text=text,
                    reason=str(item.get("reason", "")),
                    confidence=float(item.get("confidence", 0.5)),
                    born_step=step,
                )
            )
            seen.add(text.lower())
        return out

    async def certificate(
        self,
        query: str,
        obligation: Obligation,
        executor_text: str,
        chunks: list[TextChunk],
    ) -> Certificate:
        evidence = "\n".join(f"[{chunk.id}] {chunk.text[:600]}" for chunk in chunks)
        payload = await self._json(
            f"""
Create evidence for whether this obligation is finished. Evidence IDs must come from
the supplied IDs.
Return:
{{"claim":"completed|not_completed|uncertain","evidence_ids":["..."],
"rationale":"...","confidence":0.0}}

QUERY:
{query}

OBLIGATION:
{obligation.text}

INTERMEDIATE:
{executor_text}

EVIDENCE:
{evidence}
"""
        )
        valid = {chunk.id for chunk in chunks}
        evidence_ids = [item for item in payload.get("evidence_ids", []) if item in valid]
        return Certificate(
            obligation_id=obligation.id,
            claim=str(payload.get("claim", "uncertain")),
            evidence_ids=evidence_ids,
            rationale=str(payload.get("rationale", "")),
            confidence=float(payload.get("confidence", 0.0)),
        )

    async def verify(
        self,
        query: str,
        obligation: Obligation,
        certificate: Certificate,
        executor_text: str,
        chunks: list[TextChunk],
    ) -> Verdict:
        if (
            certificate.claim.lower() != "completed"
            or certificate.confidence < self.verify_threshold
            or not certificate.evidence_ids
        ):
            return Verdict.UNCERTAIN

        evidence_set = set(certificate.evidence_ids)
        evidence = "\n".join(
            f"[{chunk.id}] {chunk.text[:700]}" for chunk in chunks if chunk.id in evidence_set
        )
        payload = await self._json(
            f"""
Verify conservatively whether the cited evidence is sufficient to establish that the
obligation's remaining role for the query is complete.
Return:
{{"verdict":"VERIFIED|REJECTED|UNCERTAIN","confidence":0.0}}
Choose UNCERTAIN if evidence is incomplete or ambiguous.

QUERY:
{query}

OBLIGATION:
{obligation.text}

CERTIFICATE:
{certificate.rationale}

EVIDENCE:
{evidence}
""",
            client=self.verifier_client,
        )
        verdict = str(payload.get("verdict", "UNCERTAIN")).upper()
        confidence = float(payload.get("confidence", 0.0))
        if confidence < self.verify_threshold:
            return Verdict.UNCERTAIN
        if verdict not in Verdict._value2member_map_:
            return Verdict.UNCERTAIN
        return Verdict(verdict)


class DeterministicDemoControl:
    async def construct(self, query: str, chunks: list[TextChunk]) -> list[Obligation]:
        text = "identify the bicycle referred to by Rahul and determine its colour"
        return [
            Obligation(
                id=stable_id("o", text),
                text=text,
                reason="query requirement",
                confidence=1.0,
                born_step=0,
            )
        ]

    async def births(
        self,
        query: str,
        current: list[Obligation],
        executor_text: str,
        chunks: list[TextChunk],
        step: int,
    ) -> list[Obligation]:
        return []

    async def certificate(
        self,
        query: str,
        obligation: Obligation,
        executor_text: str,
        chunks: list[TextChunk],
    ) -> Certificate:
        ids = [chunk.id for chunk in chunks if "red" in chunk.text.lower()]
        return Certificate(
            obligation.id,
            "completed" if ids else "uncertain",
            ids,
            "Evidence states the requested colour.",
            1.0 if ids else 0.0,
        )

    async def verify(
        self,
        query: str,
        obligation: Obligation,
        certificate: Certificate,
        executor_text: str,
        chunks: list[TextChunk],
    ) -> Verdict:
        if certificate.claim == "completed" and certificate.evidence_ids:
            return Verdict.VERIFIED
        return Verdict.UNCERTAIN
