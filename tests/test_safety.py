from oblivion_textlm.safety import SafetyGuard


def test_safety_size_limit():
    guard = SafetyGuard(max_query_chars=3, max_context_chars=10)
    assert not guard.check("abcd", "x").allowed
