import time
import re

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
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


def write_content(url, data):
    """write job data to file"""
    f = open("job_descriptions_arbeitsagentur.txt",
             "a", encoding='utf-8')
    f.writelines((url + '\n',
                  f"{data[0]}, {data[1]} \n",
                  data[3] + '\n',
                  data[5] + '\n'))
    f.close()


def arbeitsagentur_scraper():
    URL = "https://www.arbeitsagentur.de/jobsuche/suche?angebotsart=1&was=aws%20python"
    with chrome_driver as driver:
        driver.implicitly_wait(5)
        driver.get(URL)
        wait = WebDriverWait(driver, 5)

        # wait until this element is visible
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.liste-container')))

        elem = driver.find_element(By.XPATH,
                                   '/html/body/jb-root/main/jb-jobsuche/jb-jobsuche-suche/div[1]/div/jb-h1zeile/h2')
        print(elem.text)

        # create list of job description urls
        elements = driver.find_elements(By.CLASS_NAME, 'ergebnisliste-item')
        urls = []
        for elem in elements:
            url = elem.get_attribute('href')
            urls.append(url)

        # clean for known urls
        with open(known_URLs.txt, 'r') as known:
            known_URLs = list(known.readlines())

        for i, url in enumerate(urls):
            print("i: ", i)
            print(f"{url}")

            driver.implicitly_wait(5)
            driver.get(url)
            # wait.until(EC.visibility_of_element_located(
            #     (By.CSS_SELECTOR, '.liste-container')))

            # gather information from page
            try:
                IDs = ("jobdetails-hauptberuf",
                       "jobdetails-titel",
                       "jobdetails-veroeffentlichungsdatum",
                       "jobdetails-kopf-arbeitgeber",
                       "jobdetails-arbeitsort",
                       "jobdetails-beschreibung")
                data = [None]*len(IDs)
                for j, id in enumerate(IDs):
                    # print(f"searching {id}")
                    data[j] = wait.until(EC.visibility_of_element_located(
                        (By.ID, id))).text

                # element = driver.find_element(
                #     By.ID, 'jobdetails-beschreibung')
                print("url: ", url)
                for j in range(5):
                    print(f"{IDs[j]}: {data[j]}")

                # print("X: ", data[-1])

                write_content(url, data)
                # res = driver.page_source  # requests.get(URL)
                # soup = BeautifulSoup(res, 'html.parser')
                # print(soup.prettify())
            except TimeoutException:
                print("Element not found on the page")
            # if i > 0:
            #     break


arbeitsagentur_scraper()
