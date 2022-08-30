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
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
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


def scrollDownPage(t):
    time.sleep(t)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # javaScript = "window.scrollBy(0, 1000);"
    # driver.execute_script(javaScript)


def process_data():
    time.sleep(0.02)

# Cities for search
categories = ['whisky', 'vinos','cervezas', 'tequilas', 'ron'] 

shops = {'Bogotá, D.c.': 'Carulla FreshMarket Calle 140',
         'Medellín': 'Carulla Oviedo', 'Barranquilla': 'Carulla Mall Plaza Buenavista'}

# ------------------------------------------------------------------
# TODO: Extract the data for shop EXITO
# ------------------------------------------------------------------

for city, suc in shops.items():
    for category in categories:
        for _ in track(range(100), description=f'[green]Iniciando Scraping en Carulla ciudad: {city} sucursal: {suc} categoria: {category}]'):
            process_data()
        options = Options()
        driver = webdriver.Firefox(options=options)
        driver.maximize_window()

        # Open the Page
        driver.get(f"https://www.carulla.com/vinos-y-licores/{category}")
        time.sleep(15)

        findElementBy(
            By.XPATH, "//div[@class='exito-geolocation-3-x-contentOrderOption flex']//div[1]", 2)
        # Click for city selection
        findElementBy(
            By.CSS_SELECTOR, ".exito-geolocation-3-x-orderOptionsButton.orderoption-compra-recoge", 2)
        # List of cities
        findElementByAndSendKey(
            By.ID, "react-select-2-input", city, 5)
        findElementByAndSendKey(
            By.ID, "react-select-4-input", suc, 2)
        findElementBy(By.XPATH, "//button[normalize-space()='Confirmar']", 2)

        # For security reasons, we used twice the function because the page is refresh
        scrollDownPage(15)
        # scrollDownFullPage(driver)

        initial_XPATH = "//div[contains(@class,'vtex-button__label flex items-center justify-center h-100 ph5')]"

        # WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH, initial_XPATH))).click()
        # max_click_SHOW_MORE = 5
        # count = 1 
        # while count <= max_click_SHOW_MORE:
        #     try:
        #         time.sleep(20)
        #         new_XPATH = initial_XPATH[:67] + str(count) + initial_XPATH[67:]
        #         WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH, new_XPATH))).click()
        #         print("Button clicked #", count+1)
        #         count += 1
        #     except TimeoutException:
        #         break
        # define the max clicks for page for default 30
        max_click_SHOW_MORE = 25
        # count the number of clicks
        count = 1
        # This loop search the button load more and apply the click until the end of page
        scrollDownPage(3)
        scrollDownPage(3)
        scrollDownPage(3)
        WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH, initial_XPATH))).click()
        while count <= max_click_SHOW_MORE:
            try:
                scrollDownPage(2)
                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, initial_XPATH))).click()
                # scrollDownPage(driver, 2)
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, initial_XPATH))).click()
                # to click on No button
                count += 1
                # time.sleep(1)
                # Bar progress -> comment
                for i in track(range(4), description=f"[red]Explorando Pagina Web iter {count - 1}.........."):
                    time.sleep(1)
            except ElementClickInterceptedException:
                break

        # try:
        #     for i in range(1000):
        #         load_more_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, XPATH)))
        #     time.sleep(3)
        #     load_more_button.click()
        # except:
        #     pass
        #     print("task load more button completed")    

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

            data.append({f"shop": "CARULLA",
                        "city": city,
                        "location": suc,
                        "category": category,
                        "name": name,
                        "brand": brand,
                        "price_prime": price_prime,
                        "price_regular": price_regular,
                        "price_now": price_now,
                        "discount": discount})

        df = pd.DataFrame(data)
        df.to_csv(f'C:\workflow\dt_web_scraping\prod\data\carulla_{city}_{suc}_{category}_data.txt',
                index=False, encoding='utf-8')

        time.sleep(1)
        driver.quit()


time.sleep(3)
driver.quit()
