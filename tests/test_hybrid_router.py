from oblivion_textlm.router import HybridObligationRouter
from oblivion_textlm.types import Obligation, TextChunk

def test_hybrid_router_prefers_related_chunk():
    router = HybridObligationRouter(top_k=1, embed_dimensions=64)
    chunks = [
        TextChunk("a", "verified semantic obligation retirement"),
        TextChunk("b", "a cooking recipe for soup"),
    ]
    selected, _ = router.route(
        "When may an obligation be retired?",
        [Obligation("o", "find retirement condition")],
        chunks,
    )
    assert selected[0].id == "a"
