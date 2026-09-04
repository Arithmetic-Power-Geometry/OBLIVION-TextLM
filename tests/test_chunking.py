from oblivion_textlm.chunking import chunk_text


def test_chunking_nonempty_and_unique():
    chunks = chunk_text("alpha beta gamma delta epsilon " * 100, 120, 20)
    assert len(chunks) > 1
    assert len({chunk.id for chunk in chunks}) == len(chunks)


def test_chunking_empty():
    assert chunk_text("   ") == []
