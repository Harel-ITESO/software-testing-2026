from tdd.fizz_buzz import fizz_buzz


def test_returns_number_as_string_when_not_fizz_or_buzz():
    assert fizz_buzz(1) == "1"


def test_returns_fizz_for_multiples_of_three():
    assert fizz_buzz(3) == "Fizz"


def test_returns_buzz_for_multiples_of_five():
    assert fizz_buzz(5) == "Buzz"


def test_returns_fizz_buzz_for_multiples_of_three_and_five():
    assert fizz_buzz(15) == "FizzBuzz"
