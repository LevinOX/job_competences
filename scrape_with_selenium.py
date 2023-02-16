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
import csv
import requests

options = webdriver.ChromeOptions()
wait_seconds = 20
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
        driver.implicitly_wait(wait_seconds)
        driver.get(URL)
        wait = WebDriverWait(driver, wait_seconds)

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
        with open('known_URLs.txt', 'r') as known:
            known_URLs = [line.strip() for line in known]
        with open('bad_URLs.txt', 'r') as bad:
            bad_URLs = [line.strip() for line in bad]

        print("known_URLs: ", known_URLs)
        print("bad_URLs: ", bad_URLs)
        urls = [item for item in urls if item not in known_URLs or item not in bad_URLs]

        for i, url in enumerate(urls):
            print("i: ", i)
            print(f"{url}")

            driver.implicitly_wait(wait_seconds)
            driver.get(url)
            driver.execute_script("window.scrollBy(0, 500)")

            logo_xpath = '//div[@class="ba-logo"]/a'
            # logo_xpath = 'jobdetails-hauptberuf'
            logo_element = wait.until(EC.visibility_of_element_located(
                (By.XPATH, logo_xpath)))
            # driver.find_element(By.XPATH, logo_xpath)
            logo_title = logo_element.get_attribute('title')
            print(logo_title)

            # <button class="ba-btn ba-btn-contrast" aria-label="Auswahl bestätigen – Ausgewählte Cookies werden akzeptiert"><bahf-i18n class="hydrated">Auswahl bestätigen</bahf-i18n></button>
            # button = wait.until(EC.presence_of_element_located(
            #     (By.XPATH, "ba-btn ba-btn-contrast")))
            # button.click()

            break
            # gather information from page
            try:

                if wait.until(EC.presence_of_element_located(
                        (By.CLASS_NAME, "externe-Beschreibung"))):
                    print("extern job ad.")
                    raise TimeoutException

                IDs = ("jobdetails-hauptberuf",
                       "jobdetails-titel",
                       "jobdetails-veroeffentlichungsdatum",
                       "jobdetails-kopf-arbeitgeber",
                       "jobdetails-arbeitsort",
                       "jobdetails-beschreibung")
                data = [None]*len(IDs)
                for j, id in enumerate(IDs):
                    data[j] = wait.until(EC.presence_of_element_located(
                        (By.ID, id))).text

                write_content(url, data)
                with open('known_URLs.txt', 'a') as known:
                    print(url, file=known)

            except TimeoutException:
                print("Element not found on the page")
                # add url to known urls
                with open('bad_URLs.txt', 'a') as bad:
                    print(url, file=bad)
            if i > 4:
                break


arbeitsagentur_scraper()
