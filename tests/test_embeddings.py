from oblivion_textlm.embeddings import HashingEmbedder, cosine_similarity



def test_hash_embedding_is_deterministic():
    embedder = HashingEmbedder(64)
    assert embedder.embed("semantic obligation") == embedder.embed("semantic obligation")



def test_cosine_identity_positive():
    embedder = HashingEmbedder(64)
    vector = embedder.embed("query relative neural computation")
    assert cosine_similarity(vector, vector) > 0.99
