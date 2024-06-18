# for getting pass and user out of env
import os
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
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
login_button = driver.find_element(By.NAME, "btnSubmit")
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


time.sleep(500)

