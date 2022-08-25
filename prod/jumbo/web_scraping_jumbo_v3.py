# import libraries
import time
import pandas as pd
from rich import print as rprint
from rich.pretty import pprint
from rich.progress import Progress
import re
from rich.progress import track
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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

def scrollDownFullPage(driver):
    height = driver.execute_script("return document.body.scrollHeight")
    for i in range(height):
        driver.execute_script('window.scrollBy(0,20)') # scroll by 10 on each iteration
        height = driver.execute_script("return document.body.scrollHeight") # reset height to the new height after scroll-triggered elements have been loaded.
        time.sleep(0.05)  


# Function Beatiful View


def process_data():
    time.sleep(0.02)

# ----------------------------------------------------------------
# TODO: add support for the WebDriver
# ----------------------------------------------------------------


# Bar progress -> comment
for _ in track(range(100), description='[green]Iniciando Scraping Almacenes JUMBO'):
    process_data()
# Initialized by selenium driver
driver = webdriver.Firefox()
driver.maximize_window()
# Categories of brands that should be considered for search results
categories = ['whisky', 'vino', 'cervezas', 'tequilas-y-piscos', 'ron']

# ------------------------------------------------------------------
# TODO: Extract the data for shop JUMBO
# ------------------------------------------------------------------
for category in categories:
    # Bar progress -> comment
    for _ in track(range(100), description=f'[yellow]Busqueda por la Categoria : {category}'):
        process_data()

    driver.get(
        f"https://www.tiendasjumbo.co/supermercado/vinos-y-licores/{category}")
    time.sleep(15)

    initial_XPATH = "//div[contains(@class,'vtex-button__label flex items-center justify-center h-100 ph5')]"
    # define the max clicks for page for default 30
    max_click_SHOW_MORE = 35
    # count the number of clicks
    count = 1
    # This loop search the button load more and apply the click until the end of page
    while count <= max_click_SHOW_MORE:
        try:
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, initial_XPATH))).click()
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, initial_XPATH))).click()
            count += 1
            time.sleep(10)
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
            ".vtex-product-summary-2-x-productBrandName", "SIN MARCA")
        price_prime = findElementNumberBySelector(
            ".tiendasjumboqaio-jumbo-minicart-2-x-generalPrice.tiendasjumboqaio-jumbo-minicart-2-x-primePrice.tiendasjumboqaio-jumbo-minicart-2-x-generalPriceSmall", "0")
        price_regular = findElementNumberBySelector(
            ".tiendasjumboqaio-jumbo-minicart-2-x-cencoListPrice", "0")
        price_now = findElementNumberBySelector(
            ".flex.c-emphasis.tiendasjumboqaio-jumbo-minicart-2-x-cencoPrice", "0")
        discount = findElementNumberBySelector(
            ".tiendasjumboqaio-jumbo-minicart-2-x-containerPercentageFlag", "0")

        data.append({"shop": "JUMBO",
                           "city": "Medellin",
                           "location": "Nacional",
                           "category": category,
                           "name": name,
                           "brand": brand,
                           "price_prime": price_prime,
                           "price_regular": price_regular,
                           "price_now": price_now,
                           "discount": discount})
    df = pd.DataFrame(data)
    df.to_csv(f'C:\workflow\dt_web_scraping\prod\data\jumbo_medellin_{category}_data.txt',
              index=False, encoding='utf-8')

time.sleep(3)
driver.quit()
