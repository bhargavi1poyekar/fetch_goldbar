import pytest
from unittest.mock import MagicMock, patch
from ..goldbar import GoldBarWeighing
from ..web_driver_utilities import WebDriverUtility
 

left = [0, 1, 2]
right = [3, 4, 5]
remaining = [6, 7, 8]

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
            gb.weigh = MagicMock()
            gb.find_suspected_bars = MagicMock()
            return gb


def test_find_fake_bar_less_equal(gold_bar_weighing):
    """
    Test the identification of the fake bar when the first weighing result is '<'
    and the second is '='.

    Asserts:
        Asserts that the identified fake bar is correct based on the
        simulated weighing results.
    """

    gold_bar_weighing.weigh.side_effect = ['<', '=']
    gold_bar_weighing.find_suspected_bars.side_effect = [
        [0, 1, 2],
        [2]
    ]

    fake_bar = gold_bar_weighing.find_fake_bar(left, right, remaining)
    assert fake_bar == 2


def test_find_fake_bar_less_greater(gold_bar_weighing):
    """
    Test the identification of the fake bar when the first weighing result is '<'
    and the second is '>'.

    Asserts:
        Asserts that the identified fake bar is correct based on the simulated weighing results.
    """
    gold_bar_weighing.weigh.side_effect = ['<', '>']
    gold_bar_weighing.find_suspected_bars.side_effect = [
        [0, 1, 2],
        [1]
    ]

    fake_bar = gold_bar_weighing.find_fake_bar(left, right, remaining)
    assert fake_bar == 1


def test_find_fake_bar_less_less(gold_bar_weighing):
    """
    Test the identification of the fake bar when both weighings result in '<'.

    Asserts:
        Asserts that the identified fake bar is correct based on the
        consecutive '<' weighing results.
    """
    gold_bar_weighing.weigh.side_effect = ['<', '<']
    gold_bar_weighing.find_suspected_bars.side_effect = [
        [0, 1, 2],
        [0]
    ]

    fake_bar = gold_bar_weighing.find_fake_bar(left, right, remaining)
    assert fake_bar == 0
