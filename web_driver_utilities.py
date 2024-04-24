from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import List


class WebDriverUtility:

    def __init__(self, driver: WebDriver):
        """
        Initializes the WebDriverUtility class with a Selenium WebDriver.
        Args:
        driver (WebDriver): The Selenium WebDriver to use for browser interactions.
        """
        self.driver = driver

    def click_button_by_id(self, selector: str) -> None:
        """
        Clicks a button based on its ID.

        Args:
        selector (str): The ID of the button to click.

        Raises:
        NoSuchElementException: If the button cannot be found.
        """
        try:
            button = self.driver.find_element(By.ID, selector)
            button.click()
        except NoSuchElementException:
            print(f"Button with selector {selector} not found")
            raise

    def click_button_by_css(self, selector: str) -> None:
        """
        Clicks a button based on a CSS selector.

        Args:
        selector (str): The CSS selector of the button to click.

        Raises:
        NoSuchElementException: If the button cannot be found.
        """
        try:
            button = self.driver.find_element(By.CSS_SELECTOR, selector)
            button.click()
        except NoSuchElementException:
            print(f"Button with selector {selector} not found")
            raise

    def set_text(self, selector: str, text_string: str) -> None:
        """
        Sets text in an input field identified by an ID.

        Args:
        selector (str): The ID of the input field.
        text_string (str): The text to set in the input field.

        Raises:
        NoSuchElementException: If the input field cannot be found.
        """
        try:
            grid = self.driver.find_element(By.ID, selector)
            grid.send_keys(text_string)
        except NoSuchElementException:
            print(f"Grid with selector {selector} not found")
            raise

    def get_text(self, selector: str) -> str:
        """
        Retrieves text from an element identified by an ID.

        Args:
        selector (str): The ID of the element.

        Returns:
        str: The text of the element.

        Raises:
        NoSuchElementException: If the element cannot be found.
        """
        try:
            element = self.driver.find_element(By.ID, selector)
            return element.text
        except NoSuchElementException:
            print(f"Element with selector {selector} not found")
            raise

    def wait_for_element(self, selector: str, results: List[str]) -> None:
        """
        Waits for an element's text to match one of the specified results.

        Args:
        selector(str): The ID of the element to monitor.
        results(List[str]): The acceptable values of the element's text.

        Raises:
        If the text of the element does not match the expected results within the timeout.
        """
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.find_element(By.ID, selector).text in results
            )
        except TimeoutException:
            print(f"Weighing operation timed out or the result element did not "
                  f"contain the expected value.")
            raise

    def get_alert_text(self) -> str:
        """
        Retrieves the text from an active alert.

        Returns:
        str: The text from the alert.
        """
        alert = self.driver.switch_to.alert
        return alert.text

    def accept_alert(self) -> None:
        """
        Accepts the currently active alert.
        """
        self.driver.switch_to.alert.accept()

    def get_elements_by_css(self, selector: str) -> List[WebElement]:
        """
        Retrieves a list of elements based on a CSS selector.

        Args:
        selector (str): The CSS selector of the elements to retrieve.

        Returns:
        List[WebElement]: A list of WebElements found.

        Raises:
        NoSuchElementException: If no elements can be found.
        """
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            return elements
        except NoSuchElementException:
            print(f"Elements with selector {selector} not found")
            raise
