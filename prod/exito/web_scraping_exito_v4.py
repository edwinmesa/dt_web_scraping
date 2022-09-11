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
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
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


def scrollDownPage(driver, t):
    time.sleep(t)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def scrollDownFullPage(driver):
    height = driver.execute_script("return document.body.scrollHeight")
    for i in range(height):
        # scroll by 10 on each iteration
        driver.execute_script('window.scrollBy(0,10)')
        # reset height to the new height after scroll-triggered elements have been loaded.
        height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(0.05)

# Function Beatiful View


def process_data():
    time.sleep(0.02)

# Date 

today = datetime.date.today() 

# Categories of brands that should be considered for search results
categories = ['whisky-ron-brandy-conac', 'vinos','cervezas', 'tequilas-ginebras-y-vodkas'] 
# City for search
shops = {'Bogotá, D.c.': 'EXITO Calle 80', 'Medellín': 'Exito Envigado','Barranquilla':'Exito Barranquilla'}
# ------------------------------------------------------------------
# TODO: Extract the data for shop EXITO
# ------------------------------------------------------------------

for city, suc in shops.items():
    for category in categories:
        for _ in track(range(100), description=f'[green]Iniciando Scraping en Exito ciudad: {city} sucursal: {suc} categoria: {category}'):
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
        options.set_preference(
            "browser.display.show_image_placeholders", False)
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
        driver.set_window_position(900,-50)
        # driver.set_window_position(2000,0)
        # driver.set_window_size(960, 1050)
        # driver.set_window_size(960, 1050)
        driver.maximize_window()
        # options = webdriver.ChromeOptions()
        # # options.add_argument("--headless")
        # options.add_argument("start-maximized")
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        # Open the Page
        if category == "whisky-ron-brandy-conac":
            driver.get(f"https://www.exito.com/licores/{category}")
        else:
            driver.get(f"https://www.exito.com/mercado/vinos-y-licores/{category}")

        time.sleep(20)

        findElementBy(
            By.XPATH, "//div[@class='exito-geolocation-3-x-contentOrderOption flex']//div[1]", 2)
        # Click for city selection
        findElementBy(
            By.CSS_SELECTOR, ".exito-geolocation-3-x-orderOptionsButton.orderoption-compra-recoge", 5)
        # List of cities
        findElementByAndSendKey(
            By.ID, "react-select-2-input", city, 5)
        findElementByAndSendKey(
            By.ID, "react-select-4-input", suc, 2)
        findElementBy(By.XPATH, "//button[normalize-space()='Confirmar']", 15)

        # For security reasons, we used twice the function because the page is refresh
        scrollDownPage(driver, 15)

        initial_XPATH = "//div[contains(@class,'vtex-button__label flex items-center justify-center h-100 ph5')]"
        # define the max clicks for page for default 30
        max_click_SHOW_MORE = 50
        # count the number of clicks
        count = 1
        # This loop search the button load more and apply the click until the end of page
        while count <= max_click_SHOW_MORE:
            try:
                WebDriverWait(driver, 30).until(
                    EC.visibility_of_all_elements_located((By.XPATH, initial_XPATH)))
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
                ".vtex-store-components-3-x-productNameContainer.mv0.t-heading-4", "SIN DESCRIPCION")
            brand = findElementTextBySelector(
                ".vtex-product-summary-2-x-productBrandName", "SIN MARCA")
            price_prime = findElementNumberBySelector(
                ".exito-vtex-components-4-x-valuePLPAllied", "0")
            price_regular = findElementNumberBySelector(
                ".exito-vtex-components-4-x-list-price.t-mini.ttn.strike", "0")
            price_now = findElementNumberBySelector(
                ".exito-vtex-components-4-x-PricePDP", "0")
            discount = findElementNumberBySelector(
                ".exito-vtex-components-4-x-badgeDiscount.flex.items-center", "0")

            data.append({f"shop": "EXITO",
                         "city": city,
                         "location": suc,
                         "category": category,
                         "name": name,
                         "brand": brand,
                         "price_prime": price_prime,
                         "price_regular": price_regular,
                         "price_now": price_now,
                         "discount": discount,
                         "date": today})

        df = pd.DataFrame(data)
        df.to_csv(f'D:\workflow\dt_web_scraping\prod\data\exito_{city}_{suc}_{category}_data_{today}.txt',
                  index=False, encoding='utf-8')

        time.sleep(1)
        driver.quit()


time.sleep(3)
driver.quit()
