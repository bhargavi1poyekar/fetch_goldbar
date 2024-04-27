# web_driver_config.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class WebDriver:

    def __init__(self, headless=True):
        """
        Initializes a WebDriver instance with optional headless mode.

        Args:
            headless (bool): If True, the browser will be run in headless mode.
            Defaults to True.
        """
        options = Options
        if headless:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            self.driver = webdriver.Chrome(options=options)
        else:
            self.driver = webdriver.Chrome()
    
    