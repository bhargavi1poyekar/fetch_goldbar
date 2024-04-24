# goldbar.py

from typing import List
from web_driver_utilities import WebDriverUtility
from logger import setup_logger


class GoldBarWeighing:

    def __init__(self, driver) -> None:
        """
        Initializes the Chromedriver, WebDriver Object and Logger.
        """
        self.driver = driver
        self.webutils = WebDriverUtility(driver)
        self.logger = setup_logger()

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
        self.webutils.click_button_by_css("button#reset.button:not([disabled])")

    def enter_bars_on_bowl(self, bars: List[int], bowl_side: str) -> None:
        """
        Enter bar numbers in left or right bowl grid.

        Args:
        bars (List[int]): List of bar indices.
        bowl_side (str): 'left' or 'right' to determine the bowl.
        """

        for i, bar in enumerate(bars):
            try:
                # Set the bowl grids values as given argument
                self.webutils.set_text(f"{bowl_side}_{i}", str(bar))
            except Exception as e:
                self.logger.error(f"Some error occurred. {e}")

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
            self.webutils.click_button_by_id("weigh")

            # Wait for the 'reset' (result) to be enabled with the result text
            self.webutils.wait_for_element('reset', ['<', '>', '='])

            # Get the text of the element with id = 'reset'
            result = self.webutils.get_text("reset")
            self.reset()  # Reset the bowls
            return result
        except Exception as e:
            self.logger.error(f"Some Error occurred. {e}")
            raise

    def find_suspected_bars(self,
                            left: List[int],
                            right: List[int],
                            remaining: List[int],
                            result: str) -> List[int]:
        """
        Determine the possible fake bars that might be fake based on the weighing result.

        Args:
        left (List[int]): Bars on the left side of the scale during the last weigh.
        right (List[int]): Bars on the right side of the scale during the last weigh.
        remaining (List[int]): Bars that have not been weighed.
        result (str): The result of the last weigh, '<', '>', or '='.

        Returns:
        List[int]: List of suspected fake bars.
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
            self.logger.error(f"Some Error occurred: {e}")
            raise

    @staticmethod
    def valid_bar_values(left_bars: List[int], right_bars: List[int], remaining: List[int]) -> bool:

        """
        Validates the values of the bars. Checks 3 conditions, length of all bars should be 3,
        All the values should be unique and between the range 0-9

        Args:
        left (List[int]): Bars on the left side of the scale.
        right (List[int]): Bars on the right side of the scale.
        remaining (List[int]): Bars that will not be weighed.

        Returns:
        bool: Returns if the bar values are valid or not.
        """

        if len(left_bars) != 3 or len(right_bars) != 3 or len(remaining) != 3:
            return False

        all_bars = left_bars + right_bars + remaining
        if len(set(all_bars)) == 9 and all(0 <= bar <= 8 for bar in all_bars):
            return True
        return False

    def find_fake_bar(self, left: List[int], right: List[int], remaining: List[int]) -> int:

        """
        Find the fake bar by performing a series of weightings.

        Args:
        left (List[int]): Bars on the left side of the scale.
        right (List[int]): Bars on the right side of the scale.
        remaining (List[int]): Bars that will not be weighed.

        Returns:
        int: The index of the suspected fake bar.
        """

        try:
            if not self.valid_bar_values(left, right, remaining):
                raise ValueError("The values in all the bars are not correct. "
                                 "Enter 3 unique values in each bar from 0-8")

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
            self.logger.error(f"Some error occurred while finding the fake bar: {e}")
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
            # self.driver.find_element(By.ID, f"coin_{fake_bar}").click()
            self.webutils.click_button_by_id(f"coin_{fake_bar}")

            # Get th text in alert pop up
            alert_text = self.webutils.get_alert_text()
            print(f"\nAlert: {alert_text}")

            # Accept the alert
            self.webutils.accept_alert()

            # Check if correct bar found
            found_bar = True
            if alert_text != "Yay! You find it!":
                found_bar = False
            return found_bar
        except Exception as e:
            self.logger.error(f"Some error occurred :{e}")

    def print_weighings_list(self) -> None:
        """
        Print the list of weightings performed.
        """
        try:
            # Print the weightings performed
            weighings_list = self.webutils.get_elements_by_css("div.game-info ol li")
            print("\nWeightings list: ")
            for item in weighings_list:
                print(item.text)
        except Exception as e:
            self.logger.error(f"Some error occurred :{e}")
