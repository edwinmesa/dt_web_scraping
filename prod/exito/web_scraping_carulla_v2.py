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
from selenium.webdriver import ActionChains
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


# def findElementByAndSendKey(by, selector, key, t):
#     open_modal = driver.find_element(by, selector)
#     open_modal.click()
#     open_modal.send_keys(key)
#     open_modal.send_keys(Keys.TAB)
#     time.sleep(t)

def findElementByAndSendKey(by, selector, key, t):
    open_modal = driver.find_element(by, selector)
    actions = ActionChains(driver)
    actions.move_to_element(open_modal)
    actions.click()
    time.sleep(t)
    actions.key_down(Keys.SPACE).send_keys(key).key_up(Keys.CONTROL).perform()
    time.sleep(t)


def scrollDownPage(driver, t):
    time.sleep(t)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def scrollDownFullPage(driver):
    height = driver.execute_script("return document.body.scrollHeight")
    for i in range(height):
        driver.execute_script('window.scrollBy(0,10)') # scroll by 10 on each iteration
        height = driver.execute_script("return document.body.scrollHeight") # reset height to the new height after scroll-triggered elements have been loaded.
        time.sleep(0.05)  

# Function Beatiful View
def process_data():
    time.sleep(0.02)

# Date 

today = datetime.date.today()   

# Categories of brands that should be considered for search results
categories = ['whisky', 'vinos','cervezas', 'tequilas', 'ron'] 
# Cities for search 
shops = {'Bogot??, D.c.': 'Carulla FreshMarket Calle 140','Medell??n': 'Carulla Oviedo', 'Barranquilla': 'Carulla Mall Plaza Buenavista'}

# ------------------------------------------------------------------
# TODO: Extract the data for shop EXITO
# ------------------------------------------------------------------

for city, suc in shops.items():
    for category in categories:
        for _ in track(range(100), description=f'[green]Iniciando Scraping en Carulla ciudad: {city} sucursal: {suc} categoria: {category}]'):
            process_data()
    
        # Initialized by selenium driver with options and optmizer
        options=Options()
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
        # driver.set_window_position(2000,0)
        driver.maximize_window()
        # driver.set_window_position(900,-50)
        # driver.set_window_size(960, 1050)

        # Open the Page
        driver.get(f"https://www.carulla.com/vinos-y-licores/{category}")
        time.sleep(12)

        # findElementBy(
        #     By.XPATH, "//div[@class='exito-geolocation-3-x-contentOrderOption flex']//div[1]", 5)
        # # Click for city selection
        # findElementBy(
        #     By.CSS_SELECTOR, ".exito-geolocation-3-x-orderOptionsButton.orderoption-compra-recoge", 8)
        try:
            findElementBy(
                By.XPATH, "//span[@class='exito-geolocation-3-x-addressResultLabel']", 2)
        except:
            pass   
        # List of cities
        findElementByAndSendKey(
            By.CSS_SELECTOR, ".exito-geolocation-3-x-pickUpPointCitySelectCity.shippingaddress-lista-ciudad", city, 5)
        findElementByAndSendKey(
            By.CSS_SELECTOR, ".exito-geolocation-3-x-pickUpPointCitySelectCity.buycollect-lista-almacen", suc, 2)
        findElementBy(By.XPATH, "//button[normalize-space()='Confirmar']", 15)

         # For security reasons, we used twice the function because the page is refresh
        scrollDownPage(driver, 15)
        # scrollDownFullPage(driver)

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
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, initial_XPATH))).click()
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

            data.append({f"shop": "CARULLA",
                        "city": city,
                        "location": suc,
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
        df.to_csv(f'/home/pydev/workflow/dt_web_scraping/prod/data/carulla_{city}_{suc}_{category}_data_{today}.txt',
                index=False, encoding='utf-8')

        time.sleep(1)
        driver.quit()


time.sleep(3)
driver.quit()
