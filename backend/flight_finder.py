from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time as t
import os

# CONSTANTS
DESTINATION_BOX_CLASS = "tsAU4e "



options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, \
like Gecko) Firefox/91.0 Safari/537.36"
    )

service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(options=options)

url = "https://www.google.com/travel/explore"
driver.get(url)

# wait until results load + catch them
destinations = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, DESTINATION_BOX_CLASS))
    )

print(driver.page_source)