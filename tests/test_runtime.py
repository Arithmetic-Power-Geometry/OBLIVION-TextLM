from oblivion_textlm.runtime.batching import BatchItem, pack_batches
from oblivion_textlm.runtime.kv_manager import KVCacheManager


def test_kv_cache_retirement_eligibility():
    manager = KVCacheManager()
    manager.register("b1", {"o1"}, 100)
    manager.register("b2", {"o2"}, 200)
    assert manager.eligible_for_eviction({"o2"}) == ["b1"]


def test_batching_respects_budget():
    items = [BatchItem("a", 4, None), BatchItem("b", 5, None)]
    batches = pack_batches(items, 6)
    assert len(batches) == 2
