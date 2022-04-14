from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

options = Options()
# options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)


# driver.get("http://www.python.org")
# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()

def sel_invoke(url):
    driver.get(url)
    elem = driver.find_element_by_id("search")
    childNodes = elem.find_elements(By.XPATH(("./child::*")))

    # for child in childNodes:
    #     print(child)

    time.sleep(10)
    driver.close()
    return None