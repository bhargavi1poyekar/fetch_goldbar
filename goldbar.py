from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from typing import List
from selenium.webdriver.chrome.options import Options
import logging


# Define Log to store the errors
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename="goldbar.log",
    filemode='a'
    )


class GoldBarWeighing:

    def __init__(self) -> None:
        """
        Initializes the Chromedriver
        """
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options)
        self.driver.get("http://sdetchallenge.fetch.com/")
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exits the chrome testing mode
        """
        self.driver.quit()
    
    def reset(self):
        """
        Resets the bowl grids
        """
        self.driver.find_element(By.CSS_SELECTOR, "button#reset.button:not([disabled])").click()

    def enter_bars_on_bowl(self, bars: List[int], bowl_side: str) -> None:
        """
        Enter bar numbers in left or right bowl grid.

        Args:
        bars (List[int]): List of bar indices.
        bowl_side (str): 'left' or 'right' to determine the bowl.
        """

        for i, bar in enumerate(bars):
            try:
                # Bar numbers are only from 0-8
                if bar not in range(0, 9):
                    raise ValueError("Input should be within range of 0 to 8")

                # Set the bowl grids values as given argument
                self.driver.find_element(By.ID, f"{bowl_side}_{i}").send_keys(str(bar))
            except NoSuchElementException:
                logging.error(f"Element {bowl_side}_{i} not found.")
                raise
            except ValueError:
                logging.error(f"Invalid bar number")
                raise
            except Exception as e:
                logging.error(f"Some error occurred. {e}")

    def weigh(self, bars_left: List[int], bars_right: List[int]) -> str:
        """
        Compare the weights of the left and right bars and return the result.

        Args:
        bars_left (List[int]): List of bar indices on the left side.
        bars_right (List[int]): List of bar indices on the right side.

        Returns:
        str: The result of the weighing, '<', '>', or '='.
        """

        # Set the left and right bowls
        self.enter_bars_on_bowl(bars_left, 'left')
        self.enter_bars_on_bowl(bars_right, 'right')

        try:
            # Click the weigh button, to compare the weights on both side
            self.driver.find_element(By.ID, "weigh").click()

            # Wait for the 'reset' (result) to be enabled with the result text
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.find_element(By.ID, "reset").text in ["<", ">", "="]
            )

            # Get the text of the element with id = 'reset'
            result = self.driver.find_element(By.ID, "reset").text
            self.reset()  # Reset the bowls
            return result

        # If WebDriverWait times out
        except TimeoutException:
            logging.error(f"Weighing operation timed out or the result element did not "
                          f"contain the expected value.")
            raise
        except NoSuchElementException:
            logging.error(f"Requested Element not found.")
            raise
        except Exception as e:
            logging.error(f"Some Error occurred. {e}")
            raise

    @staticmethod
    def find_suspected_bars(left: List[int],
                            right: List[int],
                            remaining: List[int],
                            result: str) -> List[int]:
        """
        Determine the possible fake bars that might be fake based on the weighing result.

        Args:
        left (List[int]/int): Bars on the left side of the scale during the last weigh.
        right (List[int]/int): Bars on the right side of the scale during the last weigh.
        remaining (List[int]/int): Bars that have not been weighed.
        result (str): The result of the last weigh, '<', '>', or '='.

        Returns:
        List[int]/int: List of suspected fake bars.
        """
        try:
            if result == "<":
                possible_fake = left
            elif result == '>':
                possible_fake = right
            elif result == "=":
                possible_fake = remaining
            else:
                raise ValueError("Unexpected Result")
            return possible_fake
        except Exception as e:
            logging.error(f"Some Error occurred: {e}")
            raise

    def find_fake_bar(self) -> int:

        """
        Find the fake bar by performing a series of weightings.

        Returns:
        int: The index of the suspected fake bar.
        """
        
        try:
            left = [0, 1, 2]
            right = [3, 4, 5]
            remaining = [6, 7, 8]

            # First weighing
            result = self.weigh(left, right)
            possible_fake_bar = self.find_suspected_bars(left, right, remaining, result)

            # Second weighing
            result = self.weigh([possible_fake_bar[0]], [possible_fake_bar[1]])
            fake_bar = self.find_suspected_bars(
                [possible_fake_bar[0]],
                [possible_fake_bar[1]],
                [possible_fake_bar[2]],
                result
            )

            return fake_bar[0]
        except Exception as e:
            logging.error(f"Some error occurred while finding the fake bar: {e}")
            raise

    def validate_answer(self, fake_bar: int) -> bool:

        """
        Validate if the identified bar is actually the fake one.

        Args:
        fake_bar (int): The index of the suspected fake bar to validate.

        Returns:
        bool: True if the identified bar is the fake one, otherwise False.
        """

        try:
            # Click the fake bar button
            self.driver.find_element(By.ID, f"coin_{fake_bar}").click()

            # Get th text in alert pop up
            alert_text = self.driver.switch_to.alert.text
            print(f"\nAlert: {alert_text}")

            # Accept the alert
            self.driver.switch_to.alert.accept()

            # Check if correct bar found
            found_bar = True 
            if alert_text != "Yay! You find it!":
                found_bar = False
            return found_bar
        except NoSuchElementException:
            logging.error(f"Failed to find the coin button for bar {fake_bar}.")
            raise
        except Exception as e:
            logging.error(f"Some error occurred :{e}")

    def print_weighings_list(self) -> None:
        """
        Print the list of weightings performed.
        """
        try:
            # Print the weightings performed
            weighings_list = self.driver.find_elements(By.CSS_SELECTOR, "div.game-info ol li")
            print("\nWeightings list: ")
            for item in weighings_list:
                print(item.text)
        except NoSuchElementException:
            logging.error("Failed to find weighing list elements")
            raise
        except Exception as e:
            logging.error(f"Some error occurred :{e}")
