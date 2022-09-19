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


def findElementNumberByXPATH(selector, exception):
    try:
        element = i.find_element(
            By.XPATH, selector).text.replace('$', '')
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
        time.sleep(0.35)

# Function Beatiful View


def process_data():
    time.sleep(0.02)


# Date

today = datetime.date.today()

# Categories of brands that should be considered for search results
# categories = ['whisky', 'vino','ron', 'tequila', 'cerveza']


shops = {'ANTIOQUIA': 'Medellín',
         'BOGOTÁ, D.C.': 'Bogotá, D.C.', 'ATLÁNTICO': 'BARRANQUILLA'}

# ------------------------------------------------------------------
# TODO: Extract the data for shop LA LICORERA
# ------------------------------------------------------------------

for city, suc in shops.items():
    # Bar progress -> comment
    for _ in track(range(100), description=f'[green]Iniciando Scraping Almacenes Olimpica ciudad: {city} sucursal: {suc}'):
        process_data()
    # Initialized by selenium driver with options and optmizer
    options = Options()
    options.set_preference("network.http.pipelining", True)
    options.set_preference("network.http.proxy.pipelining", True)
    # options.set_preference("network.http.pipelining.maxrequests", 8)
    # options.set_preference("content.switch.threshold", 250000)
    # options.set_preference("browser.cache.memory.capacity", 65536)
    options.set_preference("general.startup.browser", False)
    # Disable reader, we won't need that.
    options.set_preference("reader.parse-on-load.enabled", False)
    options.set_preference("browser.pocket.enabled", False)
    options.set_preference("loop.enabled", False)
    # Text on Toolbar instead of icons
    options.set_preference("browser.chrome.toolbar_style", 1)
    # Don't show thumbnails on not loaded images.
    options.set_preference("browser.display.show_image_placeholders", False)
    # Don't show document colors.
    options.set_preference("browser.display.use_document_colors", False)
    # Don't load document fonts.
    options.set_preference("browser.display.use_document_fonts", 0)
    # Use system colors.
    options.set_preference("browser.display.use_system_colors", True)
    # Autofill on forms disabled.
    options.set_preference("browser.formfill.enable", False)
    # Delete temprorary files.
    options.set_preference("browser.helperApps.deleteTempFileOnExit", True)
    options.set_preference("permissions.default.image", 2)
    # Disable tabs, We won't need that.
    options.set_preference("browser.tabs.forceHide", True)
    # Disable autofill on URL bar.
    options.set_preference("browser.urlbar.autoFill", False)
    # Disable autocomplete on URL bar.
    options.set_preference("browser.urlbar.autocomplete.enabled", False)

    driver = webdriver.Firefox(options=options)
    # driver.set_window_position(900,-50)
    # driver.set_window_size(960, 1050)
    # driver.set_window_size(1500, 1050)
    driver.set_window_position(2000, 0)
    driver.set_window_size(1500, 1050)
    # driver.maximize_window()

    # Open the Page
    driver.get(f"https://www.olimpica.com/supermercado/licores")
    time.sleep(10)

    # Click for city selection
    findElementBy(
        By.XPATH, "//div[@class='flex flex-row']//div[@class='css-1pcexqc-container pointer bw1 t-body']", 2)

    findElementBy(
        By.XPATH, f"//div[contains(text(),'{city}')]", 2)

    findElementBy(
        By.XPATH, "//div[contains(@class,'flex flex-row pt3')]//div[contains(@class,'css-1pcexqc-container pointer bw1 t-body')]", 2)

    findElementBy(
        By.XPATH, f"//div[contains(text(),'{suc}')]", 2)

    findElementBy(
        By.XPATH, "//div[normalize-space()='Elegir']", 2)

    scrollDownFullPage(driver)

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
            ".olimpica-dinamic-flags-0-x-strikePrice.false", "0")
        price_now = findElementNumberBySelector(
            ".vtex-product-price-1-x-sellingPrice--hasListPrice--dynamicF", "0")
        discount = findElementNumberBySelector(
            ".olimpica-dinamic-flags-0-x-containerPercentageFlagDcto", "0")

        data.append({f"shop": "OLIMPICA",
                     "city": city,
                     "location": suc,
                     "category": "Todas",
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
    df.to_csv(f'/home/edwsar/worflow/dt_web_scraping/prod/data/olimpica_{city}_{suc}_data_{today}.txt',
              index=False, encoding='utf-8')

    time.sleep(1)
    driver.quit()

time.sleep(3)
driver.quit()
