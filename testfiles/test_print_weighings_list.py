import pytest
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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


def test_print_weighings_no_such_element(gold_bar_weighing):
    """
    Test the `print_weighings` method when an element is not found (NoSuchElementException).

    Asserts:
        - A NoSuchElementException is raised when an element is not found.
    """
    gold_bar_weighing.driver.find_elements.side_effect = NoSuchElementException
    with pytest.raises(NoSuchElementException):
        gold_bar_weighing.print_weighings_list()
        