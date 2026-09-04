from oblivion_textlm.memory import ConversationMemory



def test_memory_round_trip(tmp_path):
    memory = ConversationMemory(tmp_path / "memory.db")
    memory.append("s", "user", "hello")
    memory.append("s", "assistant", "hi")
    assert [item["content"] for item in memory.history("s")] == ["hello", "hi"]
