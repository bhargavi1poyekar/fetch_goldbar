import pytest
from unittest.mock import MagicMock, patch
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from ..app import WebDriverUtility  
from selenium.webdriver.common.by import By


@pytest.fixture
def web_driver_utility():
    with patch('selenium.webdriver.Chrome') as MockWebDriver:
        driver = MockWebDriver()
        return WebDriverUtility(driver)


def test_click_button_by_id_success(web_driver_utility):
    """Test clicking a button by ID successfully."""
    mock_button = MagicMock()
    web_driver_utility.driver.find_element.return_value = mock_button

    web_driver_utility.click_button_by_id("test-button")

    web_driver_utility.driver.find_element.assert_called_once_with("id", "test-button")
    mock_button.click.assert_called_once()


def test_click_button_by_id_not_found(web_driver_utility):
    """Test clicking a button by ID where the button is not found."""
    web_driver_utility.driver.find_element.side_effect = NoSuchElementException()

    with pytest.raises(NoSuchElementException):
        web_driver_utility.click_button_by_id("nonexistent-button")


def test_set_text_success(web_driver_utility):
    """Test setting text in an input field."""
    mock_input = MagicMock()
    web_driver_utility.driver.find_element.return_value = mock_input

    web_driver_utility.set_text("input-field", "Hello, World!")

    web_driver_utility.driver.find_element.assert_called_once_with("id", "input-field")
    mock_input.send_keys.assert_called_once_with("Hello, World!")


def test_set_text_not_found(web_driver_utility):
    """Test setting text where the input field is not found."""
    web_driver_utility.driver.find_element.side_effect = NoSuchElementException()

    with pytest.raises(NoSuchElementException):
        web_driver_utility.set_text("nonexistent-field", "Hello, World!")


def test_get_text_success(web_driver_utility):
    """Test retrieving text from an element."""
    mock_element = MagicMock()
    mock_element.text = "Expected Text"
    web_driver_utility.driver.find_element.return_value = mock_element

    result = web_driver_utility.get_text("text-element")

    assert result == "Expected Text"
    web_driver_utility.driver.find_element.assert_called_once_with("id", "text-element")


def test_get_text_not_found(web_driver_utility):
    """Test retrieving text where the element is not found."""
    web_driver_utility.driver.find_element.side_effect = NoSuchElementException()

    with pytest.raises(NoSuchElementException):
        web_driver_utility.get_text("nonexistent-element")


def test_wait_for_element_timeout(web_driver_utility):
    """Test waiting for an element where the element does not meet expected conditions."""
    web_driver_utility.driver.find_element.side_effect = TimeoutException()

    with pytest.raises(TimeoutException):
        web_driver_utility.wait_for_element("wait-element", ["valid", "values"])


def test_accept_alert(web_driver_utility):
    """
    Test accepting an active alert.
    """
    # Set up a mock alert object
    mock_alert = MagicMock()
    web_driver_utility.driver.switch_to.alert = mock_alert

    web_driver_utility.accept_alert()

    # Assert the accept method on the alert was called
    mock_alert.accept.assert_called_once()


def test_get_alert_text(web_driver_utility):
    """
    Test retrieving text from an active alert.
    """
    # Set up a mock alert with expected text
    expected_text = "Alert text"
    mock_alert = MagicMock()
    mock_alert.text = expected_text
    web_driver_utility.driver.switch_to.alert = mock_alert

    result = web_driver_utility.get_alert_text()

    # Check that the text returned is what was set on the mock alert
    assert result == expected_text


def test_get_elements_by_css_success(web_driver_utility):
    """
    Test retrieving a list of elements based on a CSS selector successfully.
    """
    # Create a list of mock elements to return
    mock_elements = [MagicMock(), MagicMock()]
    web_driver_utility.driver.find_elements.return_value = mock_elements

    elements = web_driver_utility.get_elements_by_css(".test-class")

    # Assert that the correct method was called and the correct elements returned
    web_driver_utility.driver.find_elements.assert_called_once_with(By.CSS_SELECTOR, ".test-class")
    assert elements == mock_elements


def test_get_elements_by_css_not_found(web_driver_utility):
    """
    Test retrieving a list of elements where no elements are found.
    """
    web_driver_utility.driver.find_elements.side_effect = NoSuchElementException()

    with pytest.raises(NoSuchElementException):
        web_driver_utility.get_elements_by_css(".nonexistent-class")
