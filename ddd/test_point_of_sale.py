import json
from pathlib import Path

import pytest

from ddd.point_of_sale import scan, total


def _load_data():
    file_path = Path(__file__).parent / "test_data" / "point_of_sale_cases.json"
    return json.loads(file_path.read_text(encoding="utf-8"))


POINT_OF_SALE_DATA = _load_data()


@pytest.mark.parametrize(
    "case", POINT_OF_SALE_DATA["scan_cases"], ids=lambda case: case["name"]
)
def test_scan(case):
    assert scan(case["barcode"]) == case["expected"]


@pytest.mark.parametrize(
    "case", POINT_OF_SALE_DATA["total_cases"], ids=lambda case: case["name"]
)
def test_total(case):
    assert total(case["barcodes"]) == case["expected"]
