from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# get login info
login_dict = pd.read_excel('../login.xlsx').to_dict()
username = login_dict['username'][0]
password = login_dict['password'][0]
auth = login_dict['auth'][0]

# start chrome driver and set download path
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "./instructor_xlxs"}
chromeOptions.add_experimental_option("prefs",prefs)
chromedriver = "./chromedriver"
browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)

#go to banner
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

# get table of classes
instructor_names = []
browser.switch_to_window(browser.window_handles[1])
tbody = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
rows = WebDriverWait(tbody, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))

# iterate over table
for row in rows:
    prof = row.find_element_by_xpath('./td[4]').text
    print(prof)

    # if a new prof is found
    if prof not in instructor_names:
        instructor_names.append(prof)

        # open up reviews
        faculty_page = row.find_element_by_xpath('./td[5]/span[2]/a')
        faculty_page.click()
        browser.switch_to_window(browser.window_handles[2])
        sleep(2)

        # save reviews
        gear = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'uberBar_dashboardpageoptions')))
        gear.click()
        export_excel = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'idPageExportToExcel')))
        export_excel.click()
        export_dashboard = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="idDashboardExportToExcelMenu"]/table/tbody/tr[1]/td[1]/a[2]')))
        export_dashboard.click()
        sleep(2)

        # go back to table
        browser.close()
        browser.switch_to_window(browser.window_handles[1])

# clean up
browser.close()
browser.close()
