import json
from pathlib import Path

import pytest

from ddd.city_search import search_cities


def _load_cases():
    file_path = Path(__file__).parent / "test_data" / "city_search_cases.json"
    return json.loads(file_path.read_text(encoding="utf-8"))["cases"]


@pytest.mark.parametrize("case", _load_cases(), ids=lambda case: case["name"])
def test_search_cities(case):
    assert search_cities(case["search_text"]) == case["expected"]
