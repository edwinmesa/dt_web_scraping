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

def scrollDownPage(driver, t):
    time.sleep(t)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # time.sleep(t)
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Function Beatiful View
def process_data():
    time.sleep(0.02)

# Categories of brands that should be considered for search results
categories = ['vinos','licores', 'tequilas'] 

shops = {'Bogot??, D.c.', 'Medell??n','Barranquilla'}

# ------------------------------------------------------------------
# TODO: Extract the data for shop EXITO
# ------------------------------------------------------------------

for city in shops:
    for category in categories:
        # Bar progress -> comment
        for _ in track(range(100), description=f'[green]Iniciando Scraping en Dislicores ciudad {city} categoria: {category}'):
            process_data()
        # Initialized by selenium driver with options and optmizer
        options=Options()
        options.set_preference("network.http.pipelining", True)
        options.set_preference("network.http.proxy.pipelining", True)
        options.set_preference("network.http.pipelining.maxrequests", 8)
        options.set_preference("content.switch.threshold", 250000)
        options.set_preference("browser.cache.memory.capacity", 65536)
        options.set_preference("general.startup.browser", False)
        options.set_preference("reader.parse-on-load.enabled", False) # Disable reader, we won't need that.
        options.set_preference("browser.pocket.enabled", False)
        options.set_preference("loop.enabled", False)
        options.set_preference("browser.chrome.toolbar_style", 1) # Text on Toolbar instead of icons
        options.set_preference("browser.display.show_image_placeholders", False) # Don't show thumbnails on not loaded images.
        options.set_preference("browser.display.use_document_colors", False) # Don't show document colors.
        options.set_preference("browser.display.use_document_fonts", 0) # Don't load document fonts.
        options.set_preference("browser.display.use_system_colors", True) # Use system colors.
        options.set_preference("browser.formfill.enable", False) # Autofill on forms disabled.
        options.set_preference("browser.helperApps.deleteTempFileOnExit", True) # Delete temprorary files.
        options.set_preference("permissions.default.image", 2) 
        options.set_preference("browser.tabs.forceHide", True) # Disable tabs, We won't need that.
        options.set_preference("browser.urlbar.autoFill", False) # Disable autofill on URL bar.
        options.set_preference("browser.urlbar.autocomplete.enabled", False) # Disable autocomplete on URL bar.

        driver = webdriver.Firefox(options=options)
        driver.maximize_window()

        # Open the Page
       
        driver.get(f"https://www.dislicores.com/{category}")
      
        time.sleep(12)

        # Click on Modal Window
        findElementBy(
            By.XPATH, "//div[contains(text(),'BY ICOMMKT')]", 1)
        # Click for city selection
        findElementBy(
            By.XPATH, "//div[@class=' css-mqam1g']", 2)
        # Select City
        findElementBy(
            By.XPATH, "//div[@id='react-select-2-option-9']", 2)
        # Click Box
        findElementBy(
            By.XPATH, "//span[@class='dislicoresqa-custom-app-2-x-AgeVerification_a_checkbox_checkmark']", 2)
        # Click button continue
        findElementBy(
            By.XPATH, "//button[normalize-space()='Continuar']", 5)
        # Close ICOMMKT
        # findElementBy(
        #     By.XPATH, "//a[normalize-space()='Ahora no']", 2)

        # For security reasons, we used twice the function because the page is refresh
        # scrollDownPage(driver, 5)
        scrollDownPage(driver, 10)
      
        initial_XPATH = "//div[contains(@class,'vtex-button__label flex items-center justify-center h-100 ph5')]"
        # define the max clicks for page for default 30
        max_click_SHOW_MORE = 30
        # count the number of clicks
        count = 1
        # This loop search the button load more and apply the click until the end of page
        while count <= max_click_SHOW_MORE:
            try:
                WebDriverWait(driver, 30).until(
                    EC.visibility_of_all_elements_located((By.XPATH, initial_XPATH)))
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
                ".vtex-product-summary-2-x-productBrand.vtex-product-summary-2-x-brandName.t-body", "SIN DESCRIPCION")
            brand = findElementTextBySelector(
                ".vtex-product-summary-2-x-productBrandName", "SIN MARCA")
            price_prime = findElementNumberBySelector(
                ".exito-vtex-components-4-x-valuePLPAllied", "0")    
            price_regular = findElementNumberBySelector(
                ".vtex-store-components-3-x-listPriceValue.ph2.dib.strike.vtex-store-components-3-x-price_listPrice", "0")
            price_now = findElementNumberBySelector(
                ".vtex-store-components-3-x-sellingPrice.vtex-store-components-3-x-sellingPriceValue.t-heading-2-s.dib.ph2.vtex-store-components-3-x-price_sellingPrice", "0")
            discount = findElementNumberBySelector(
                ".vtex-store-components-3-x-discountInsideContainer.t-mini.white.absolute.right-0.pv2.ph3.bg-emphasis.z-1", "0")

            data_exito.append({f"shop": "DISLICORES",
                               "city": city,
                               "location": "Store",
                               "category": category,
                               "name": name,
                               "brand": brand,
                               "price_prime": price_prime,
                               "price_regular": price_regular,
                               "price_now": price_now,
                               "discount": discount})

        df = pd.DataFrame(data_exito)
        df.to_csv(f'C:\workflow\dt_web_scraping\prod\data\dislicores_{city}_{category}_data.txt',
                  index=False, encoding='utf-8')

        time.sleep(1)
        driver.quit()


time.sleep(3)
driver.quit()