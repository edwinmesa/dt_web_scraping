# ------------------------------------------------------------------
# TODO: functions
# ------------------------------------------------------------------

class WebScraping:
    def initBrowserFirefox():
        options = Options()
        options.set_preference("network.http.pipelining", True)
        options.set_preference("network.http.proxy.pipelining", True)
        options.set_preference("network.http.pipelining.maxrequests", 8)
        options.set_preference("content.switch.threshold", 250000)
        options.set_preference("browser.cache.memory.capacity", 65536)
        options.set_preference("general.startup.browser", False)
        options.set_preference("reader.parse-on-load.enabled", False)
        options.set_preference("browser.pocket.enabled", False)
        options.set_preference("loop.enabled", False)
        options.set_preference("browser.chrome.toolbar_style", 1)
        options.set_preference(
            "browser.display.show_image_placeholders", False)
        options.set_preference("browser.display.use_document_colors", False)
        options.set_preference("browser.display.use_document_fonts", 0)
        options.set_preference("browser.display.use_system_colors", True)
        options.set_preference("browser.formfill.enable", False)
        options.set_preference("browser.helperApps.deleteTempFileOnExit", True)
        options.set_preference("permissions.default.image", 2)
        options.set_preference("browser.tabs.forceHide", True)
        options.set_preference("browser.urlbar.autoFill", False)
        options.set_preference("browser.urlbar.autocomplete.enabled", False)
        driver = webdriver.Firefox(options=options)
        driver.maximize_window()

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
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

    def scrollDownFullPage(driver):
        height = driver.execute_script("return document.body.scrollHeight")
        for i in range(height):
            # scroll by 10 on each iteration
            driver.execute_script('window.scrollBy(0,10)')
            # reset height to the new height after scroll-triggered elements have been loaded.
            height = driver.execute_script("return document.body.scrollHeight")
            time.sleep(0.01)

    def process_data():
        # Function Beatiful View
        time.sleep(0.02)
