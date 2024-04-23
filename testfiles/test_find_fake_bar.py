import pytest
from unittest.mock import MagicMock, patch
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

    fake_bar = gold_bar_weighing.find_fake_bar()
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

    fake_bar = gold_bar_weighing.find_fake_bar()
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

    fake_bar = gold_bar_weighing.find_fake_bar()
    assert fake_bar == 0
