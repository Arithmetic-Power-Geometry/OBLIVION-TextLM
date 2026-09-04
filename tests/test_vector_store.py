from oblivion_textlm.embeddings import HashingEmbedder
from oblivion_textlm.types import TextChunk
from oblivion_textlm.vector_store import PersistentVectorStore

def test_vector_store_returns_chunk():
    store = PersistentVectorStore(HashingEmbedder(64))
    store.upsert(
        [
            TextChunk("a", "semantic obligation retirement"),
            TextChunk("b", "banana recipe"),
        ]
    )
    found = store.search("semantic obligation", top_k=1)
    assert found and found[0][1].id == "a"
