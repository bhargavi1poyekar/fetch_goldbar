from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from typing import List
from selenium.webdriver.chrome.options import Options
import logging
import json



class WebDriver:

    def __init__(self, headless=True):
        options = Options
        if headless:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=options)
    
    