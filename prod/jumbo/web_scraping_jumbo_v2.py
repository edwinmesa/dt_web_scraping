import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd

# Initialized by selenium driver
driver = webdriver.Firefox()
driver.maximize_window()

# Categories of brands

categories = ['whisky', 'vino', 'cervezas',
              'tequilas-y-piscos', 'ron']


for category in categories:
    driver.get(
        f"https://www.tiendasjumbo.co/supermercado/vinos-y-licores/{category}")

    time.sleep(15)

    # class vtex button load more
    initial_XPATH = "//div[contains(@class,'vtex-button__label flex items-center justify-center h-100 ph5')]"
    # define the max clicks for page
    max_click_SHOW_MORE = 20
    # count the number of clicks
    count = 1
    while count <= max_click_SHOW_MORE:
        try:
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, initial_XPATH))).click()
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, initial_XPATH))).click()
            count += 1
            time.sleep(10)
        except TimeoutException:
            break

    items = driver.find_elements(
        By.CSS_SELECTOR,  ".vtex-product-summary-2-x-element.pointer.pt3.pb4.flex.flex-column.h-100")

    data_jumbo = []

    for i in items:
        try:
            name = i.find_element(
                By.CSS_SELECTOR, ".vtex-product-summary-2-x-productBrand.vtex-product-summary-2-x-brandName.t-body").text.strip().upper()
        except:
            name = "SIN DESCRIPCION"
        try:
            brand = i.find_element(
                By.CSS_SELECTOR, ".vtex-product-summary-2-x-productBrandName").text.strip().upper()
        except:
            brand = "SIN MARCA"
        try:
            price_jumbo_prime = i.find_element(
                By.CSS_SELECTOR, ".tiendasjumboqaio-jumbo-minicart-2-x-generalPrice.tiendasjumboqaio-jumbo-minicart-2-x-primePrice.tiendasjumboqaio-jumbo-minicart-2-x-generalPriceSmall").text
        except:
            price_jumbo_prime = 0
        try:
            price_regular = i.find_element(
                By.CSS_SELECTOR, ".tiendasjumboqaio-jumbo-minicart-2-x-cencoPriceWithoutDiscount").text
        except:
            price_regular = 0
        try:
            price_now = i.find_element(
                By.CSS_SELECTOR, ".vtex-flex-layout-0-x-flexRow.vtex-flex-layout-0-x-flexRow--selling-price").text
        except:
            price_now = 0
        try:
            discount = i.find_element(
                By.CSS_SELECTOR, ".tiendasjumboqaio-jumbo-minicart-2-x-containerPercentageFlag").text
        except:
            discount = 0

        data_jumbo.append({"shop": "JUMBO", "name": name, "brand": brand, "price_jumbo_prime": price_jumbo_prime, "price_regular": price_regular,
                           "price_now": price_now, "discount": discount})

    df = pd.DataFrame(data_jumbo)
    df.to_csv(f'C:\workflow\dt_web_scraping\prod\data\jumbo_{category}_data.txt',
              index=False, encoding='utf-8')
