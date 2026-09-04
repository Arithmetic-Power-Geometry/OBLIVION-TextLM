import pytest

from oblivion_textlm.audit import CostModel
from oblivion_textlm.baseline import BaselineTextLM
from oblivion_textlm.chunking import chunk_text
from oblivion_textlm.control import DeterministicDemoControl
from oblivion_textlm.engine import OblivionTextLM
from oblivion_textlm.executor import DeterministicDemoExecutor
from oblivion_textlm.rag import RAGTextLM
from oblivion_textlm.router import HybridObligationRouter

@pytest.mark.asyncio
async def test_three_modes_work():
    query = "What colour is Rahul's bicycle?"
    chunks = chunk_text(
        "Rahul borrowed Maya's bicycle. Maya's bicycle was painted red."
    )
    executor = DeterministicDemoExecutor()
    router = HybridObligationRouter(3, 64)

    baseline = await BaselineTextLM(executor).infer(query, chunks)
    rag = await RAGTextLM(executor, router).infer(query, chunks)
    oblivion = await OblivionTextLM(
        executor,
        DeterministicDemoControl(),
        router,
        CostModel(controller_weight=0.0),
        max_steps=2,
    ).infer(query, chunks)

    assert "red" in baseline.answer.lower()
    assert "red" in rag.answer.lower()
    assert "red" in oblivion.answer.lower()
    assert baseline.mode == "baseline"
    assert rag.mode == "rag"
    assert oblivion.mode == "oblivion"
