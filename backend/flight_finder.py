# IMPORTS
from time import sleep
from functools import wraps
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from scraper_helpers import to_xpath, get_driver, find_all
import re



# CONSTANTS
ORIGIN_INPUT_CLASS = "II2One j0Ppje zmMKJ LbIaRd"
SEARCH_RESULTS_DROPDOWN_CLASS = "n4HaVc "
DESTINATION_LIST_XPATH = "//ol[@class='SD4Ugf']"
FLIGHT_PRICE_CLASS = "MJg7fb QB2Jof"
FLIGHT_DURATION_CLASS = "Xq1DAb"
FLIGHT_DATE_CLASS = "xyc80b sSHqwe"
FLIGHT_DESTINATION_CLASS = "W6bZuc YMlIz"
DESTINATION_IMAGE_CLASS = "EWmqCb "
ORDERED_CSV_HEADERS = [
    "Price",
    "Destination",
    "Date",
    "Duration",
    "Origin",
    "IMG URL",
]
ORDERED_CSV_HEADER_CLASSES = [
    FLIGHT_PRICE_CLASS,
    FLIGHT_DESTINATION_CLASS,
    FLIGHT_DATE_CLASS,
    FLIGHT_DURATION_CLASS,
]
LANGUAGE = "en-US"
INVALID_ORIGIN_ERROR = ValueError("Origin airport code must be 3 letters, e.g.: YYZ, and correspond to a real airport.")
NULL_DRIVER_ERROR = ValueError("Please supply a Selenium driver as 'driver' keyword argument")



# WRAPPER (TO GUARANTEE SELENIUM DRIVER CLEANUP)
def auto_quit_driver(func):
    """Wrapper to guarantee that the Selenium driver quits post-use"""
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
    """
    Writes to results.csv with following columns: Price, Destination, Date, Duration, Origin, IMG_URL
    Returns True when done writing.
    """
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

    # get each data point in order:
    data = list()
    for column_class in ORDERED_CSV_HEADER_CLASSES:
        elements = find_all(driver, column_class)
        vals = [e.text for e in elements] # to prevent stale reference
        data.append(vals)

    # add origin airport (always same)
    data.append([origin_airport] * len(data[0]))

    # specific case - image URLs
    elements = find_all(driver, DESTINATION_IMAGE_CLASS)
    # clean up URL fetched from style attribute
    vals = [e.get_attribute("style") for e in elements]
    data.append([re.sub(r"(background-image:url\\\('|,url\('\/\/.*?'\))$", "", v) for v in vals])


    values = zip(*data)

    print("values:\n"+"\n".join(str(v) for v in values))

    # filter according to budget if valid one provided
    if type(budget) is int and budget > 0:
        values = filter(lambda v: int(re.sub(r"\D", "", v[0])) <= budget, values)

    print("filtered values:\n"+"\n".join(str(v) for v in list(values)))

    # csv entries
    entries = [dict(zip(ORDERED_CSV_HEADERS, v)) for v in values]
    print(entries)

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