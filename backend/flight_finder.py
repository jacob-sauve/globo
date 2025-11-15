from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from scraper_helpers import to_xpath
from bs4 import BeautifulSoup
import time as t
import os

# CONSTANTS
ORIGIN_INPUT_CLASS = "II2One j0Ppje zmMKJ LbIaRd"
RESULTS_BOX_TEXT = "min"


# setup Selenium agent
options = Options()
# activate headless (no view of bot's actions) when everything works
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

# wait until results load + catch them
print("Waiting for results to load...")
destinations = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, to_xpath(ORIGIN_INPUT_CLASS)))
    )

print(f"{driver.page_source=}")

html = driver.page_source
