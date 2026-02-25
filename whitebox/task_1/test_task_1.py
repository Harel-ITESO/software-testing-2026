from whitebox.exercises import (
    check_number_status,
    validate_password,
    calculate_total_discount,
    calculate_order_total,
    calculate_items_shipping_cost,
    validate_login,
    verify_age,
    categorize_product,
    validate_email,
    celsius_to_fahrenheit,
    validate_credit_card,
    validate_date,
    check_flight_eligibility,
    validate_url,
    calculate_quantity_discount,
    check_file_size,
    check_loan_eligibility,
    calculate_shipping_cost,
    grade_quiz,
    authenticate_user,
    get_weather_advisory,
)

import pytest


# 1) check_number_status
@pytest.mark.parametrize(
    "number, expected",
    [
        (10, "Positive"),
        (-3, "Negative"),
        (0, "Zero"),
    ],
)
def test_check_number_status(number, expected):
    assert check_number_status(number) == expected


# 2) validate_password
@pytest.mark.parametrize(
    "password, expected",
    [
        ("Aa1!aaa", False),  # len < 8
        ("aa1!aaaa", False),  # no uppercase
        ("AA1!AAAA", False),  # no lowercase
        ("Aa!aaaaa", False),  # no digit
        ("Aa1aaaaa", False),  # no special from [!@#$%&]
        ("Strong1!", True),  # valid
    ],
)
def test_validate_password(password, expected):
    assert validate_password(password) is expected


# 3) calculate_total_discount
@pytest.mark.parametrize(
    "total_amount, expected",
    [
        (99, 0),
        (100, 10),
        (500, 50),
        (600, 120),
    ],
)
def test_calculate_total_discount(total_amount, expected):
    assert calculate_total_discount(total_amount) == pytest.approx(expected)


# 4) calculate_order_total
@pytest.mark.parametrize(
    "items, expected",
    [
        ([{"quantity": 1, "price": 10}], 10),  # no discount
        ([{"quantity": 5, "price": 10}], 50),  # no discount boundary
        ([{"quantity": 6, "price": 10}], 57),  # 5% discount boundary
        ([{"quantity": 10, "price": 10}], 95),  # 5% discount boundary
        ([{"quantity": 11, "price": 10}], 99),  # 10% discount
        (
            [
                {"quantity": 1, "price": 10},
                {"quantity": 6, "price": 10},
                {"quantity": 11, "price": 10},
            ],
            166,
        ),  # mixed branches
    ],
)
def test_calculate_order_total(items, expected):
    assert calculate_order_total(items) == pytest.approx(expected)


# 5) calculate_items_shipping_cost
@pytest.mark.parametrize(
    "items, method, expected",
    [
        ([{"weight": 5}], "standard", 10),
        ([{"weight": 5.1}], "standard", 15),
        ([{"weight": 10.1}], "standard", 20),
        ([{"weight": 5}], "express", 20),
        ([{"weight": 5.1}], "express", 30),
        ([{"weight": 10.1}], "express", 40),
    ],
)
def test_calculate_items_shipping_cost(items, method, expected):
    assert calculate_items_shipping_cost(items, method) == expected


def test_calculate_items_shipping_cost_invalid_method():
    with pytest.raises(ValueError, match="Invalid shipping method"):
        calculate_items_shipping_cost([{"weight": 1}], "overnight")


# 6) validate_login
@pytest.mark.parametrize(
    "username, password, expected",
    [
        ("abcde", "12345678", "Login Successful"),  # min bounds
        ("a" * 20, "b" * 15, "Login Successful"),  # max bounds
        ("abcd", "12345678", "Login Failed"),  # short username
        ("abcde", "1234567", "Login Failed"),  # short password
        ("a" * 21, "12345678", "Login Failed"),  # long username
        ("abcde", "b" * 16, "Login Failed"),  # long password
    ],
)
def test_validate_login(username, password, expected):
    assert validate_login(username, password) == expected


# 7) verify_age
@pytest.mark.parametrize(
    "age, expected",
    [
        (18, "Eligible"),
        (65, "Eligible"),
        (17, "Not Eligible"),
        (66, "Not Eligible"),
    ],
)
def test_verify_age(age, expected):
    assert verify_age(age) == expected


# 8) categorize_product
@pytest.mark.parametrize(
    "price, expected",
    [
        (10, "Category A"),
        (50, "Category A"),
        (51, "Category B"),
        (100, "Category B"),
        (101, "Category C"),
        (200, "Category C"),
        (9, "Category D"),
        (201, "Category D"),
    ],
)
def test_categorize_product(price, expected):
    assert categorize_product(price) == expected


# 9) validate_email
@pytest.mark.parametrize(
    "email, expected",
    [
        ("a@.b", "Invalid Email"),  # too short
        ("userexample.com", "Invalid Email"),  # missing @
        ("user@examplecom", "Invalid Email"),  # missing .
        ("a@b." + "c" * 47, "Invalid Email"),  # too long (51 chars)
        ("user@example.com", "Valid Email"),
    ],
)
def test_validate_email(email, expected):
    assert validate_email(email) == expected


# 10) celsius_to_fahrenheit
@pytest.mark.parametrize(
    "celsius, expected",
    [
        (-100, -148),
        (100, 212),
        (0, 32),
    ],
)
def test_celsius_to_fahrenheit_valid(celsius, expected):
    assert celsius_to_fahrenheit(celsius) == pytest.approx(expected)


