# for getting pass and user out of env
import os
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


import time
# Set up the WebDriver (make sure chromedriver is in your PATH)
driver = webdriver.Chrome()

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
driver.execute_script("document.getElementsByName('ctl00$ctl00$cphBaseBody$cphBody$cbDraft')[0].click();")
driver.execute_script("document.getElementsByName('ctl00$ctl00$cphBaseBody$cphBody$cbPending')[0].click();")
driver.execute_script("document.getElementsByName('ctl00$ctl00$cphBaseBody$cphBody$btnFilter')[0].click();")
driver.execute_script("document.getElementsByName('ctl00$ctl00$cphBaseBody$cphBody$cbToggleDisplay')[0].click();")



select_entries = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'eventTable_length')))
select = Select(select_entries)
# this changes the table to show all entries/events
select.select_by_value('-1')

time.sleep(5)
numberOf = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'eventTable_info')))
numberOf_string = numberOf.text
numberOf_split = numberOf_string.split(" ")
numberOfEvents = numberOf_split[5]

link = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'ctl00_ctl00_cphBaseBody_cphBody_lvEventDetails_ctrl0_lbAttendees')))
link.click()

print(1)
div = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "modal-content")))
# div = driver.find_element(by=By.CLASS_NAME, value="modal-content")
table = div.find_elements(by=By.XPATH, value='//*/tbody')

rows = table[1].find_elements(by=By.TAG_NAME, value="tr")

# Column to choose by its index, say the second column in the table
desired_column = 1
desired_column_data = []

for row in rows:
    columns = row.find_elements(by=By.TAG_NAME, value='td')

    for index, col in enumerate(columns):
        if index == desired_column:
            desired_column_data.append(col.text)

print(desired_column_data)

# closes list
# link = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'ctl00_ctl00_cphBaseBody_cphBody_eventNoticeboard_btnCloseModal')))
# link.click()
# print(2)

# ctl00_ctl00_cphBaseBody_cphBody_lvEventDetails_ctrl7_lbAttendees
time.sleep(500)
