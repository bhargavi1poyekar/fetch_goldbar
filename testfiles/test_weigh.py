import pytest
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from unittest.mock import MagicMock, call, patch
from ..goldbar import GoldBarWeighing
from selenium.webdriver.common.by import By


@pytest.fixture
def gold_bar_weighing():
    """
    Creates a test fixture with a mocked GoldBarWeighing instance.

    Returns:
        An instance of the GoldBarWeighing class equipped with a mocked WebDriver.
    """
    with patch('selenium.webdriver.Chrome') as MockWebDriver:
        # mocker.patch()
        gb = GoldBarWeighing(MockWebDriver())
        mock_element = MagicMock()
        gb.driver.find_element = MagicMock()
        gb.driver.find_element.return_value = mock_element
        mock_element.text = "="
        return gb


def test_weigh_success(gold_bar_weighing):
    """
    Test the `weigh` method under successful conditions to ensure correct behavior.
    Asserts:
        - `enter_bars_on_bowl` is called with correct parameters for left and right bars.
        - The 'weigh' and 'reset' buttons are accessed and clicked as expected.
        - The final weighing result text is retrieved and actions are taken based on this result.
    """
    gold_bar_weighing.enter_bars_on_bowl = MagicMock()
    gold_bar_weighing.driver.find_element().click = MagicMock()
    gold_bar_weighing.driver.find_element().text = "="
    gold_bar_weighing.weigh([0, 1, 2], [3, 4, 5])
    gold_bar_weighing.driver.find_element.assert_any_call(By.ID, "weigh")
    gold_bar_weighing.driver.find_element.assert_any_call(By.ID, "reset")
    gold_bar_weighing.driver.find_element().click.assert_called()
    gold_bar_weighing.enter_bars_on_bowl.has_calls(
        [call([0, 1, 2], 'left'),
         call([3, 4, 5], 'right')]
    )


