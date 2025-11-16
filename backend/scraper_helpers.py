from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def to_xpath(compoundClass):
    """Packs compound class name into xpath usable by Selenium"""
    return f"//*[@class='{compoundClass}']"


def to_css_selector(compoundClass):
    """Turns compound class name into CSS selector usable by Selenium"""
    classList = compoundClass.split()
    return "." + ".".join(classList)


def get_driver(headless=True):
    """Returns a Selenium webdriver, with headless mode toggled if specified"""
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


def find_all(driver, compoundClass):
    """Increases reliability by ensuring elements loaded in before parsing DOM"""
    xpath = to_xpath(compoundClass)
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath))
    )
    results = driver.find_elements(By.XPATH, xpath)
    return results
