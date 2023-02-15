import time

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests

options = webdriver.ChromeOptions()

# options.add_argument("--headless")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-gpu")
# options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-extensions")

chrome_driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)


def write_content(URL):
    # URL = "https://www.arbeitsagentur.de/jobsuche/jobdetail/12288-2839234052-S"
    with chrome_driver as driver:
        driver.implicitly_wait(15)
        driver.get(URL)
        # wait = WebDriverWait(driver, 10)
        # wait.until(EC.visibility_of_element_located(
        #     (By.CSS_SELECTOR, '.liste-container')))
        # element = driver.find_element(By.ID, 'jobdetails-beschreibung')
        # text = element.text
        # print(text)


def arbeitsagentur_scraper():
    URL = "https://www.arbeitsagentur.de/jobsuche/suche?angebotsart=1&was=aws%20python"
    with chrome_driver as driver:
        driver.implicitly_wait(15)
        driver.get(URL)
        wait = WebDriverWait(driver, 10)

        # wait until this element is visible
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.liste-container')))

        elem = driver.find_element(By.XPATH,
                                   '/html/body/jb-root/main/jb-jobsuche/jb-jobsuche-suche/div[1]/div/jb-h1zeile/h2')
        print(elem.text)
        # res = driver.page_source  # requests.get(URL)
        # soup = BeautifulSoup(res, 'html.parser')
        # print(soup.prettify())
        # user_message = chrome_browser.find_element(By.ID, 'user-message')
        elements = driver.find_elements(By.CLASS_NAME, 'ergebnisliste-item')
        # urls = []

        for i, elem in enumerate(elements):
            print("i: ", i)
            url = elem.get_attribute('href')
            description = elem.get_attribute('aria-label')
            # urls.append(url)
            print(f"{url}")
            # time.sleep(1)
            # wait until this element is visible'
            if i > 0:
                driver.implicitly_wait(15)
                driver.get(url)
                # wait.until(EC.visibility_of_element_located(
                #     (By.CSS_SELECTOR, '.liste-container')))
                # wait.until(EC.visibility_of_element_located(
                #     (By.ID, "jobdetails-beschreibung")))
                wait = WebDriverWait(driver, 10)
                element = wait.until(EC.visibility_of_element_located(
                    (By.ID, "jobdetails-beschreibung")))
                element = driver.find_element(By.ID, 'jobdetails-beschreibung')
                # element = wait.until(EC.visibility_of_element_located(
                #     (By.ID, "jobdetails-beschreibung")))
                print(element)
        # write_content(url)
        # if i > 0:
        #     break
        # URL2 = "https://www.arbeitsagentur.de/jobsuche/jobdetail/12288-2839234052-S"
        # URL2 = "https://www.arbeitsagentur.de/jobsuche/jobdetail/12265-260461_JB3578034-S"
        # https://www.arbeitsagentur.de/jobsuche/jobdetail/10000-1193203999-S
        # https://www.arbeitsagentur.de/jobsuche/jobdetail/12456-890003-1-S

        # wait until this element is visible
        # wait.until(EC.visibility_of_element_located(
        #     (By.CSS_SELECTOR, '.liste-container')))


arbeitsagentur_scraper()
# write_content()
