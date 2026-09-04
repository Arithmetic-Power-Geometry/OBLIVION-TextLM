from oblivion_textlm.util import extract_json_object, stable_id


def test_json_extraction():
    assert extract_json_object('```json\n{"x":1}\n```')["x"] == 1


def test_stable_id():
    assert stable_id("o", "abc") == stable_id("o", "abc")
