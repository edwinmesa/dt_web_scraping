# selenium 4
from selenium import webdriver  # browser exposes an executable file
# Through Selenium test we will invoke the executable file which will then #invoke actual browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()))


# get method to launch the URL
url = driver.get("https://www.dislicores.com/")
# to refresh the browser

time.sleep(2)  # Sleep for 3 seconds

# the driver determines that should be used or not based the XPATH variable
# This variables should be changed with the time

# Open modal window
open_modal = driver.find_element(
    By.XPATH, "//div[contains(text(),'BY ICOMMKT')]")
open_modal.click()


time.sleep(2)  # Sleep for 3 seconds

# select city
select_modal = driver.find_element(By.XPATH, "//div[@class=' css-mqam1g']")
select_modal.click()

# # select city
select_modal_city = driver.find_element(
    By.XPATH, "//div[@id='react-select-2-option-9']")
select_modal_city.click()

time.sleep(2)  # Sleep for 3 seconds

# # click on list box
click_modal_list_box = driver.find_element(
    By.XPATH, "//span[@class='dislicoresqa-custom-app-2-x-AgeVerification_a_checkbox_checkmark']")
click_modal_list_box.click()

time.sleep(2)  # Sleep for 3 seconds

# # click on continue button
click_modal_continue_button = driver.find_element(
    By.XPATH, "//button[normalize-space()='Continuar']")
click_modal_continue_button.click()


time.sleep(2)  # Sleep for 3 seconds

# # click on whisky
click_close_notification = driver.find_element(
    By.XPATH, "//a[normalize-space()='Ahora no']")
click_close_notification.click()

time.sleep(2)  # Sleep for 3 seconds

# # click on licors
click_licors = driver.find_element(By.XPATH, "//a[@href='/licores/whisky']//div[@class='vtex-store-link-0-x-childrenContainer vtex-store-link-0-x-childrenContainer--home-main-category-card']//div[@class='vtex-rich-text-0-x-container vtex-rich-text-0-x-container--home-main-category-text flex tl items-start justify-start t-body c-on-base']//div[@class='vtex-rich-text-0-x-wrapper vtex-rich-text-0-x-wrapper--home-main-category-text']")
click_licors.click()


time.sleep(5)  # Sleep for 3 seconds