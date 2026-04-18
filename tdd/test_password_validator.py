from tdd.password_validator import validate_password


def test_validate_password_accepts_valid_password():
    assert validate_password("Abcd12$%") == {"is_valid": True, "errors": []}


def test_validate_password_requires_minimum_length():
    assert validate_password("Ab12$") == {
        "is_valid": False,
        "errors": ["Password must be at least 8 characters"],
    }


def test_validate_password_requires_at_least_two_numbers():
    assert validate_password("Abcdefg$") == {
        "is_valid": False,
        "errors": ["The password must contain at least 2 numbers"],
    }


def test_validate_password_handles_multiple_errors():
    assert validate_password("password") == {
        "is_valid": False,
        "errors": [
            "The password must contain at least 2 numbers",
            "password must contain at least one capital letter",
            "password must contain at least one special character",
        ],
    }


def test_validate_password_requires_a_capital_letter():
    assert validate_password("abcd12$%") == {
        "is_valid": False,
        "errors": ["password must contain at least one capital letter"],
    }


def test_validate_password_requires_a_special_character():
    assert validate_password("Abcd1234") == {
        "is_valid": False,
        "errors": ["password must contain at least one special character"],
    }
