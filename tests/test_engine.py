import pytest

from oblivion_textlm.audit import CostModel
from oblivion_textlm.chunking import chunk_text
from oblivion_textlm.control import DeterministicDemoControl
from oblivion_textlm.engine import OblivionTextLM
from oblivion_textlm.executor import DeterministicDemoExecutor
from oblivion_textlm.router import LexicalObligationRouter

@pytest.mark.asyncio
async def test_full_demo_retires_verified_obligation():
    context = (
        "Rahul borrowed Maya's bicycle. Maya's bicycle was painted red. "
        "Other facts are irrelevant."
    )
    query = "What colour is Rahul's bicycle?"
    engine = OblivionTextLM(
        DeterministicDemoExecutor(),
        DeterministicDemoControl(),
        LexicalObligationRouter(3),
        CostModel(controller_weight=0.0),
        max_steps=2,
    )
    result = await engine.infer(query, chunk_text(context, 100, 10))
    assert "red" in result.answer.lower()
    assert result.obligations == []
    assert result.trace[0].retirements[0]["decision"] == "RETIRE"

@pytest.mark.asyncio
async def test_uncertain_keeps_obligation():
    context = "Rahul owns a bicycle. No colour is stated."
    query = "What colour is Rahul's bicycle?"
    engine = OblivionTextLM(
        DeterministicDemoExecutor(),
        DeterministicDemoControl(),
        LexicalObligationRouter(3),
        CostModel(controller_weight=0.0),
        max_steps=1,
    )
    result = await engine.infer(query, chunk_text(context, 100, 10))
    assert len(result.obligations) == 1
    assert result.trace[0].retirements[0]["decision"] == "KEEP"
