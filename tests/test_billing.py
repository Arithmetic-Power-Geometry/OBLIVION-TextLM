from oblivion_textlm.billing import TokenPrice, estimate_cost

def test_cost_estimation():
    cost = estimate_cost(1_000_000, 500_000, TokenPrice(1.0, 2.0))
    assert cost == 2.0
