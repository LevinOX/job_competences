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
wait_seconds = 5
# options.add_argument("--headless")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-gpu")
# options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-extensions")

chrome_driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)


def read_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]


def write_file(file_path, data, mode):
    with open(file_path, mode, encoding='utf-8') as file:
        file.write(data)


def write_content(url, data):
    """write job data to file"""
    f = open("job_descriptions_arbeitsagentur.txt",
             "a", encoding='utf-8')
    f.writelines((url + '\n',
                  f"{data[0]}, {data[1]} \n",
                  data[3] + '\n',
                  data[5].strip() + '\n'))
    f.close()


def store_url(url):
    with open('known_URLs.txt', 'a') as known:
        print(url, file=known)


def get_ad_number(wait, driver):
    # wait until this element is visible
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '.liste-container')))
    elem = driver.find_element(By.XPATH,
                               '/html/body/jb-root/main/jb-jobsuche/jb-jobsuche-suche/div[1]/div/jb-h1zeile/h2')


def create_url_list(driver):
    elements = driver.find_elements(By.CLASS_NAME, 'ergebnisliste-item')
    urls = []
    for elem in elements:
        url = elem.get_attribute('href')
        urls.append(url)
    return urls


def clean_urls(urls):
    known_URLs = read_file('known_URLs.txt')
    bad_URLs = read_file('bad_URLs.txt')
    clean_urls = [
        item for item in urls if item not in known_URLs and item not in bad_URLs]
    return clean_urls


def scrape_selenium(wait, IDs, url, data):
    # in case it's not on the page, but external
    if wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "externe-Beschreibung"))):
        print("extern job ad.")
        raise TimeoutException

    # requesting the data via Selenium, waiting a bit
    for j, id in enumerate(IDs):
        data[j] = wait.until(EC.visibility_of_element_located(
            (By.ID, id))).text
    return data


def scrape_beautiful_soup(html, IDs, url, data):
    soup = BeautifulSoup(html, 'html.parser')
    # find the requested elements like job title, company name, etc
    for j, id in enumerate(IDs):
        element = soup.find(id=id)
        data[j] = element.text
    return data


def arbeitsagentur_scraper():
    """docstring"""
    URL = "https://www.arbeitsagentur.de/jobsuche/suche?angebotsart=1&was=aws%20python"
    with chrome_driver as driver:
        driver.implicitly_wait(wait_seconds)
        driver.get(URL)
        wait = WebDriverWait(driver, wait_seconds)

        # get number of ads
        print(get_ad_number(wait, driver))

        # create list of job description urls
        urls = create_url_list(driver)

        # clean for known urls
        urls = clean_urls(urls)

        for i, url in enumerate(urls):
            print("i: ", i)
            print(f"{url}")

            driver.implicitly_wait(wait_seconds)
            driver.get(url)
            driver.execute_script("window.scrollBy(0, 500)")

            # gather information from page
            IDs = ("jobdetails-hauptberuf",
                   "jobdetails-titel",
                   "jobdetails-veroeffentlichungsdatum",
                   "jobdetails-kopf-arbeitgeber",
                   "jobdetails-arbeitsort",
                   "jobdetails-beschreibung")
            data = [None]*len(IDs)
            try:
                data = scrape_selenium(wait, IDs, url, data)
                write_content(url, data)
                write_file('known_URLs.txt', url, 'a')
                # store_url(url)
            except TimeoutException:
                # grab it with BeautifulSoup, if Selenium doesn't
                try:
                    html = driver.page_source
                    scrape_beautiful_soup(html, IDs, url, data)
                    write_content(url, data)
                    write_file('known_URLs.txt', url, 'a')
                    # store_url(url)
                    print("Elements found with BeautifulSoup")
                # if BeautifulSoup isn't able either
                except:
                    print("Elements not found")
                    # store it to file to check later
                    error_data = url + "\n" + html + "\n"
                    write_file(f'page{i}.html', error_data, 'w')
                    # remember url
                    write_file('bad_URLs.txt', url + '\n', 'a')
            if i >= 1:
                break


arbeitsagentur_scraper()
