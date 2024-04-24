import pytest
from unittest.mock import patch
from ..app import GoldBarWeighing


@pytest.fixture
def gold_bar_weighing():
    """
    Creates a test fixture with a mocked GoldBarWeighing instance.

    Returns:
        An instance of the GoldBarWeighing class equipped with a mocked WebDriver.
    """
    with patch('selenium.webdriver.Chrome') as MockWebDriver:
       
        gb = GoldBarWeighing(MockWebDriver())
        return gb


def test_find_suspected_bars_result_less_than(gold_bar_weighing):
    """
    Test that `find_suspected_bars` correctly identifies the left group as
    suspected when the result is '<'.

    Asserts:
        The left group is returned as suspected fake bars when the weighing result
        is less than ('<').
    """
    left = [1, 2, 3]
    right = [4, 5, 6]
    remaining = [7, 8, 9]
    result = '<'
    expected = left
    assert gold_bar_weighing.find_suspected_bars(left, right, remaining, result) == expected


def test_find_suspected_bars_result_greater_than(gold_bar_weighing):
    """
    Test that `find_suspected_bars` correctly identifies the right group as suspected
    when the result is '>'.

    Asserts:
        The right group is returned as suspected fake bars when the weighing result
        is greater than ('>').
    """

    left = [1, 2, 3]
    right = [4, 5, 6]
    remaining = [7, 8, 9]
    result = '>'
    expected = right
    assert gold_bar_weighing.find_suspected_bars(left, right, remaining, result) == expected


def test_find_suspected_bars_result_equal(gold_bar_weighing):
    """
    Test that `find_suspected_bars` correctly identifies the remaining group as suspected
    when the result is '='.

    Asserts:
        The remaining group is returned as suspected fake bars when the weighing result
        is equal ('=').
    """
    left = [1, 2, 3]
    right = [4, 5, 6]
    remaining = [7, 8, 9]
    result = '='
    expected = remaining
    assert gold_bar_weighing.find_suspected_bars(left, right, remaining, result) == expected


def test_find_suspected_bars_unexpected_result(gold_bar_weighing):
    """
    Test that `find_suspected_bars` raises a ValueError when an unexpected result is provided.

    Asserts:
        A ValueError is raised due to the unexpected result.
    """
    left = [1, 2, 3]
    right = [4, 5, 6]
    remaining = [7, 8, 9]
    result = '?'
    with pytest.raises(ValueError):
        gold_bar_weighing.find_suspected_bars(left, right, remaining, result)