@pytest.mark.parametrize("celsius", [-101, 101])
def test_celsius_to_fahrenheit_invalid(celsius):
    assert celsius_to_fahrenheit(celsius) == "Invalid Temperature"


# 11) validate_credit_card
@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1" * 13, "Valid Card"),
        ("1" * 16, "Valid Card"),
        ("1" * 12, "Invalid Card"),
        ("1" * 17, "Invalid Card"),
        ("1234abcd5678", "Invalid Card"),
    ],
)
def test_validate_credit_card(card_number, expected):
    assert validate_credit_card(card_number) == expected


# 12) validate_date
@pytest.mark.parametrize(
    "year, month, day, expected",
    [
        (1900, 1, 1, "Valid Date"),
        (2100, 12, 31, "Valid Date"),
        (1899, 1, 1, "Invalid Date"),
        (2101, 1, 1, "Invalid Date"),
        (2000, 0, 1, "Invalid Date"),
        (2000, 13, 1, "Invalid Date"),
        (2000, 1, 0, "Invalid Date"),
        (2000, 1, 32, "Invalid Date"),
    ],
)
def test_validate_date(year, month, day, expected):
    assert validate_date(year, month, day) == expected


# 13) check_flight_eligibility
@pytest.mark.parametrize(
    "age, frequent_flyer, expected",
    [
        (17, False, "Not Eligible to Book"),
        (18, False, "Eligible to Book"),
        (66, False, "Not Eligible to Book"),
        (66, True, "Eligible to Book"),  # frequent flyer override
    ],
)
def test_check_flight_eligibility(age, frequent_flyer, expected):
    assert check_flight_eligibility(age, frequent_flyer) == expected


# 14) validate_url
@pytest.mark.parametrize(
    "url, expected",
    [
        ("http://example.com", "Valid URL"),
        ("https://example.com", "Valid URL"),
        ("ftp://example.com", "Invalid URL"),
        ("http://" + "a" * 300, "Invalid URL"),
        ("https://" + "a" * 300, "Valid URL"),  # precedence in implementation
    ],
)
def test_validate_url(url, expected):
    assert validate_url(url) == expected


# 15) calculate_quantity_discount
@pytest.mark.parametrize(
    "quantity, expected",
    [
        (1, "No Discount"),
        (5, "No Discount"),
        (6, "5% Discount"),
        (10, "5% Discount"),
        (0, "10% Discount"),
        (11, "10% Discount"),
    ],
)
def test_calculate_quantity_discount(quantity, expected):
    assert calculate_quantity_discount(quantity) == expected


# 16) check_file_size
@pytest.mark.parametrize(
    "size_in_bytes, expected",
    [
        (0, "Valid File Size"),
        (1048576, "Valid File Size"),
        (-1, "Invalid File Size"),
        (1048577, "Invalid File Size"),
    ],
)
def test_check_file_size(size_in_bytes, expected):
    assert check_file_size(size_in_bytes) == expected


# 17) check_loan_eligibility
@pytest.mark.parametrize(
    "income, credit_score, expected",
    [
        (29999, 800, "Not Eligible"),
        (30000, 700, "Secured Loan"),
        (60000, 701, "Standard Loan"),
        (70000, 751, "Premium Loan"),
        (70000, 750, "Standard Loan"),
    ],
)
def test_check_loan_eligibility(income, credit_score, expected):
    assert check_loan_eligibility(income, credit_score) == expected


# 18) calculate_shipping_cost
@pytest.mark.parametrize(
    "weight, length, width, height, expected",
    [
        (1, 10, 10, 10, 5),
        (1.1, 11, 11, 11, 10),
        (5, 30, 30, 30, 10),
        (2, 10, 11, 11, 20),  # dimensions fail 2nd branch
        (6, 20, 20, 20, 20),  # weight fails 2nd branch
    ],
)
def test_calculate_shipping_cost(weight, length, width, height, expected):
    assert calculate_shipping_cost(weight, length, width, height) == expected


# 19) grade_quiz
@pytest.mark.parametrize(
    "correct_answers, incorrect_answers, expected",
    [
        (7, 2, "Pass"),
        (7, 3, "Conditional Pass"),  # fails first branch, passes second
        (5, 3, "Conditional Pass"),
        (4, 3, "Fail"),
        (5, 4, "Fail"),
    ],
)
def test_grade_quiz(correct_answers, incorrect_answers, expected):
    assert grade_quiz(correct_answers, incorrect_answers) == expected


# 20) authenticate_user
@pytest.mark.parametrize(
    "username, password, expected",
    [
        ("admin", "admin123", "Admin"),
        ("hello", "password", "User"),
        ("usr", "short", "Invalid"),
    ],
)
def test_authenticate_user(username, password, expected):
    assert authenticate_user(username, password) == expected


# 21) get_weather_advisory
@pytest.mark.parametrize(
    "temperature, humidity, expected",
    [
        (31, 71, "High Temperature and Humidity. Stay Hydrated."),
        (-1, 50, "Low Temperature. Bundle Up!"),
        (25, 80, "No Specific Advisory"),
    ],
)
def test_get_weather_advisory(temperature, humidity, expected):
    assert get_weather_advisory(temperature, humidity) == expected
