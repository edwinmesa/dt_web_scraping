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

# Categories used
categories = ['whisky', 'vino', 'cervezas',
              'tonica', 'tequilas-y-piscos', 'ron']

# ----------------------------------------------------------------
driver.get("https://www.exito.com/")

time.sleep(10)

# Slect City
open_modal = driver.find_element(
    By.XPATH, "//span[@class='exito-geolocation-3-x-addressResult']")
open_modal.click()
time.sleep(5)

select_geo = driver.find_element(
    By.XPATH, "//div[@class='exito-geolocation-3-x-contentOrderOption flex']//div[1]")
select_geo.click()
time.sleep(2)


select_modal = driver.find_element(
    By.CSS_SELECTOR, ".exito-geolocation-3-x-orderOptionsButton.orderoption-compra-recoge")
select_modal.click()
time.sleep(2)


select_city = driver.find_element(
    By.CSS_SELECTOR, ".exito-geolocation-3-x-cssUnderline.shippingaddress-lista-ciudad.w-100")
select_city.click()
time.sleep(2)


select_city_bog = driver.find_element(
    By.XPATH, "//div[@id='react-select-2-option-0']")
select_city_bog.click()
time.sleep(2)

select_address = driver.find_element(
    By.CSS_SELECTOR, ".buycollect-lista-almacen.exito-geolocation-3-x-listaAlmacen")
select_address.click()
time.sleep(2)

select_modal2 = driver.find_element(
    By.XPATH, "//div[@id='react-select-4-option-0']")
select_modal2.click()
time.sleep(2)

select_modal2 = driver.find_element(
    By.XPATH, "//button[normalize-space()='Confirmar']")
select_modal2.click()
time.sleep(10)

# ----------------------------------------------------------------

# PASS

# ----------------------------------------------------------------

select_menu = driver.find_element(
    By.ID, "category-menu")
select_menu.click()
time.sleep(15)


select_mercado = driver.find_element(
    By.ID, "undefined-nivel2-Mercado")
select_mercado.click()
time.sleep(10)


select_menu_whisky = driver.find_element(
    By.XPATH, "//p[@id='Categorías-nivel3-Whisky, ron, brandy y coñac']")
select_menu_whisky.click()

# sleep for a few seconds before loading the page
time.sleep(20)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
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
        time.sleep(2)
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, initial_XPATH))).click()
        count += 1
        time.sleep(10)
    except TimeoutException:
        break

print("Continue......")

items = driver.find_elements(
    By.ID,  "gallery-layout-container")

data_exito = []

for i in items:
    try:
        name = i.find_element(
            By.CSS_SELECTOR, ".vtex-flex-layout-0-x-flexColChild.vtex-flex-layout-0-x-flexColChild--product-info.pb0").text.strip().upper()
    except:
        name = "SIN DESCRIPCION"
    print(name)


print("Exit......")


# select_menu_whisky = driver.find_element(
#     By.CSS_SELECTOR, ".exito-filters-0-x-filterItem.exito-filters-0-x-filterItem--new-layout-filters.exito-filters-0-x-filterItem--whisky.exito-filters-0-x-filterItem--new-layout-filters--whisky.lh-copy.w-100")
# select_menu_whisky.click()
# time.sleep(2)
# select_cat_lic = driver.find_element(
#     By.XPATH, "//strong[@id='Categorías-nivel2-Licores']")
# select_cat_lic.click()
# time.sleep(5)

# select_b_menu = driver.find_element(
#     By.CSS_SELECTOR, ".exito-filters-0-x-filter__container.exito-filters-0-x-filter__container--new-layout-filters.bb.b--muted-4.exito-filters-0-x-filter__container--category-3")
# select_b_menu.click()
# time.sleep(10)