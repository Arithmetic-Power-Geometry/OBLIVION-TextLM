from oblivion_textlm.audit import CostModel

def test_positive_gain_when_verification_is_cheap():
    model = CostModel(controller_weight=0.0, active_token_weight=1.0)
    assert model.retirement_gain(100, 1000) > 0

def test_nonpositive_gain_can_keep():
    model = CostModel(controller_weight=10.0, active_token_weight=0.01)
    assert model.retirement_gain(0.01, 5) < 0
