# import libraries
import time
import datetime
import pandas as pd
from rich import print as rprint
from rich.pretty import pprint
from rich.progress import Progress
import re
from rich.progress import track
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
# ------------------------------------------------------------------
# TODO: functions
# ------------------------------------------------------------------

# This function search each element of the document DOM


def findElementTextBySelector(selector, exception):
    try:
        element = i.find_element(
            By.CSS_SELECTOR, selector).text.strip().upper()
    except:
        element = exception
    return element


def findElementNumberBySelector(selector, exception):
    try:
        element = i.find_element(
            By.CSS_SELECTOR, selector).text.replace('$', '')
        element = "".join([ch for ch in element if ch.isdigit()])
    except:
        element = exception
    return element


def findElementBy(by, selector, t):
    open_modal = driver.find_element(by, selector)
    open_modal.click()
    time.sleep(t)


def findElementByAndSendKey(by, selector, key, t):
    open_modal = driver.find_element(by, selector)
    open_modal.click()
    open_modal.send_keys(key)
    open_modal.send_keys(Keys.TAB)
    time.sleep(t)



def findElementNumberByXPATH(selector, exception):
    try:
        element = i.find_element(
            By.XPATH, selector).text.replace('$', '')
        element = "".join([ch for ch in element if ch.isdigit()])
    except:
        element = exception
    return element


def scrollDownPage(driver, t):
    time.sleep(t)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def scrollDownFullPage(driver):
    height = driver.execute_script("return document.body.scrollHeight")
    for i in range(height):
        # scroll by 10 on each iteration
        driver.execute_script('window.scrollBy(0,20)')
        # reset height to the new height after scroll-triggered elements have been loaded.
        height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(0.05)

# Function Beatiful View


def process_data():
    time.sleep(0.02)

# Date 

today = datetime.date.today()    

# Categories of brands that should be considered for search results


shops = ["Bogota", "Medellin"]
categories = ['whisky', 'vodka', 'cremas',
              'ginebra', 'ron', 'tequila-y-mezcal']

# ------------------------------------------------------------------
# TODO: Extract the data for shop EXITO
# ------------------------------------------------------------------

for city in shops:
    for category in categories:
        # Bar progress -> comment
        for _ in track(range(100), description=f'[green]Iniciando Scraping en Diageo categoria: {category} en la ciudad: {city}'):
            process_data()
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        # driver.maximize_window()

        # Open the Page

        driver.get(f"https://co.thebar.com/{category}")

        time.sleep(10)

        # Click on Modal Window
        findElementBy(
            By.XPATH, "//*[@id='btn-si']", 1)

        findElementBy(
            By.CSS_SELECTOR, "#termsAndConditions", 2)
        
        # Click for city selection
        findElementBy(
            By.XPATH, "//select[@id='ciudadAgeVerification']", 2)
        # Select City
        findElementByAndSendKey(
            By.ID, "ciudadAgeVerification", city, 2)

        # scrollDownPage(driver, 15)
        # scrollDownFullPage(driver)

        initial_XPATH = "//div[contains(@class,'vtex-button__label flex items-center justify-center h-100 ph5')]"
        # define the max clicks for page for default 30
        max_click_SHOW_MORE = 35
        # count the number of clicks
        count = 1
        # This loop search the button load more and apply the click until the end of page
        while count <= max_click_SHOW_MORE:
            try:
                WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located((By.XPATH, initial_XPATH)))
                time.sleep(5)    
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, initial_XPATH))).click()
                count += 1
                time.sleep(2)
                # Bar progress -> comment
                for i in track(range(4), description=f"[red]Explorando Pagina Web iter {count - 1}.........."):
                    time.sleep(1)

            except TimeoutException:
                break

        # Search the elements of the page
        items = driver.find_elements(
            By.CSS_SELECTOR,  ".vtex-product-summary-2-x-element.pointer.pt3.pb4.flex.flex-column.h-100")
        # Create a frame empty for the data
        data = []
        # iterate over each element
        for i in items:
            name = findElementTextBySelector(
                ".vtex-product-summary-2-x-productBrand.vtex-product-summary-2-x-brandName.t-body", "SIN DESCRIPCION")
            brand = findElementTextBySelector(
                ".class", "SIN MARCA")
            price_prime = findElementNumberBySelector(
                ".class", "0")
            price_regular = findElementNumberBySelector(
                ".vtex-product-price-1-x-listPriceValue.strike", "0")
            price_now = findElementNumberBySelector(
                ".vtex-product-price-1-x-sellingPriceValue", "0")
            discount = findElementNumberBySelector(
                ".vtex-store-components-3-x-discountInsideContainer.t-mini.white.absolute.right-0.pv2.ph3.bg-emphasis.z-1", "0")

            data.append({f"shop": "DIAGEO",
                         "city": city,
                         "location": city,
                         "category": category,
                         "name": name,
                         "unit_measure": "",
                         "brand": brand,
                         "price_prime": price_prime,
                         "price_regular": price_regular,
                         "price_now": price_now,
                         "conditional_discount": "",
                         "conditional_discount_2": "",
                         "discount": discount,
                         "date": today
                         })

        df = pd.DataFrame(data)
        df.to_csv(f'D:\workflow\dt_web_scraping\prod\data\diageo_{city}_{category}_data_{today}.txt',
                  index=False, encoding='utf-8')

        time.sleep(1)
        driver.quit()

time.sleep(3)
driver.quit()
