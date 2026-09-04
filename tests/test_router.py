from oblivion_textlm.router import LexicalObligationRouter
from oblivion_textlm.types import Obligation, TextChunk


def test_router_prefers_matching_chunk():
    chunks = [
        TextChunk("a", "Maya owns a red bicycle."),
        TextChunk("b", "The capital of France is Paris."),
    ]
    obligations = [Obligation("o", "find Maya bicycle colour")]
    selected, _ = LexicalObligationRouter(1).route(
        "What colour is Maya's bicycle?",
        obligations,
        chunks,
    )
    assert selected[0].id == "a"
