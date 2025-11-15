# IMPORTS
from sys import orig_argv
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from scraper_helpers import to_xpath
from bs4 import BeautifulSoup
import os

# CONSTANTS
ORIGIN_INPUT_CLASS = "II2One j0Ppje zmMKJ LbIaRd"
SEARCH_RESULTS_DROPDOWN_CLASS = "n4HaVc "
INVALID_ORIGIN_ERROR = ValueError("Origin airport code must be 3 letters, e.g.: YYZ, and correspond to a real airport.")

# SCRAPER
def scrape(origin_airport):
    if not (len(origin_airport) == 3 and origin_airport.isalpha()):
        raise INVALID_ORIGIN_ERROR
    origin_airport = origin_airport.upper()

    # setup Selenium agent
    options = Options()
    # !!
    # only activate headless (no view of bot's actions) when everything works
    # !!
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, \
    like Gecko) Firefox/91.0 Safari/537.36"
        )

    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(options=options)

    # access URL
    url = "https://www.google.com/travel/explore"
    driver.get(url)

    # wait until input box loads
    print("Waiting for results to load...")
    point_of_origin_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, to_xpath(ORIGIN_INPUT_CLASS)))
        )
    print("Loaded!")

    # HTML beautification
    html = driver.page_source
    ma_soupe = BeautifulSoup(html, "html.parser")

    # search
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

    # when the last scrape has been scraped...
    sleep(30)
    driver.quit()
    return

# TESTING
if __name__ == "__main__":
    origin_airport = input("Origin airport code: ")
    scrape(origin_airport)