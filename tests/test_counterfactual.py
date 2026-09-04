from oblivion_textlm.counterfactual import text_delta


def test_delta_identical_zero():
    assert text_delta("red", "red") == 0


def test_delta_changed_positive():
    assert text_delta("red", "blue") > 0
