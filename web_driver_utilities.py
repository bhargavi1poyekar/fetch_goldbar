from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from typing import List
from selenium.webdriver.chrome.options import Options
import logging
import json


class WebDriverUtility:

    def __init__(self, driver):
        self.driver = driver
    
    def click_button_by_id(self, selector):
        try:
            button = self.driver.find_element(By.ID, selector)
            button.click()
        except NoSuchElementException:
            print(f"Button with selector {selector} not found")
            raise
    
    def click_button_by_css(self, selector):
        try:
            button = self.driver.find_element(By.CSS_SELECTOR, selector)
            button.click()
        except NoSuchElementException:
            print(f"Button with selector {selector} not found")
            raise
    
    def set_text(self, selector, text_string):
        try:
            grid = self.driver.find_element(By.ID, selector)
            grid.send_keys(text_string)
        except NoSuchElementException:
            print(f"Grid with selector {selector} not found")
            raise
    
    def get_text(self, selector):
        try:
            element = self.driver.find_element(By.ID, selector)
            return element.text
        except NoSuchElementException:
            print(f"Element with selector {selector} not found")
            raise
    
    def wait_for_element(self, selector, results):
        try:   
            WebDriverWait(self.driver, 10).until(
                    lambda driver: driver.find_element(By.ID, selector).text in results
                )
        except TimeoutException:
            print(f"Weighing operation timed out or the result element did not "
                          f"contain the expected value.")
            raise

    def get_alert_text(self):

        alert = self.driver.switch_to.alert
        return alert.text
    
    def accept_alert(self):

        self.driver.switch_to.alert.accept()

    def get_elements_by_css(self, selector):
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            return elements
        except NoSuchElementException:
            print(f"Element with selector {selector} not found")
            raise
    