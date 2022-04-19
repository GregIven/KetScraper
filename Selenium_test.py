from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.add_argument("--disable-software-rasterizer")
driver = webdriver.Chrome(options=options)

def sel_invoke(url):
    page_list = []
    driver.get(url)
    driver.implicitly_wait(0.5)
    next_page = driver.find_elements(By.ID, value="pnnext")
    source = driver.page_source
    page_list.append(source)
    next_page[0].click()
    driver.implicitly_wait(0.5)
   
    # print(next_page)
    # while (next_page):
    #     if (driver.find_elements(By.ID, value="pnnext")):
    #         next_page = driver.find_elements(By.ID, value="pnnext")
    #         source = driver.page_source
    #         page_list.append(source)
    #         next_page[0].click()
    #         driver.implicitly_wait(0.5)
    #     else:
    #         driver.close()
    #         return page_list

    return page_list

        



