"""
file: main.py
author: Afnan Enayet

This module is the entry point for the data processing pipeline, which takes
the raw HTML data scraped from the course assessment portal.
"""

import os
from typing import List
from pathlib import Path
from bs4 import BeautifulSoup
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# The set of classes that need to be present for a valid "review"
REVIEW_CLASSES: set = {"mPTDC", "TTHC", "mPTLC", "PTLC", "OOLT"}


def scrape_html_files(chromedriver: str) -> dict:
    """ Using the chromedriver, go to the course assessment portal and extract
    the HTML files for each Professor, saving the HTML in the desired directory.

    Args:
        - chromedriver: The path to the chromedriver executable. If this isn't
          set, then the program will attempt to look for chromedriver in your
          path.
    """
    browser = webdriver.Chrome(
        executable_path=chromedriver, chrome_options=webdriver.ChromeOptions())
    # Get security information so we can log in
    username = os.environ["dart_username"]
    password = os.environ["dart_password"]
    auth = os.environ["dart_auth"]

    # go to banner
    browser.get('https://www.dartmouth.edu/bannerstudent/')

    # input username
    username_box = browser.find_element_by_id("userid")
    username_box.send_keys(username)
    submit_user = browser.find_element_by_class_name("loginButton")
    submit_user.click()

    # input password
    password_box = browser.find_element_by_id("Bharosa_Password_PadDataField")
    password_box.send_keys(password)
    password_box.send_keys(Keys.ENTER)

    # security question
    auth_box = browser.find_element_by_id("Bharosa_Challenge_PadDataField")
    auth_box.send_keys(auth)
    auth_box.send_keys(Keys.ENTER)

    # find course assessments
    all_tiles = browser.find_element_by_id("all-tiles-category")
    all_tiles.click()
    portal = browser.find_element_by_link_text('Course Assessment Portal')
    portal.click()

    # dictionary of professor and corresponding comments
    reviews = dict()

    # get table of classes
    instructor_names = list()
    browser.switch_to.window(browser.window_handles[1])
    tbody = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
    rows = WebDriverWait(tbody, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))

    for row in rows:
        prof = row.find_element_by_xpath('./td[4]').text

        # if a new prof is found
        if prof not in instructor_names:
            first_name = prof.split(",")[1].strip()
            last_name = prof.split(",")[0].strip()
            print(f"Scraping for Prof: {first_name} {last_name}")
            instructor_names.append(prof)

            # open up reviews
            faculty_page = row.find_element_by_xpath('./td[5]/span[2]/a')
            faculty_page.click()
            browser.switch_to.window(browser.window_handles[2])
            # sleep(2)

            # save reviews as HTML
            gear = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID,
                                                'uberBar_dashboardpageoptions')))
            gear.click()
            print_page = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, 'idPagePrint')))
            print_page.click()
            print_menu = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, "idDashboardPrintDisplayLayoutMenu")))
            print_html_button = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    "#idDashboardPrintDisplayLayoutMenu > table > tbody > " +
                    "tr:nth-child(1) > td.masterMenu.shadowMenuCell > " +
                    "a:nth-child(2)")))
            print_html_button.click()
            sleep(2)

            # extract the HTML source and parse the source files
            html_source = browser.page_source
            review_list = list(parse_html(html_source))
            print(f"({len(review_list)}) reviews")
            reviews[f"{last_name},{first_name}"] = review_list

            # go back to table
            browser.switch_to.window(browser.window_handles[3])
            browser.close()
            browser.switch_to.window(browser.window_handles[2])
            browser.close()
            browser.switch_to.window(browser.window_handles[1])
    browser.close()
    return reviews


def load_html(path: str) -> str:
    """ Load the contents of an HTML file given some path

    This function will raise an exception if the path is not a valid,
    accessible file.

    Args:
        - path: The path to a file
    Returns: The contents of the file as a string
    """
    # Check the validity of the path
    path_obj = Path(path)

    if not path_obj.is_file():
        raise ValueError("Given path is not a valid file")

    # The string holding the contents of the file
    file_str: str = ""

    # Read the contents of a file to string
    with open(path, "r") as f:
        file_str = f.read()
    return file_str


def parse_html(html_contents: str) -> List[str]:
    """ Given a file containing reviews for a class, a faculty member, or a
    cross section, this function parses the actual text content of reviews and
    dumps them into a list.

    Args:
        - html_contents: A string containing the contents of the HTML file to parse
    Returns: A list of strings, containing all of the reviews that were parsed
    """
    soup = BeautifulSoup(html_contents, "lxml")

    # try to look for the table elements with the review text
    review_candidates = soup.findAll("td")
    reviews = list()

    # Look for elements that have the proper set of classes, so we
    # can determine that they are valid reviews
    for rev in review_candidates:
        if rev.has_attr("class"):
            classes: set = set(rev.get("class", []))

            if classes == REVIEW_CLASSES:
                reviews.append(rev.text)
    return reviews


def main():
    """ Entry point for the main function
    """
    parser = argparse.ArgumentParser(
        description="Process HTML files with class review data")
    parser.add_argument("file_loc", type=str,
                        help="The location of the JSON file to save")
    args = parser.parse_args()
    review_dict = scrape_html_files("./chromedriver")
    j = json.dumps(review_dict)

    with open(str(args.file_loc), "w+") as f:
        f.write(j)


if __name__ == "__main__":
    main()
