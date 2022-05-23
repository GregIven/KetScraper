from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support import expected_conditions as EC
import time

from parse_defs import *

options = Options()
options.add_argument("--disable-software-rasterizer")
options.add_argument("--headless")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)

def sel_invoke(url):
    page_list = []
    driver.get(url)
    driver.implicitly_wait(30)
    next_page = driver.find_elements(By.ID, value="pnnext")

    # source = driver.page_source
    source_dict = html_parser(url)
    parsed_page = parse_page_results(source_dict["soup"])
    redir_url = source_dict["redirect"]
    page_list.append(parsed_page)
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

    return {"pages": page_list, "redirect": redir_url}

        



