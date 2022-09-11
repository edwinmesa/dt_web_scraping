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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options


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
categories = ['whisky', 'vino', 'cervezas', 'tequilas-y-piscos', 'ron']
for category in categories:
    # Bar progress -> comment
    for _ in track(range(100), description=f'[yellow]Busqueda por la Categoria : {category}'):
        process_data()
    # Initialized by selenium driver
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
    driver.set_window_position(2000,0)
    # driver.set_window_position(900,-50)
    # driver.set_window_size(960, 1050)
    driver.set_window_size(1500, 1050)
    # driver.maximize_window()
    

    driver.get(
        f"https://www.tiendasjumbo.co/supermercado/vinos-y-licores/{category}")

    time.sleep(15)

    initial_XPATH = "//div[contains(@class,'vtex-button__label flex items-center justify-center h-100 ph5')]"
    # define the max clicks for page for default 30
    max_click_SHOW_MORE = 45
    # count the number of clicks
    count = 1
    # This loop search the button load more and apply the click until the end of page
    while count <= max_click_SHOW_MORE:
        try:
            WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.XPATH, initial_XPATH))).click()
            time.sleep(10)    
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, initial_XPATH))).click()
            count += 1
            time.sleep(5)
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
                     "discount": discount,
                     "date": today})
    df = pd.DataFrame(data)
    df.to_csv(f'D:\workflow\dt_web_scraping\prod\data\jumbo_medellin_{category}_data_{today}.txt',
              index=False, encoding='utf-8')
    time.sleep(1)
    driver.quit()

time.sleep(3)
driver.quit()
