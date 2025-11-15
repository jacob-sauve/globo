# IMPORTS
from time import sleep
from functools import wraps
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from backend.scraper_helpers import find_all
from scraper_helpers import to_xpath, get_driver, find_all
import os



# CONSTANTS
ORIGIN_INPUT_CLASS = "II2One j0Ppje zmMKJ LbIaRd"
SEARCH_RESULTS_DROPDOWN_CLASS = "n4HaVc "
DESTINATION_LIST_XPATH = "//ol[@class='SD4Ugf']"
FLIGHT_PRICE_CLASS = "MJg7fb QB2Jof"
FLIGHT_DURATION_CLASS = "Xq1DAb"
FLIGHT_DESTINATION_CLASS = "xyc80b sSHqwe"
LANGUAGE = "en-US"
INVALID_ORIGIN_ERROR = ValueError("Origin airport code must be 3 letters, e.g.: YYZ, and correspond to a real airport.")
NULL_DRIVER_ERROR = ValueError("Please supply a Selenium driver as 'driver' keyword argument")



# WRAPPER (TO GUARANTEE SELENIUM DRIVER CLEANUP)
def auto_quit_driver(func):
    @wraps(func)
    def wrapper(driver, *args, **kwargs):
        try:
            return func(driver, *args, **kwargs)
        except Exception:
            print("!! An exception occurred !!")
            raise # the same one for debugging
        finally:
            print("Quitting driver...")
            driver.quit()
            print("Successfully quit driver!")
    return wrapper


# SCRAPER
@auto_quit_driver
def scrape(driver=get_driver(), origin_airport=None, budget=None):
    '''
    Writes to results.csv with following columns: Origin, Destination, Price, Date, IMG_URL
    Returns True when done writing.
    '''
    output_dict = dict()

    if driver is None:
        raise NULL_DRIVER_ERROR
    if not (type(origin_airport) is str and len(origin_airport) == 3 and origin_airport.isalpha()):
        print(f"{origin_airport=}")
        raise INVALID_ORIGIN_ERROR
    origin_airport = origin_airport.upper()

    # access URL
    url = f"https://www.google.com/travel/explore?hl={LANGUAGE}"
    driver.get(url)

    # wait until input box loads
    print("Waiting for page to load...")
    point_of_origin_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, to_xpath(ORIGIN_INPUT_CLASS)))
        )
    print("Loaded!")

    # launch search for all outbound flights
    try:
        point_of_origin_input.clear()
        point_of_origin_input.send_keys(origin_airport)
        WebDriverWait(driver, 30).until(
            EC.text_to_be_present_in_element_attribute((By.XPATH, to_xpath(SEARCH_RESULTS_DROPDOWN_CLASS)), "data-code", origin_airport)
        )
        sleep(1)
        driver.find_element(By.XPATH, to_xpath(SEARCH_RESULTS_DROPDOWN_CLASS)).click()
    except:
        raise INVALID_ORIGIN_ERROR

    # collect all possible flights
    flight_list_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, DESTINATION_LIST_XPATH))
    )
    flights = flight_list_element.find_elements(By.TAG_NAME, "li")
    print(len(flights))


    duration = find_all(driver, FLIGHT_DURATION_CLASS)
    print("\n".join(d.text for d in duration))
    print(len(duration))

    prices = find_all(driver, FLIGHT_PRICE_CLASS)
    print("\n".join(p.text for p in prices))
    print(len(prices))

    destinations = find_all(driver, FLIGHT_DESTINATION_CLASS)
    print("\n".join(d.text for d in destinations))
    print(len(destinations))


    # when the last scrape has been scraped...
    # sleep(60)
    # WRITE TO CSV
    return True



# TESTING
if __name__ == "__main__":
    origin_airport = input("Origin airport code: ").strip()
    max_price = int(input("Budget (CAD): "))
    if scrape(get_driver(headless=False),origin_airport=origin_airport, budget=max_price):
        print("Scrape successful!")