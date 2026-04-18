import json
from pathlib import Path
from unittest.mock import Mock, call

import pytest

from ddd.banking import Account


def _load_cases():
    file_path = Path(__file__).parent / "test_data" / "banking_cases.json"
    return json.loads(file_path.read_text(encoding="utf-8"))["cases"]


@pytest.mark.parametrize("case", _load_cases(), ids=lambda case: case["name"])
def test_account_prints_statement_from_data_driven_case(case):
    clock = Mock()
    clock.today.side_effect = case["dates"]
    printer = Mock()
    account = Account(clock=clock, printer=printer)

    for action in case["actions"]:
        if action["type"] == "deposit":
            account.deposit(action["amount"])
        else:
            account.withdraw(action["amount"])

    account.print_statement()

    expected_calls = [call(line) for line in case["expected_lines"]]
    printer.print.assert_has_calls(expected_calls)
    assert printer.print.call_count == len(case["expected_lines"])
