from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.add_argument("--disable-software-rasterizer")
driver = webdriver.Chrome(options=options)

def sel_invoke(url, list):
    page_list = []
    driver.get(url)
    driver.implicitly_wait(0.5)
    next_page = driver.find_elements(By.ID, value="pnnext")
    source = driver.page_source
    next_page[0].click()
    page_list.append(source)
    driver.implicitly_wait(0.5)
    current_page_url = driver.current_url
   
    print(next_page)
    while (next_page):
        sel_invoke(current_page_url, page_list)
    
    driver.close()
    return current_page_url, page_list

