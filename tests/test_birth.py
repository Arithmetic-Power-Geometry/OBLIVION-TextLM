import pytest

from oblivion_textlm.audit import CostModel
from oblivion_textlm.chunking import chunk_text
from oblivion_textlm.engine import OblivionTextLM
from oblivion_textlm.executor import DeterministicDemoExecutor
from oblivion_textlm.router import LexicalObligationRouter
from oblivion_textlm.types import Certificate, Obligation, Verdict
from oblivion_textlm.util import stable_id


class BirthControl:
    async def construct(self, query, chunks):
        text = "identify Rahul bicycle source"
        return [Obligation(stable_id("o", text), text, born_step=0)]

    async def births(self, query, current, executor_text, chunks, step):
        if step == 1:
            text = "determine Maya bicycle colour"
            return [Obligation(stable_id("o", text), text, born_step=step)]
        return []

    async def certificate(self, query, obligation, executor_text, chunks):
        if "Rahul" in obligation.text:
            return Certificate(
                obligation.id,
                "completed",
                [chunks[0].id],
                "source link established",
                1.0,
            )
        return Certificate(obligation.id, "uncertain", [], "not complete", 0.0)

    async def verify(self, query, obligation, certificate, executor_text, chunks):
        if certificate.claim == "completed":
            return Verdict.VERIFIED
        return Verdict.UNCERTAIN


@pytest.mark.asyncio
async def test_birth_is_added_while_old_obligation_is_discharged():
    engine = OblivionTextLM(
        DeterministicDemoExecutor(),
        BirthControl(),
        LexicalObligationRouter(2),
        CostModel(controller_weight=0.0),
        max_steps=1,
    )
    result = await engine.infer(
        "What colour is Rahul's bicycle?",
        chunk_text(
            "Rahul borrowed Maya's bicycle. Maya's bicycle was red.",
            100,
            10,
        ),
    )
    assert len(result.obligations) == 1
    assert "Maya" in result.obligations[0].text
    assert result.obligations[0].born_step == 1
