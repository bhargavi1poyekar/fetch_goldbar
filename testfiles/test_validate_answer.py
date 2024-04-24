import pytest
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from unittest.mock import MagicMock, patch
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
        gb.weigh = MagicMock()
        gb.find_suspected_bars = MagicMock()
        return gb


def test_validate_answer_correct(gold_bar_weighing):
    """
    Test the `validate_answer` method for correct identification of the fake bar.

    Asserts:
        - The method returns True for correct fake bar identification.
        - The alert is accepted once as expected.
    """
    gold_bar_weighing.driver.switch_to.alert.text = "Yay! You find it!"
    assert gold_bar_weighing.validate_answer(3) is True
    gold_bar_weighing.driver.switch_to.alert.accept.assert_called_once()


def test_validate_answer_incorrect(gold_bar_weighing):
    """
    Test the `validate_answer` method for incorrect identification of the fake bar.

    Asserts:
        - The method returns False for incorrect fake bar identification.
        - The alert is accepted once as expected.
    """

    gold_bar_weighing.driver.switch_to.alert.text = "Oops Try again!"
    assert gold_bar_weighing.validate_answer(3) is False
    gold_bar_weighing.driver.switch_to.alert.accept.assert_called_once()
