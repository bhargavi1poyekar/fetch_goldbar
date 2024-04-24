# main.py

from app.goldbar import GoldBarWeighing
import json
from app.web_driver_config import WebDriver

with open("config.json", "r") as config_file:
    config = json.load(config_file)

if __name__ == "__main__":

    driver_obj = WebDriver(headless=config['isheadless']) 

    # Context Management
    with GoldBarWeighing(driver_obj.driver) as gb:
        gb.driver.get(config['url'])
        gb.reset()
        fake_bar = gb.find_fake_bar(
            left=config['left_bar'], 
            right=config['right_bar'], 
            remaining=config['remaining'])
        print(f"\nFake bar is: {fake_bar}")
        gb.validate_answer(fake_bar)
        gb.print_weighings_list()
    