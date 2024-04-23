import pytest
from unittest.mock import patch
from ..goldbar import GoldBarWeighing


@pytest.fixture
def gold_bar_weighing():
    """
    Creates a test fixture with a mocked GoldBarWeighing instance.

    Returns:
        An instance of the GoldBarWeighing class equipped with a mocked WebDriver.
    """
    with patch('selenium.webdriver.Chrome') as MockWebDriver:
       
        gb = GoldBarWeighing()
        gb.driver = MockWebDriver()
        return gb


def test_valid_bar_values_all_correct(gold_bar_weighing):
    """
    Test that valid_bar_values correctly returns True when all the conditions are satisfied

    Asserts:
        All the bars satisy the conditions.
    """
    left = [0, 1, 2]
    right = [3, 4, 5]
    remaining = [6, 7, 8]
    expected = True
    assert gold_bar_weighing.valid_bar_values(left, right, remaining) == expected

def test_valid_bar_values_not_unique(gold_bar_weighing):
    """
    Test that valid_bar_values correctly returns False when the values are not unique

    Asserts:
        All the bars satisy the conditions.
    """
    left = [0, 0, 2]
    right = [3, 4, 5]
    remaining = [6, 7, 8]
    expected = False

    assert gold_bar_weighing.valid_bar_values(left, right, remaining) == expected

def test_valid_bar_values_length_not_three(gold_bar_weighing):
    """
    Test that valid_bar_values correctly returns False when the length of bars is not equal to 3

    Asserts:
        All the bars satisy the conditions.
    """
    left = [0, 1, 2, 5]
    right = [3, 4]
    remaining = [6, 7, 8]
    expected = False

    assert gold_bar_weighing.valid_bar_values(left, right, remaining) == expected

def test_valid_bar_values_not_between_0_8(gold_bar_weighing):
    """
    Test that valid_bar_values correctly returns False when the values are not between 0-8

    Asserts:
        All the bars satisy the conditions.
    """
    left = [0, 1, 2]
    right = [3, 4, 5]
    remaining = [6, 7, 10]
    expected = False

    assert gold_bar_weighing.valid_bar_values(left, right, remaining) == expected


