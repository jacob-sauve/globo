from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep



def to_xpath(compoundClass):
    '''Packs compound class name into xpath usable by Selenium'''
    return f"//*[@class='{compoundClass}']"


def to_css_selector(compoundClass):
    '''Turns compound class name into CSS selector usable by Selenium'''
    classList = compoundClass.split()
    return "." + ".".join(classList)


def get_driver(headless=True):
    '''Returns a Selenium webdriver, with headless mode toggled if specified'''
    options = Options()
    # !!
    # only activate headless (no view of bot's actions) when everything works
    # !!
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, \
    like Gecko) Firefox/91.0 Safari/537.36"
    )
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(options=options)
    return driver


# def find_nested(driver, successive_class_list):
#     '''Get element nested within elements of successive classes those in the provided list'''
#     # if the list is empty
#     if not successive_class_list:
#         return [driver]
#
#     c = successive_class_list[0]
#     output = []
#
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_all_elements_located((By.XPATH, "." + to_xpath(c)))
#     )
#     elements = driver.find_elements(By.XPATH, "." + to_xpath(c))
#
#     for match in elements:
#         next_layer = find_nested(match, successive_class_list[1:])
#         output.extend(next_layer)
#
#     return output