# import libraries
from ast import Break
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
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
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


# def findElementTextByHTMLXPATH(selector, exception):
#     try:
#         element = i.find_element(
#             By.XPATH, selector).text.strip().upper()
#     except NoSuchElementException:
#         continue
#     return element


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


def findElementNumberByXPATH(selector, exception):
    try:
        element = i.find_element(
            By.XPATH, selector).text.replace('$', '')
        element = "".join([ch for ch in element if ch.isdigit()])
    except NoSuchElementException:
        element = exception
    return element


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
        time.sleep(0.01)

# Function Beatiful View


def process_data():
    time.sleep(0.02)

# Categories of brands that should be considered for search results


shops = ["Calle 10 #42-63, Medellín"]
categories = ['vinos']

# ------------------------------------------------------------------
# TODO: Extract the data for shop EXITO
# ------------------------------------------------------------------

for city in shops:
    for category in categories:
        # Bar progress -> comment
        for _ in track(range(100), description=f'[green]Iniciando Scraping en Rappi categoria: {category}'):
            process_data()
        # Initialized by selenium driver with options and optmizer
        options = Options()
        # options.set_preference("network.http.pipelining", True)
        # options.set_preference("network.http.proxy.pipelining", True)
        # options.set_preference("network.http.pipelining.maxrequests", 8)
        # options.set_preference("content.switch.threshold", 250000)
        # options.set_preference("browser.cache.memory.capacity", 65536)
        # options.set_preference("general.startup.browser", False)
        # # Disable reader, we won't need that.
        # options.set_preference("reader.parse-on-load.enabled", False)
        # options.set_preference("browser.pocket.enabled", False)
        # options.set_preference("loop.enabled", False)
        # # Text on Toolbar instead of icons
        # options.set_preference("browser.chrome.toolbar_style", 1)
        # # Don't show thumbnails on not loaded images.
        # options.set_preference(
        #     "browser.display.show_image_placeholders", False)
        # # Don't show document colors.
        # options.set_preference("browser.display.use_document_colors", False)
        # # Don't load document fonts.
        # options.set_preference("browser.display.use_document_fonts", 0)
        # # Use system colors.
        # options.set_preference("browser.display.use_system_colors", True)
        # # Autofill on forms disabled.
        # options.set_preference("browser.formfill.enable", False)
        # # Delete temprorary files.
        # options.set_preference("browser.helperApps.deleteTempFileOnExit", True)
        # options.set_preference("permissions.default.image", 2)
        # # Disable tabs, We won't need that.
        # options.set_preference("browser.tabs.forceHide", True)
        # # Disable autofill on URL bar.
        # options.set_preference("browser.urlbar.autoFill", False)
        # # Disable autocomplete on URL bar.
        # options.set_preference("browser.urlbar.autocomplete.enabled", False)

        driver = webdriver.Firefox(options=options)
        driver.maximize_window()

        # Open the Page

        driver.get(
            f"https://www.rappi.com.co/tiendas/900131965-turbo-licores-home/licores/{category}")

        time.sleep(10)
        # Select the geolocation
        findElementBy(
            By.CSS_SELECTOR, ".sc-cZwWEu.eJnuUV.ButtonAddress__text", 4)
        # # Select for send the city
        findElementBy(
            By.CSS_SELECTOR, ".chakra-input.css-5p5pfl", 4)
        # # Send The City
        findElementByAndSendKey(
            By.CSS_SELECTOR, ".chakra-input.css-u3tcey", city, 4)
        # Select the direction
        findElementBy(
            By.CSS_SELECTOR, ".sc-hAZoDl.FcjuD.sc-ikZpkk.fpunMk", 4)

        findElementBy(
            By.CSS_SELECTOR, ".chakra-stack.css-1cp68dr", 4)

        findElementBy(
            By.CSS_SELECTOR, ".sc-y1vkgn-3.kAbqxb", 4)
        # Save the location
        findElementBy(
            By.CSS_SELECTOR, ".chakra-modal__footer.css-1pw6her", 2)

        # Expand the category
        # findElementBy(
        #     By.CSS_SELECTOR, ".sc-bdVaJa sc-bwzfXH gJFplR tertiary big", 5)

        scrollDownFullPage(driver)

        initial_XPATH = ".sc-bdVaJa.sc-bwzfXH.gJFplR.tertiary.big"

        # define the max clicks for page for default 30
        max_click_SHOW_MORE = 1
        # count the number of clicks
        count = 1
        # This loop search the button load more and apply the click until the end of page
        while count <= max_click_SHOW_MORE:
            try:
                WebDriverWait(driver, 30).until(
                    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, initial_XPATH)))
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, initial_XPATH))).click()
                count += 1
                time.sleep(5)
                # Bar progress -> comment
                for i in track(range(4), description=f"[red]Explorando Pagina Web iter {count - 1}.........."):
                    time.sleep(1)

            except TimeoutException:
                break

        # break
        # Search the elements of the page
        items = driver.find_elements(
            By.XPATH,  "/html/body/div[1]/div[4]/div[2]/div[2]/ul/div[1]/a")

        # /html/body/div[1]/div[4]/div[2]/div[2]/ul/div[1]/a
        data = []
        max_div = 50
        countdiv = 1
        while countdiv <= max_div:
            try:
                for i in items:
                    #  if len((i.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[2]/div[2]/ul/div[{countdiv}]/a/div/div[2]/h4").text)):
                    #     oferta = 0
                    #  else:
                    #     oferta = i.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[2]/div[2]/ul/div[{countdiv}]/a/div/div[2]/h4").text    
                     
                    #  print(oferta)
                    #  if(i.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[2]/div[2]/ul/div[{countdiv}]/a/div/div[2 + {countdiv}]/h4").text) is None:
                    name = i.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[2]/div[2]/ul/div[{countdiv}]/a/div/div[3]/h4").text
                    #  else:
                    #     name = i.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[2]/div[2]/ul/div[{countdiv}]/a/div/div[2 + {countdiv}]/h4").text

                        # /html/body/div[1]/div[4]/div[2]/div[2]/ul/div[1]/a/div/div[3]/h4  1   oferta
                        # /html/body/div[1]/div[4]/div[2]/div[2]/ul/div[2]/a/div/div[2]/h4  2   normal
                        # /html/body/div[1]/div[4]/div[2]/div[2]/ul/div[3]/a/div/div[3]/h4  3   oferta
                        # /html/body/div[1]/div[4]/div[2]/div[2]/ul/div[4]/a/div/div[2]/h4  4   normal
      

                    # price_regular = i.find_element(
                    #     By.XPATH, f"/html/body/div[1]/div[4]/div[2]/div[2]/ul/div[{countdiv}]/a/div/div[1]/span[1]").text.replace('$', '')
                    # price_regular = "".join(
                    #     [ch for ch in price_regular if ch.isdigit()])

                    # price_now = i.find_element(
                    #     By.XPATH, f"/html/body/div[1]/div[4]/div[2]/div[2]/ul/div[{countdiv}]/a/div/div[1]/span[2]").text.replace('$', '')
                    # price_now = "".join(
                    #     [ch for ch in price_now if ch.isdigit()])

                    # discount = i.find_element(
                    #     By.XPATH, f"/html/body/div[1]/div[4]/div[2]/div[2]/ul/div[{countdiv}]/a/div/div[2]/span").text.replace('%', '')
                    # discount = "".join([ch for ch in discount if ch.isdigit()])

                countdiv += 1
            except NoSuchElementException:
                break

            # print(name)
            rprint(
                "SKU: " + name,
                # "nombre: {}"+ name  
                # "|price desc: " + price_now,
                # "|desc: " + discount
            )

        #     data.append({f"shop": "RAPPI",
        #                  "city": city,
        #                  "location": "Store",
        #                  "category": category,
        #                  "name": name,
        #                  "brand": brand,
        #                  "price_prime": price_prime,
        #                  "price_regular": price_regular,
        #                  "price_now": price_now,
        #                  "discount": discount})

        # df = pd.DataFrame(data)
        # df.to_csv(f'C:\workflow\dt_web_scraping\prod\data\rappi_data.txt',
        #           index=False, encoding='utf-8')

        time.sleep(1)
        driver.quit()

time.sleep(3)
driver.quit()
