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

# Function Beatiful View
def process_data():
    time.sleep(0.02)

# Categories of brands that should be considered for search results
categories = ['whisky', 'vino','ron', 'tequila', 'cerveza'] 

# ------------------------------------------------------------------
# TODO: Extract the data for shop EXITO
# ------------------------------------------------------------------

for category in categories:
    # Bar progress -> comment
    for _ in track(range(100), description=f'[green]Iniciando Scraping en La Licorera categoria: {category}'):
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
    
    driver.get(f"https://www.lalicorera.com/productos/{category}")
    
    time.sleep(5)

    height = driver.execute_script("return document.body.scrollHeight")
    for i in range(height):
        driver.execute_script('window.scrollBy(0,10)') # scroll by 20 on each iteration
        height = driver.execute_script("return document.body.scrollHeight") # reset height to the new height after scroll-triggered elements have been loaded.
        time.sleep(0.01)

    # height = driver.execute_script("return document.body.scrollHeight")
    # for scrol in range(100,height,100):
    #     driver.execute_script(f"window.scrollTo(0,{scrol})")
    #     time.sleep(0.1)
    
    # break
    # Search the elements of the page
    items = driver.find_elements(
        By.CSS_SELECTOR,  ".item.product-card")
    # Create a frame empty for the data
    data = []
    # iterate over each element
    for i in items:
        name = findElementTextBySelector(
            ".product-card-description-title", "SIN DESCRIPCION")
        brand = findElementTextBySelector(
            ".class", "SIN MARCA")
        price_prime = findElementNumberBySelector(
            ".class", "0")    
        price_regular = findElementNumberBySelector(
            ".product-card-description-before", "0")
        price_now = findElementNumberByXPATH(
            "//p[@class='product-card-description-price']", "0")
        # price_now = driver.find_element(By.XPATH, "//p[@class='product-card-description-price']").text
        discount = findElementNumberBySelector(
            ".class", "0")

        data.append({f"shop": "LA LICORERA",
                            "city": "Nacional",
                            "location": "Store",
                            "category": category,
                            "name": name,
                            "brand": brand,
                            "price_prime": price_prime,
                            "price_regular": price_regular,
                            "price_now": price_now,
                            "discount": discount})

    df = pd.DataFrame(data)
    df.to_csv(f'C:\workflow\dt_web_scraping\prod\data\la_licorera_{category}_data.txt',
                index=False, encoding='utf-8')

    time.sleep(1)
    driver.quit()

time.sleep(3)
driver.quit()