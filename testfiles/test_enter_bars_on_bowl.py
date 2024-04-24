import pytest
from selenium.common.exceptions import NoSuchElementException
from unittest.mock import MagicMock, call, patch
from ..app import GoldBarWeighing
from ..app import WebDriverUtility

@pytest.fixture
def gold_bar_weighing():
    """
    Creates a test fixture with a mocked GoldBarWeighing instance.
    Returns:
       An instance of the GoldBarWeighing class equipped with a mocked WebDriver.
    """
    with patch('selenium.webdriver.Chrome') as MockWebDriver:
        mocked_web_driver = MockWebDriver()

        with patch.object(WebDriverUtility, 'set_text') as mock_set_text, patch.object(WebDriverUtility, 'click_button_by_id') as mock_click:
        # mocker.patch()
            gb = GoldBarWeighing(mocked_web_driver)
            gb.webutils = WebDriverUtility(mocked_web_driver)
            gb.webutils.set_text = mock_set_text
            gb.webutils.click_button_by_id = mock_click
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
    gold_bar_weighing.webutils.set_text.assert_has_calls(expected_calls)

