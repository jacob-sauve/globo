# IMPORTS
from time import sleep
from functools import wraps
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from scraper_helpers import to_xpath, get_driver
import os



# CONSTANTS
ORIGIN_INPUT_CLASS = "II2One j0Ppje zmMKJ LbIaRd"
FILTER_MENU_CLASS = "VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-Bz112c-M1Soyc VfPpkd-LgbsSe-OWXEXe-dgl2Hf ksBjEc lKxP2d LQeN7 bRx3h x4Vnpe yJQRU sIWnMc hNyRxf cd29Sd"
PRICE_SLIDER_CLASS = "undefined Cs7q4e UlwoYd VfPpkd-SxecR VfPpkd-SxecR-OWXEXe-ALTDOd"
SEARCH_RESULTS_DROPDOWN_CLASS = "n4HaVc "
LANGUAGE_BUTTON_CLASS = "VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-INsAgc VfPpkd-LgbsSe-OWXEXe-Bz112c-M1Soyc VfPpkd-LgbsSe-OWXEXe-dgl2Hf Rj2Mlf OLiIxf PDpWxe LQeN7 my6Xrf wJjnG dA7Fcf CapH0e"
EN_US_XPATH = "//input[@value='en-GB']"
LANGUAGE_OK_BUTTON_CLASS = "VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-dgl2Hf ksBjEc lKxP2d LQeN7 bRx3h yJQRU sIWnMc"
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
    if driver is None:
        raise NULL_DRIVER_ERROR
    if not (type(origin_airport) is str and len(origin_airport) == 3 and origin_airport.isalpha()):
        print(f"{origin_airport=}")
        raise INVALID_ORIGIN_ERROR
    origin_airport = origin_airport.upper()

    # access URL
    url = "https://www.google.com/travel/explore"
    driver.get(url)

    # wait until input box loads
    print("Waiting for page to load...")
    point_of_origin_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, to_xpath(ORIGIN_INPUT_CLASS)))
        )
    print("Loaded!")

    # HTML beautification
    html = driver.page_source

    # switch language to English
    language_toggle = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, to_xpath(LANGUAGE_BUTTON_CLASS)))
    )
    language_toggle.click()
    sleep(1)
    en_us = driver.find_element(By.XPATH, EN_US_XPATH)
    en_us.click()
    sleep(1)
    ok_button = driver.find_element(By.XPATH, to_xpath(LANGUAGE_OK_BUTTON_CLASS))
    ok_button.click()

    # get all outbound flights
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

    # sort by price
    if type(budget) is int and budget > 0:
        sleep(3)


        # filter_menu = WebDriverWait(driver, 30).until(
        #     EC.presence_of_element_located((By.XPATH, to_xpath(FILTER_MENU_CLASS)))
        # )
        # filter_menu.click()
        # price_slider = WebDriverWait(driver, 30).until(
        #     EC.presence_of_element_located((By.XPATH, to_xpath(PRICE_SLIDER_CLASS)))
        # )
        while True:
            # price_slider.click()
            sleep(1)

    # when the last scrape has been scraped...
    # sleep(60)
    return True



# TESTING
if __name__ == "__main__":
    origin_airport = input("Origin airport code: ")
    max_price = int(input("Budget (CAD): "))
    if scrape(get_driver(headless=False),origin_airport=origin_airport, budget=max_price):
        print("Scrape successful!")