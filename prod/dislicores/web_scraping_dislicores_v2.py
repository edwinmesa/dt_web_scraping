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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
# ------------------------------------------------------------------
# TODO: functions
# ------------------------------------------------------------------

# This function search each element of the document DOM

# sudo apt install firefox
# pip install webdriver-manager
# sudo apt install firefox-geckodriver

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
        time.sleep(0.0005)

# Function Beatiful View

def process_data():
    time.sleep(0.02)

# Date 

today = datetime.date.today() 

# Categories of brands that should be considered for search results
categories = ['vinos', 'licores', 'tequilas']

shops = {'Bogotá, D.c.', 'Medellín', 'Barranquilla'}

# ------------------------------------------------------------------
# TODO: Extract the data for shop EXITO
# ------------------------------------------------------------------

for city in shops:
    for category in categories:
        # Bar progress -> comment
        for _ in track(range(100), description=f'[green]Iniciando Scraping en Dislicores ciudad {city} categoria: {category}'):
            process_data()
        # Initialized by selenium driver with options and optmizer
        options = Options()
        options.set_preference("network.http.pipelining", True)
        options.set_preference("network.http.proxy.pipelining", True)
        # options.set_preference("network.http.pipelining.maxrequests", 8)
        # options.set_preference("content.switch.threshold", 250000)
        # options.set_preference("browser.cache.memory.capacity", 65536)
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
        # driver.maximize_window()
        # driver.set_window_position(2000,0)
        # driver.set_window_size(1180, 1000)
        driver.set_window_position(-50,-50)
        driver.set_window_size(1500, 1050)
        # driver.maximize_window()

        # Open the Page

        driver.get(f"https://www.dislicores.com/{category}")

        time.sleep(10)

        # Click on Modal Window
        try:
            findElementBy(
             By.XPATH, "//span[@class='vtex-minicart-2-x-minicartIconContainer gray relative']//*[@class=' ']", 2)
        except:
            break     
        # ActionChains(driver)

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
            By.XPATH, "//button[normalize-space()='Continuar']", 10)

        scrollDownPage(driver, 5)
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
                    EC.visibility_of_all_elements_located((By.XPATH, initial_XPATH)))
                time.sleep(5)       
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, initial_XPATH))).click()
                # to click on No button
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
            unit_measure = findElementNumberBySelector(
                ".vtex-product-summary-2-x-valueWrapper.vtex-product-summary-2-x-valueWrapper--grid.vtex-store-components-3-x-valueWrapper.vtex-product-summary-2-x-skuSelectorItemTextValue.vtex-product-summary-2-x-skuSelectorItemTextValue--grid.vtex-store-components-3-x-skuSelectorItemTextValue.c-on-base.center.pl5.pr5.z-1.t-body", "0")
            brand = findElementTextBySelector(
                ".vtex-product-summary-2-x-productBrandName", "SIN MARCA")
            price_prime = findElementNumberBySelector(
                ".exito-vtex-components-4-x-valuePLPAllied", "0")
            price_regular = findElementNumberBySelector(
                ".vtex-store-components-3-x-listPriceValue.ph2.dib.strike.vtex-store-components-3-x-price_listPrice", "0")
            price_now = findElementNumberBySelector(
                ".vtex-store-components-3-x-sellingPrice.vtex-store-components-3-x-sellingPriceValue.t-heading-2-s.dib.ph2.vtex-store-components-3-x-price_sellingPrice", "0")
            conditional_discount = findElementTextBySelector(
                ".dislicoresqa-custom-app-2-x-a_layout.dislicoresqa-custom-app-2-x-a_layout--productSummaryTagsGrid.flex.flex-column.justify-around.items-stretch.h-100.bg-base", "")
            discount = findElementNumberBySelector(
                ".vtex-store-components-3-x-discountInsideContainer.t-mini.white.absolute.right-0.pv2.ph3.bg-emphasis.z-1", "0")

            data.append({f"shop": "DISLICORES",
                         "city": city,
                         "location": city,
                         "category": category,
                         "name": name,
                         "unit_measure": unit_measure,
                         "brand": brand,
                         "price_prime": price_prime,
                         "price_regular": price_regular,
                         "price_now": price_now,
                         "conditional_discount": conditional_discount,
                         "conditional_discount_2": "",
                         "discount": discount,
                         "date": today
                         })

        df = pd.DataFrame(data)
        df.to_csv(f'D:\workflow\dt_web_scraping\prod\data\dislicores_{city}_{category}_data_{today}.txt',
                  index=False, encoding='utf-8')

        time.sleep(1)
        driver.quit()

time.sleep(10)
driver.quit()
