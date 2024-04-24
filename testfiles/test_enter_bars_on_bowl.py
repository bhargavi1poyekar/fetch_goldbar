import pytest
from selenium.common.exceptions import NoSuchElementException
from unittest.mock import MagicMock, call, patch
from ..goldbar import GoldBarWeighing


@pytest.fixture
def gold_bar_weighing():
    """
    Creates a test fixture with a mocked GoldBarWeighing instance.
    Returns:
       An instance of the GoldBarWeighing class equipped with a mocked WebDriver.
    """
    with (patch('selenium.webdriver.Chrome') as MockWebDriver,
          patch('..web_driver_utilities.WebDriverUtility') as MockWebDriverUtility):
        # mocker.patch()
        gb = GoldBarWeighing(MockWebDriver())
        gb.webutils = MockWebDriverUtility()
        gb.webutils = MockWebDriverUtility()
        gb.webutils.set_text = MagicMock()
        gb.webutils.click_button_by_id = MagicMock()
        return gb


def test_enter_bars_on_bowl_success(gold_bar_weighing):
    """
    Test that `enter_bars_on_bowl` correctly interacts with web elements
    for a valid input range.

    Asserts:
        The method correctly calls `find_element` and `send_keys` for each bar index.
    """
    bars = [3, 4, 5]
    gold_bar_weighing.enter_bars_on_bowl(bars, 'left')
    expected_calls = [call(f"left_{i}", str(bar)) for i, bar in enumerate(bars)]
    for i in bars:
        gold_bar_weighing.driver.find_element.return_value.send_keys.assert_any_call(str(i))


def test_enter_bars_on_bowl_element_not_found(gold_bar_weighing):
    """
    Test that `enter_bars_on_bowl` raises a NoSuchElementException when an
    element is not found.

    Asserts:
        A NoSuchElementException is raised when an element is not
        found by the web driver.
    """
    gold_bar_weighing.driver.find_element.side_effect = NoSuchElementException
    with pytest.raises(NoSuchElementException):
        gold_bar_weighing.enter_bars_on_bowl([1, 2, 3], 'left')
