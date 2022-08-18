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
from selenium.webdriver.common.keys import Keys
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

# Function Beatiful View


def process_data():
    time.sleep(0.02)

# ----------------------------------------------------------------
# TODO: add support for the WebDriver
# ----------------------------------------------------------------


# Bar progress -> comment
for _ in track(range(100), description='[green]Iniciando Scraping Almacenes EXITO'):
    process_data()
# Initialized by selenium driver
driver = webdriver.Firefox()
driver.maximize_window()
# Categories of brands that should be considered for search results
categories = ['whisky-ron-brandy-conac', 'vinos',
              'cervezas', 'tequilas-ginebras-y-vodkas']
shops = dict([
    ('Bogotá, D.c.', 'EXITO Calle 80'),
    ('Medellín', 'Exito Poblado'),
])
# ------------------------------------------------------------------
# TODO: Extract the data for shop EXITO
# ------------------------------------------------------------------

for category in categories:
    # Open the Page
    driver.get("https://www.exito.com/")
    time.sleep(10)

    # Open the modal for buy
    findElementBy(
        By.XPATH, "//span[@class='exito-geolocation-3-x-addressResult']", 3)
    # Select for buy
    findElementBy(
        By.XPATH, "//div[@class='exito-geolocation-3-x-contentOrderOption flex']//div[1]", 3)
    # Click for city selection
    findElementBy(
        By.CSS_SELECTOR, ".exito-geolocation-3-x-orderOptionsButton.orderoption-compra-recoge", 3)
    # List of cities
    findElementByAndSendKey(
        By.ID, "react-select-2-input", "Bogotá, D.c.", 3)
    # Select the city
    # findElementBy(By.XPATH, "//div[@id='react-select-2-option-0']", 1)
    # Click for shop selection
    findElementByAndSendKey(
        By.ID, "react-select-4-input","EXITO Calle 80", 3)
    # Select the shop
    # findElementBy(By.XPATH, "//div[@id='react-select-4-option-0']", 1)
    # confirm the selection
    
    findElementBy(By.XPATH, "//button[normalize-space()='Confirmar']", 10)

    break
    # Click in menu
    findElementBy(By.ID, "category-menu", 10)
    # Click in Grocery
    findElementBy(By.ID, "undefined-nivel2-Mercado", 10)
    # Click in Categories
    findElementBy(
        By.XPATH, "//p[@id='Categorías-nivel3-Whisky, ron, brandy y coñac']", 15)
    # Go to end the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    initial_XPATH = "//div[contains(@class,'vtex-button__label flex items-center justify-center h-100 ph5')]"
    # define the max clicks for page for default 30
    max_click_SHOW_MORE = 20
    # count the number of clicks
    count = 1
    # This loop search the button load more and apply the click until the end of page
    while count <= max_click_SHOW_MORE:
        try:
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, initial_XPATH))).click()
            WebDriverWait(driver, 20).until(
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
    data_exito = []
    # iterate over each element
    for i in items:
        name = findElementTextBySelector(
            ".vtex-store-components-3-x-productNameContainer.mv0.t-heading-4", "SIN DESCRIPCION")
        brand = findElementTextBySelector(
            ".vtex-product-summary-2-x-productBrandName", "SIN MARCA")
        price_regular = findElementNumberBySelector(
            ".exito-vtex-components-4-x-list-price.t-mini.ttn.strike", "0")
        price_now = findElementNumberBySelector(
            ".exito-vtex-components-4-x-PricePDP", "0")
        discount = findElementNumberBySelector(
            ".exito-vtex-components-4-x-badgeDiscount.flex.items-center", "0")

        data_exito.append({"shop": "EXITO", "city": "Bogota", "location": "Exito Calle 80", "name": name, "brand": brand, "price_jumbo_prime": price_jumbo_prime, "price_regular": price_regular,
                           "price_now": price_now, "discount": discount})

        rprint("SKU: " + name,
               "|Marca: " + brand,
               #    "|Precio Jumbo Prime: " + price_jumbo_prime,
               ",Precio Regular: " + price_regular,
               "|Precio Normal: " + price_now,
               "|Descuento Congnitivo: " + discount)
