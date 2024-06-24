# for getting pass and user out of env
import os
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException, TimeoutException

import time


from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-extensions")
options.add_argument('--remote-debugging-pipe')

# options.add_argument(r"--user-data-dir=/home/ben/.config/google-chrome/")
# options.add_argument(r'--profile-directory=Default')

driver = webdriver.Chrome(options=options)

# driver = webdriver.Chrome()

# Set up the WebDriver (make sure chromedriver is in your PATH)
# driver = webdriver.Chrome()

# Open the login page
driver.get("https://sms.bader.mod.uk/")

# Find the username and password fields and fill them out
username_field_1 = driver.find_element(By.NAME, "txtUsername")
password_field_1 = driver.find_element(By.NAME, "txtPassword")

username_field_2 = driver.find_element(By.NAME, "txtSecondaryUsername")
password_field_2 = driver.find_element(By.NAME, "txtSecondaryPassword")

# get .env file
load_dotenv()
# get users and pass
role_username = os.getenv("role_username")
role_password = os.getenv("role_password")
personal_username = os.getenv("personal_username")
personal_password = os.getenv("personal_password")

# send login
username_field_1.send_keys(role_username)
password_field_1.send_keys(role_password)
username_field_2.send_keys(personal_username)
password_field_2.send_keys(personal_password)

# submit 
login_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "btnSubmit")))
login_button.click()

# go to events page
driver.get("https://sms.bader.mod.uk/events/default.aspx")

# Click filter buttons to get only approved events
driver.execute_script("document.getElementsByName('ctl00$ctl00$cphBaseBody$cphBody$cbAdultIC')[0].click();")
driver.execute_script("document.getElementsByName('ctl00$ctl00$cphBaseBody$cphBody$cbMyUnit')[0].click();")
driver.execute_script("document.getElementsByName('ctl00$ctl00$cphBaseBody$cphBody$cbAttending')[0].click();")
# driver.execute_script("document.getElementsByName('ctl00$ctl00$cphBaseBody$cphBody$cbDraft')[0].click();")
# driver.execute_script("document.getElementsByName('ctl00$ctl00$cphBaseBody$cphBody$cbPending')[0].click();")
driver.execute_script("document.getElementsByName('ctl00$ctl00$cphBaseBody$cphBody$btnFilter')[0].click();")
driver.execute_script("document.getElementsByName('ctl00$ctl00$cphBaseBody$cphBody$cbToggleDisplay')[0].click();")



select_entries = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'eventTable_length')))
select = Select(select_entries)
# this changes the table to show all entries/events
select.select_by_value('-1')

numberOf = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'eventTable_info')))
numberOf_string = numberOf.text
numberOf_split = numberOf_string.split(" ")
numberOfEvents = int(numberOf_split[5])
print("There are ", numberOfEvents, "events.")
# get name of each event
table = driver.find_elements(by=By.XPATH, value='//*/tbody')
rows = table[0].find_elements(by=By.TAG_NAME, value="tr")
event_names = []
for row in rows:
    columns = row.find_elements(by=By.TAG_NAME, value='td')
    for index, col in enumerate(columns):
        if index == 1:
            event_names.append((col.text).replace("\n", " "))

data = []

for i in range(numberOfEvents):
    try:
        # click an individual event
        link = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'ctl00_ctl00_cphBaseBody_cphBody_lvEventDetails_ctrl' + str(i) +'_lbAttendees')))
        link.click()
        try:
            # this changes the table to show all entries/events
            select_entries = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'ctl00_ctl00_cphBaseBody_cphBody_eventNoticeboard_gvCadetsAttendees_length')))
            select = Select(select_entries)
            select.select_by_value('-1')
        except TimeoutException as e:
            print("Probably only staff on event")

        # get the table of names
        div = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "modal-content")))
        table = div.find_elements(by=By.XPATH, value='//*/tbody')
        rows = table[1].find_elements(by=By.TAG_NAME, value="tr")

        # Column to choose by its index, say the second column in the table
        each_event = []
        for row in rows:
            columns = row.find_elements(by=By.TAG_NAME, value='td')
            each_row = []
            for col in columns:
                each_row.append(col.text)
            each_event.append(each_row)
        
        data.append([event_names[i], each_event])


        
        # closes list
        div = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "modal-footer")))
        link = div.find_element(by=By.ID, value='ctl00_ctl00_cphBaseBody_cphBody_eventNoticeboard_btnCloseModal')
        
        link.click()

        time.sleep(0.5)
    except ElementClickInterceptedException as e:
        print("No cadets on event")
    except StaleElementReferenceException as e:
        print("Increase sleep time")

    print("Event ", i, "completed.")

# Save array to text file
with open('data.txt', 'w') as file:
    file.write(str(data))