import pytest

from tdd.string_calculator import add


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ("", 0),
        ("1", 1),
        ("1,2", 3),
        ("1,2,3,4", 10),
        ("1\n2,3", 6),
        ("//;\n1;3", 4),
        ("//|\n1|2|3", 6),
        ("//sep\n2sep5", 7),
        ("2,1001", 2),
    ],
)
def test_add_returns_sum_for_valid_inputs(numbers, expected):
    assert add(numbers) == expected


def test_add_rejects_separator_at_end():
    with pytest.raises(ValueError, match="Number expected but EOF found\\."):
        add("1,2,")


def test_add_rejects_wrong_separator_for_custom_delimiter():
    with pytest.raises(
        ValueError, match=r"'\|' expected but ',' found at position 3\."
    ):
        add("//|\n1|2,3")


def test_add_rejects_single_negative_number():
    with pytest.raises(ValueError, match=r"Negative number\(s\) not allowed: -2"):
        add("1,-2")


def test_add_rejects_multiple_negative_numbers():
    with pytest.raises(ValueError, match=r"Negative number\(s\) not allowed: -4, -9"):
        add("2,-4,-9")


def test_add_returns_multiple_errors_in_the_expected_order():
    with pytest.raises(
        ValueError,
        match=r"Negative number\(s\) not allowed: -3\n'\|' expected but ',' found at position 3\.",
    ):
        add("//|\n1|2,-3")
